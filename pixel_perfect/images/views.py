import os

import google.oauth2.credentials
from celery.result import AsyncResult
from django.conf import settings
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import FileResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import DeleteView, FormView
from django.views.generic.list import ListView
from image_processing import config
from image_processing.img_processing import ImgProcesses
from images.celery_tasks import upscale_image_task, enhance_image_task, image_restoration_task
from images.forms import EnhanceImagesForm, UpscaleImagesForm
from images.models import EnhancedImages
from users.gdrive import drive_manager
from users.mixins import CustomLoginRequiredMixin
from billiard.exceptions import WorkerLostError


class UpscaleImageView(CustomLoginRequiredMixin, FormView):
    template_name = "images/upscale-image.html"
    form_class = UpscaleImagesForm

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            img_file = request.FILES.get("img_path")
            model = form.cleaned_data.get("upscale_method")
            scale = form.cleaned_data.get("upscale_size")

            filename, _ = os.path.splitext(img_file.name)

            save_as_name = f"{filename}_{model}_x{scale}.jpeg"
            save_to_path = os.path.join(settings.BASE_DIR, config.upscaled_img_path, str(request.user.id))
            image_path = os.path.join(save_to_path, save_as_name)

            ImgProcesses.img_write_from_memory(file=img_file, save_to_path=image_path)

            upscale_params = {
                "src_image_path": image_path,
                "cnn_model": model,
                "scale": int(scale),
                "do_compress": form.cleaned_data.get("do_compress"),
                "quality_factor": form.cleaned_data.get("compress_q_factor"),
            }

            upscale_task = upscale_image_task.delay(upscale_params, request.user.id)
            return JsonResponse({"form_valid": True, 'task_id': upscale_task.id})

        return JsonResponse({"form_valid": False})


class EnhanceImageView(CustomLoginRequiredMixin, FormView):
    template_name = "images/enhance-image.html"
    form_class = EnhanceImagesForm

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            img_file = request.FILES.get("img_path")
            model = form.cleaned_data.get("image_type")

            filename, _ = img_file.name.split('.')

            save_as_name = f"{filename}_{model}.jpeg"
            save_to_path = os.path.join(settings.BASE_DIR, config.enhanced_img_path, str(request.user.id))
            image_path = os.path.join(save_to_path, save_as_name)

            ImgProcesses.img_write_from_memory(file=img_file, save_to_path=image_path)

            enhance_params = {
                "src_image_path": image_path,
                "img_type": model,
                "enhance_qfactor": int(request.POST.get("quality_factor")),
            }

            enhance_task = enhance_image_task.delay(enhance_params, request.user.id)

            return JsonResponse({"form_valid": True, 'task_id': enhance_task.id})
        return JsonResponse({"form_valid": False})


class FullEnhancementView(CustomLoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        upscale_form = UpscaleImagesForm()
        enhance_form = EnhanceImagesForm()

        context = {
            "upscale_form": upscale_form,
            "enhance_form": enhance_form,
        }
        return render(request, template_name="images/total-enhancement-image.html", context=context)

    def post(self, request, *args, **kwargs):
        upscale_form = UpscaleImagesForm(self.request.POST, self.request.FILES)
        enhance_form = EnhanceImagesForm(self.request.POST, self.request.FILES)

        if upscale_form.is_valid() and enhance_form.is_valid():
            img_file = request.FILES.get("img_path")
            model = enhance_form.cleaned_data.get("image_type")
            scale = upscale_form.cleaned_data.get("upscale_size")

            filename, _ = img_file.name.split('.')

            save_as_name = f"{filename}_{model}_x{scale}.jpeg"
            save_to_path = os.path.join(settings.BASE_DIR, config.enhanced_img_path, str(request.user.id))
            image_path = os.path.join(save_to_path, save_as_name)

            ImgProcesses.img_write_from_memory(file=img_file, save_to_path=image_path)

            upscale_params = {
                "src_image_path": image_path,
                "cnn_model": upscale_form.cleaned_data.get("upscale_method"),
                "scale": int(scale),
                "do_compress": upscale_form.cleaned_data.get("do_compress"),
                "quality_factor": upscale_form.cleaned_data.get("compress_q_factor"),
            }

            enhance_params = {
                "src_image_path": image_path,
                "img_type": model,
                "enhance_qfactor": int(request.POST.get("quality_factor")),
            }

            restore_image_task = image_restoration_task.delay(upscale_params, enhance_params, request.user.id)

            return JsonResponse({"form_valid": True, 'task_id': restore_image_task.id})
        return JsonResponse({"form_valid": False})


class ImageGalleryView(CustomLoginRequiredMixin, ListView):
    template_name = "images/images-list.html"
    model = EnhancedImages
    context_object_name = "images"
    paginate_by = 6

    def get_queryset(self):
        return EnhancedImages.objects.filter(img_owner=self.request.user.id).order_by('-date_created')


class TrackTaskView(View):
    def get(self, request):
        task_id = request.GET.get("task_id")
        result_wrapper = AsyncResult(task_id)

        try:
            return JsonResponse({"status": result_wrapper.status, 'result': result_wrapper.result})
        except TypeError:
            return JsonResponse({"status": 'ABORTED'})


class DeleteImageView(CustomLoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = EnhancedImages
    success_url = reverse_lazy("images_list")
    success_message = "Image has been deleted successfully."

    def get_object(self, queryset=None):
        return EnhancedImages.objects.get(pk=self.request.GET.get("img_id"))


class GoogleDriveUploadView(CustomLoginRequiredMixin, View):
    def get(self, request, pk):
        image_db = get_object_or_404(EnhancedImages, pk=pk, img_owner=request.user.id)

        if not request.session.get("credentials", False):
            request.session["img_id"] = pk
            return redirect("authorize")

        credentials = google.oauth2.credentials.Credentials(**request.session["credentials"])

        file_path = f'{settings.BASE_DIR}' + image_db.img_path.url

        params = {
            "src_image": file_path,
            "save_image_name": image_db.img_name,
            "mime_type": "image/jpeg",
            "folder_id": drive_manager.get_gdrive_folder_id(credentials),
        }

        drive_manager.uploadImage(credentials=credentials, **params)

        if request.session.get("img_id", None):
            request.session.pop("img_id")

        messages.success(request, "Image successfully saved to Google Drive!")
        return redirect("images_list")


class DownloadImageView(CustomLoginRequiredMixin, View):
    def get(self, request, pk):
        image_db = get_object_or_404(EnhancedImages, pk=pk, img_owner=request.user.id)
        img_url = f'{settings.BASE_DIR}' + image_db.img_path.url

        response = FileResponse(open(img_url, "rb"), as_attachment=True)
        return response

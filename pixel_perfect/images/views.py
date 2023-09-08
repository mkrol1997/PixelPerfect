import os
from datetime import date
from pathlib import Path

import google.oauth2.credentials
from django.conf import settings
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import FileResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import DeleteView, FormView
from django.views.generic.list import ListView
from images.forms import EnhanceImagesForm, UpscaleImagesForm
from images.models import EnhancedImages
from users.gdrive.manager import get_gdrive_folder_id, uploadImage
from users.mixins import CustomLoginRequiredMixin

from image_processing.img_manager import ImageManager


class UpscaleImageView(CustomLoginRequiredMixin, FormView):
    template_name = "images/upscale-image.html"
    form_class = UpscaleImagesForm
    permission_denied_message = "You need to be logged in to view this page. Please login or register!"

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            upscale_params = {
                "src_image": form.cleaned_data.get("img_path"),
                "cnn_model": form.cleaned_data.get("upscale_method"),
                "scale": int(form.cleaned_data.get("upscale_size")),
                "user_id": str(request.user.id),
                "do_compress": form.cleaned_data.get("do_compress"),
                "quality_factor": form.cleaned_data.get("compress_q_factor"),
                "enhance_after": False,
            }

            upscaled_image = ImageManager.upscale_image(**upscale_params)

            image_name = upscaled_image.split("\\")[-1]
            img_path = os.path.join("/upscaled_images/{}/{}".format(request.user.id, image_name))

            image_db, _ = EnhancedImages.objects.update_or_create(
                img_owner=request.user, img_path=img_path, img_name=image_name, date_created=date.today()
            )

            return JsonResponse({"form_valid": True, "src": image_db.img_path.url, "img_id": image_db.id})

        return JsonResponse({"form_valid": False})


class EnhanceImageView(CustomLoginRequiredMixin, FormView):
    template_name = "images/enhance-image.html"
    form_class = EnhanceImagesForm
    permission_denied_message = "You need to be logged in to view this page. Please login or register!"

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            enhance_params = {
                "src_image": request.FILES.get("img_path"),
                "img_type": request.POST.get("image_type"),
                "user_id": str(request.user.id),
                "enhance_qfactor": int(request.POST.get("quality_factor")),
            }

            enhanced_image = ImageManager.enhance_image(**enhance_params)
            image_name = enhanced_image.split("\\")[-1]

            img_path = os.path.join("/enhanced_images/{}/{}".format(request.user.id, image_name))

            image_db, _ = EnhancedImages.objects.update_or_create(
                img_owner=request.user, img_path=img_path, img_name=image_name, date_created=date.today()
            )
            return JsonResponse({"form_valid": True, "src": image_db.img_path.url, "img_id": image_db.id})
        return JsonResponse({"form_valid": False})


class FullEnhancementView(CustomLoginRequiredMixin, View):
    permission_denied_message = "You need to be logged in to view this page. Please login or register!"

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
            upscale_params = {
                "src_image": upscale_form.cleaned_data.get("img_path"),
                "cnn_model": upscale_form.cleaned_data.get("upscale_method"),
                "scale": int(upscale_form.cleaned_data.get("upscale_size")),
                "user_id": str(request.user.id),
                "do_compress": upscale_form.cleaned_data.get("do_compress"),
                "quality_factor": upscale_form.cleaned_data.get("compress_q_factor"),
                "enhance_after": True,
            }

            upscaled_image = ImageManager.upscale_image(**upscale_params)

            enhance_params = {
                "src_image": upscaled_image,
                "img_type": enhance_form.cleaned_data.get("image_type"),
                "user_id": str(request.user.id),
                "enhance_qfactor": int(enhance_form.cleaned_data.get("quality_factor")),
            }

            enhanced_image = ImageManager.enhance_image(**enhance_params)
            image_name = enhanced_image.split("\\")[-1]

            img_path = os.path.join("/enhanced_images/{}/{}".format(request.user.id, image_name))

            image_db, _ = EnhancedImages.objects.update_or_create(
                img_owner=request.user, img_path=img_path, img_name=image_name, date_created=date.today()
            )
            return JsonResponse({"src": image_db.img_path.url, "img_id": image_db.id, "form_valid": True})
        return JsonResponse({"form_valid": False})


class ImageGalleryView(CustomLoginRequiredMixin, ListView):
    template_name = "images/images-list.html"
    model = EnhancedImages
    context_object_name = "images"
    paginate_by = 6
    ordering = ["-date_created"]
    permission_denied_message = "You need to be logged in to view this page. Please login or register!"

    def get_queryset(self):
        return EnhancedImages.objects.filter(img_owner=self.request.user.id)


class DeleteImageView(CustomLoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = EnhancedImages
    success_url = reverse_lazy("images_list")
    success_message = "Image has been deleted successfully."
    permission_denied_message = "You need to be logged in to view this page. Please login or register!"

    def get_object(self, queryset=None):
        return EnhancedImages.objects.get(pk=self.request.GET.get("img_id"))

    def delete(self, request, *args, **kwargs):
        messages.info(self.request, self.success_message)
        return super(DeleteImageView, self).delete(request, *args, **kwargs)


class GoogleDriveUploadView(CustomLoginRequiredMixin, View):
    def get(self, request, pk):
        image_db = get_object_or_404(EnhancedImages, pk=pk, img_owner=request.user.id)

        if not request.session.get("credentials", False):
            request.session["img_id"] = pk
            return redirect("authorize")

        credentials = google.oauth2.credentials.Credentials(**request.session["credentials"])

        img_abs_url = str(settings.BASE_DIR) + image_db.img_path.url
        image_name = image_db.img_name
        folder_id = get_gdrive_folder_id(credentials)

        params = {
            "src_image": img_abs_url,
            "save_image_name": image_name,
            "mime_type": "image/jpeg",
            "folder_id": folder_id,
        }

        uploadImage(credentials=credentials, **params)

        if request.session.get("img_id", None):
            request.session.pop("img_id")

        messages.success(request, "Image successfully saved to Google Drive!")
        return redirect(reverse("images_list"))


class DownloadImageView(CustomLoginRequiredMixin, View):
    def get(self, request, pk):
        image_db = get_object_or_404(EnhancedImages, pk=pk, img_owner=request.user.id)
        img_abs_url = str(settings.BASE_DIR) + image_db.img_path.url

        response = FileResponse(open(img_abs_url, "rb"), as_attachment=True)
        return response

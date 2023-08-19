import os
from pathlib import Path

import google.oauth2.credentials
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import FileResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.views import View
from django.views.generic.list import ListView
from images.forms import EnhanceImagesForm, FullEnhancementForm, UpscaleImagesForm
from images.models import EnhancedImages
from users.gdrive.manager import get_gdrive_folder_id, uploadImage

from image_processing.img_manager import ImageManager


class UpscaleImageView(LoginRequiredMixin, View):
    login_alert_message = "You need to be logged in to view this page. Please login or register!"
    message_level = messages.INFO

    def get(self, request):
        form_class = UpscaleImagesForm
        return render(request, "upscale-image.html", context={"form": form_class})

    def post(self, request):
        upscale_params = {
            "src_image": request.FILES.get("src_image"),
            "cnn_model": request.POST.get("upscale_method"),
            "scale": int(request.POST.get("upscale_size")),
            "user_id": str(request.user.id),
            "do_compress": request.POST.get("do_compress"),
            "quality_factor": request.POST.get("compress_q_factor"),
            "enhance_after": False,
        }

        upscaled_image = ImageManager.upscale_image(**upscale_params)
        image_name = upscaled_image.split("\\")[-1]

        img_path = os.path.join("/upscaled_images/{}/{}".format(request.user.id, image_name))

        image_db = EnhancedImages.objects.filter(img_path=img_path).first()

        if not image_db:
            image_db = EnhancedImages(
                img_owner=self.request.user, img_path=img_path, img_name=Path(upscaled_image).name
            )
        else:
            image_db.img_path = img_path

        image_db.save()
        return JsonResponse({"src": image_db.img_path.url, "img_id": image_db.id})


class EnhanceImageView(LoginRequiredMixin, View):
    def get(self, request):
        form_class = EnhanceImagesForm
        return render(request, template_name="enhance-image.html", context={"form": form_class})

    def post(self, request):
        enhance_params = {
            "src_image": request.FILES.get("src_image"),
            "img_type": request.POST.get("image_type"),
            "user_id": str(request.user.id),
            "enhance_qfactor": int(request.POST.get("quality_factor")),
        }

        enhanced_image = ImageManager.enhance_image(**enhance_params)
        image_name = enhanced_image.split("\\")[-1]

        img_path = os.path.join("/enhanced_images/{}/{}".format(request.user.id, image_name))

        image_db = EnhancedImages.objects.filter(img_path=img_path).first()

        if not image_db:
            image_db = EnhancedImages(
                img_owner=self.request.user, img_path=img_path, img_name=Path(enhanced_image).name
            )

        else:
            image_db.img_path = img_path

        image_db.save()
        return JsonResponse({"src": image_db.img_path.url, "img_id": image_db.id, "upload_redirect": ""})


class FullEnhancementView(LoginRequiredMixin, View):
    def get(self, request):
        form_class = FullEnhancementForm
        return render(request, template_name="total-enhancement-image.html", context={"form": form_class})

    def post(self, request):
        upscale_params = {
            "src_image": request.FILES.get("src_image"),
            "cnn_model": request.POST.get("upscale_method"),
            "scale": int(request.POST.get("upscale_size")),
            "user_id": str(request.user.id),
            "do_compress": request.POST.get("do_compress"),
            "quality_factor": request.POST.get("compress_q_factor"),
            "enhance_after": True,
        }

        upscaled_image = ImageManager.upscale_image(**upscale_params)

        enhance_params = {
            "src_image": upscaled_image,
            "img_type": request.POST.get("image_type"),
            "user_id": str(request.user.id),
            "enhance_qfactor": int(request.POST.get("quality_factor")),
        }

        enhanced_image = ImageManager.enhance_image(**enhance_params)
        image_name = enhanced_image.split("\\")[-1]

        img_path = os.path.join("/enhanced_images/{}/{}".format(request.user.id, image_name))

        image_db = EnhancedImages.objects.filter(img_path=img_path).first()

        if not image_db:
            image_db = EnhancedImages(
                img_owner=self.request.user, img_path=img_path, img_name=Path(enhanced_image).name
            )

        else:
            image_db.img_path = img_path

        image_db.save()
        return JsonResponse({"src": image_db.img_path.url, "img_id": image_db.id, "upload_redirect": ""})


class ImagesListView(LoginRequiredMixin, ListView):
    model = EnhancedImages
    template_name = "images-list.html"
    context_object_name = "images"

    def get_queryset(self):
        return EnhancedImages.objects.filter(img_owner=self.request.user.id)


class ImageUploadView(LoginRequiredMixin, View):
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
        return redirect(reverse("images-list"))


class ImageSaveView(LoginRequiredMixin, View):
    def get(self, request, pk):
        image_db = get_object_or_404(EnhancedImages, pk=pk, img_owner=request.user.id)
        img_abs_url = str(settings.BASE_DIR) + image_db.img_path.url

        response = FileResponse(open(img_abs_url, "rb"), as_attachment=True)
        return response

import os
from pathlib import Path

import google.oauth2.credentials
from django.conf import settings
from django.contrib import messages
from django.http import FileResponse, JsonResponse
from django.shortcuts import redirect, render, reverse
from django.views import View
from django.views.generic.list import ListView
from images.forms import EnhanceImagesForm, UpscaleImagesForm
from images.models import EnhancedImages
from users.gdrive.manager import get_gdrive_folder_id, uploadImage

from image_processing.img_manager import ImageManager


class UpscaleImageView(View):
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
        }

        print(request.FILES.get("src_image"))

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


class EnhanceImageView(View):
    def get(self, request):
        form_class = EnhanceImagesForm
        return render(request, template_name="enhance-image.html", context={"form": form_class})

    def post(self, request):
        upscale_params = {
            "src_image": request.FILES.get("src_image"),
            "img_type": request.POST.get("image_type"),
            "user_id": str(request.user.id),
            "enhance_qfactor": int(request.POST.get("quality_factor")),
        }

        enhanced_image = ImageManager.enhance_image(**upscale_params)
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


class ImagesListView(ListView):
    model = EnhancedImages
    template_name = "images-list.html"
    queryset = EnhancedImages.objects.filter(img_owner=24)
    context_object_name = "objects"


class ImageUploadView(View):
    def get(self, request, pk):
        if not request.session.get("credentials", False):
            request.session["img_id"] = pk
            return redirect("authorize")

        credentials = google.oauth2.credentials.Credentials(**request.session["credentials"])

        image_db = EnhancedImages.objects.get(pk=pk)

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

        messages.success(request, "Image saved to Google Drive! You can access all images in the gallery!")
        return redirect(reverse("dashboard"))


class ImageSaveView(View):
    def get(self, request, pk):
        image_db = EnhancedImages.objects.get(pk=pk)

        img_abs_url = str(settings.BASE_DIR) + image_db.img_path.url
        response = FileResponse(open(img_abs_url, "rb"), as_attachment=True)

        return response

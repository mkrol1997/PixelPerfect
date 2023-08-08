import os
from pathlib import Path

from django.http import JsonResponse
from django.shortcuts import render, reverse
from django.views import View
from django.views.generic.list import ListView
from images.forms import EnhanceImagesForm, UpscaleImagesForm
from images.models import EnhancedImages

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
        form = EnhanceImagesForm
        return render(request, template_name="upscale-image.html", context={"form": form})

    def post(self, request):
        upscale_params = {
            "src_image": request.FILES.get("src_image"),
            "img_type": request.POST.get("image_type"),
            "user_id": str(request.user.id),
            "quality_factor": request.POST.get("quality_factor"),
        }

        enhanced_image = ImageManager.enhance_image(**upscale_params)
        image_name = enhanced_image.split("\\")[-1]

        img_path = os.path.join("/enhanced)images/{}/{}".format(request.user.id, image_name))

        image_db = EnhancedImages.objects.filter(img_path=img_path).first()

        if not image_db:
            image_db = EnhancedImages(
                img_owner=self.request.user, img_path=img_path, img_name=Path(enhanced_image).name
            )
        else:
            image_db.img_path = img_path

        image_db.save()
        return JsonResponse({"src": image_db.img_path.url, "img_id": image_db.id})


class ImagesListView(ListView):
    model = EnhancedImages
    template_name = "images-list.html"
    queryset = EnhancedImages.objects.filter(img_owner=24)
    context_object_name = "objects"

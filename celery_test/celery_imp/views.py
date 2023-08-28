import os

from celery.result import AsyncResult
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from image_processing.img_processing import ImgProcesses

from image_processing import config
from .celery_conf import upscale_image_task
from .forms import UpscaleImagesForm


class TrackTaskView(View):
    def get(self, request):
        task_id = request.GET.get("task_id")
        result_wrapper = AsyncResult(task_id)
        return JsonResponse({"status": result_wrapper.status, 'result': result_wrapper.result})


class CreateUpscaleImageTaskView(View):
    def get(self, request):
        form_class = UpscaleImagesForm
        return render(request, "upscale-image.html", context={"form": form_class})

    def post(self, request):
        img_file = request.FILES.get("src_image")
        ImgProcesses.img_write_from_memory(img_file, config.upscaled_img_path)

        image_path = os.path.join(settings.BASE_DIR, config.upscaled_img_path, img_file.name)

        upscale_params = {
            "src_image_path": image_path,
            "cnn_model": request.POST.get("upscale_method"),
            "scale": int(request.POST.get("upscale_size")),
            "do_compress": request.POST.get("do_compress"),
            "quality_factor": request.POST.get("compress_q_factor"),
        }

        upscale_task = upscale_image_task.delay(upscale_params)

        return JsonResponse({'task_id': upscale_task.id})

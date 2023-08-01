from django.shortcuts import reverse
from django.views.generic import FormView
from images.forms import ImageForm
from images.models import EnhancedImages

from image_processing.img_manager import upscale_image


class UpscaleImageView(FormView):
    form_class = ImageForm
    template_name = 'upscale-image.html'

    def get_success_url(self):
        return reverse('upscale')

    def form_valid(self, form):
        upscale_settings = {
            'src_image': self.request.FILES.get('img_path'),
            'model': form.cleaned_data.get('upscale_method'),
            'scale': int(form.cleaned_data.get('upscale_size')),
            'user_id': self.request.user.id
        }

        enhanced_image = upscale_image(**upscale_settings)

        image_db = EnhancedImages(
            img_owner=self.request.user,
            img_path=enhanced_image,
            img_name=enhanced_image.split('\\')[-1])
        image_db.save()

        return super(UpscaleImageView, self).form_valid(form)

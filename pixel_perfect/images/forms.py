from django import forms
from django.forms import ModelForm
from images.models import EnhancedImages


class UpscaleImagesForm(ModelForm):
    upscale_method = forms.ChoiceField(
        label="Upscale Method",
        widget=forms.RadioSelect(),
        choices=[("edsr", "EDSR"), ("espcn", "ESPCN"), ("fsrcnn", "FSRCNN"), ("lapsrn", "LapSRN")],
    )

    upscale_size = forms.ChoiceField(
        label="Upscale size", widget=forms.RadioSelect, choices=[(2, "x2"), (3, "x3"), (4, "x4")]
    )

    do_compress = forms.BooleanField(required=False)
    compress_q_factor = forms.IntegerField(
        widget=forms.NumberInput(attrs={"type": "range", "step": "1", "min": "10", "max": "95"}), required=False
    )

    class Meta:
        model = EnhancedImages
        fields = ["img_path"]
        labels = {"img_path": "Image"}


class EnhanceImagesForm(ModelForm):
    image_type = forms.ChoiceField(
        label="Upscale Method",
        widget=forms.RadioSelect(),
        choices=[("color", "RGB Color"), ("color_real", "Realworld RGB Color"), ("greyscale", "Greyscale")],
    )

    quality_factor = forms.IntegerField(
        widget=forms.NumberInput(attrs={"type": "range", "step": "1", "min": "5", "max": "95"}), required=False
    )

    class Meta:
        model = EnhancedImages
        fields = ["img_path", "image_type", "quality_factor"]
        labels = {
            "img_path": "Image",
            "image_type": "Image type",
            "quality_factor": "Quality factor",
        }

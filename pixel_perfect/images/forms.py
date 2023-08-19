import os.path

from crispy_forms.bootstrap import InlineRadios
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Div, Field, Layout, Row, Submit
from django import forms
from django.forms import ModelForm
from images.models import EnhancedImages


class UpscaleImagesForm(ModelForm):
    class Meta:
        model = EnhancedImages
        fields = ["img_path"]

    upscale_method = forms.ChoiceField(
        widget=forms.RadioSelect(attrs={"class": "form-check form-check-inline radiobtn"}),
        choices=[("espcn", "ESPCN"), ("fsrcnn", "FSRCNN"), ("edsr", "EDSR"), ("lapsrn", "LapSRN")],
    )

    upscale_size = forms.ChoiceField(
        widget=forms.RadioSelect(attrs={"class": "form-check form-check-inline"}),
        choices=[(2, "x2"), (3, "x3"), (4, "x4")],
    )

    do_compress = forms.BooleanField(
        required=False,
        label="[Optional] Compress image size",
        widget=forms.CheckboxInput(attrs={"class": "custom-control-input"}),
    )

    compress_q_factor = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={"type": "range", "step": "1", "min": "30", "max": "95", "class": "form-control"}
        ),
        required=False,
    )


class EnhanceImagesForm(ModelForm):
    image_type = forms.ChoiceField(
        widget=forms.RadioSelect(attrs={"class": "form-check form-check-inline"}),
        choices=[("color", "RGB IMAGE"), ("color_real", "REAL WORLD RGB IMAGE"), ("greyscale", "GREYSCALE")],
    )

    quality_factor = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={"type": "range", "step": "1", "min": "30", "max": "90", "class": "form-control"}
        ),
        required=False,
    )

    class Meta:
        model = EnhancedImages
        fields = ["img_path", "image_type", "quality_factor"]
        labels = {
            "img_path": "",
            "image_type": "",
            "quality_factor": "",
        }


class FullEnhancementForm(EnhanceImagesForm, UpscaleImagesForm):
    ...

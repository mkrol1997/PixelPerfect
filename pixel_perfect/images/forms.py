from django import forms
from django.core.validators import FileExtensionValidator

from images.validators import ImageValidator


class UpscaleImagesForm(forms.Form):
    img_path = forms.ImageField(
        validators=[
            ImageValidator(size=3145728, width=2400, height=1440),
            FileExtensionValidator(["jpg", "jpeg", "png"]),
        ]
    )

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


class EnhanceImagesForm(forms.Form):
    img_path = forms.ImageField(
        validators=[
            ImageValidator(size=3145728, width=2400, height=1440),
            FileExtensionValidator(["jpg", "jpeg", "png"]),
        ]
    )

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

from collections.abc import Mapping

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class ImageValidator(object):
    messages = {
        "dimensions": _("Allowed dimensions are: %(width)s x %(height)s or %(height)s x %(width)s"),
        "size": _("Image must be no larger than 3Mb."),
    }

    def __init__(self, size=None, width=None, height=None, messages=None):
        self.size = size
        self.width = width
        self.height = height

        if messages is not None and isinstance(messages, Mapping):
            self.messages = messages

    def __call__(self, value):

        if self.size is not None and value.size > self.size:
            raise ValidationError(
                self.messages["size"],
                code="invalid_size",
                params={
                    "size": float(self.size) / 1024000,
                    "value": value,
                },
            )
        if (
            self.width is not None
            and self.height is not None
            and (value.width != self.width or value.height != self.height)
        ):
            raise ValidationError(
                self.messages["dimensions"],
                code="invalid_dimensions",
                params={
                    "width": self.width,
                    "height": self.height,
                    "value": value,
                },
            )

    def __eq__(self, other):
        print((other.size, other.width, other.height), flush=True)

        return (
            isinstance(other, self.__class__)
            and self.size == other.size
            and self.width == other.width
            and self.height == other.height
        )

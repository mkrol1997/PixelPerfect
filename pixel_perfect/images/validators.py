from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from django.utils.deconstruct import deconstructible


@deconstructible
class ImageValidator(object):
    def __init__(self, size=None, width=None, height=None, messages=None):
        self.size = size
        self.width = width
        self.height = height

    def __call__(self, image):
        width, height = get_image_dimensions(image)
        if image.size > self.size:
            raise ValidationError(
                message="",
                code="invalid_size",
                params={
                    "size": float(self.size) / 1024000,
                    "image": image,
                },
            )

        if width > height:  # landscape format
            if width > self.width or height > self.height:
                raise ValidationError(
                    message="",
                    code="invalid_dimensions",
                    params={"width": self.width, "height": self.height, "image": image},
                )
        if width < height:  # portrait format
            if height > self.width or width > self.height:
                raise ValidationError(
                    message="",
                    code="invalid_dimensions",
                    params={"width": self.width, "height": self.height, "image": image},
                )
        if height == width:  # square format
            if height > self.width or width > self.width:
                raise ValidationError(
                    message="",
                    code="invalid_dimensions",
                    params={"width": self.width, "height": self.height, "image": image},
                )

    def __eq__(self, other):
        return (
                isinstance(other, self.__class__)
                and self.size == other.size
                and self.width == other.width
                and self.height == other.height
        )

#
#
#
# from django.utils.translation import gettext_lazy as _
# from django.utils.deconstruct import deconstructible
#
#
# @deconstructible
# class ImageValidator(object):
#     messages = {
#         "dimensions": _(
#             'Allowed dimensions are: %(width)s x %(height)s.'
#         ),
#         "size": _(
#             "File is larger than > %(size)skB."
#         )
#     }
#
#     def __init__(self, size=None, width=None, height=None, messages=None):
#         self.size = size
#         self.width = width
#         self.height = height
#         if messages is not None and isinstance(messages, Mapping):
#             self.messages = messages
#
#     def __call__(self, value):
#
#         if self.size is not None and value.size > self.size:
#             raise ValidationError(
#                 self.messages['size'],
#                 code='invalid_size',
#                 params={
#                     'size': float(self.size)/1024,
#                     'value': value,
#                 }
#             )
#         if (self.width is not None and self.height is not None and
#                 (value.width != self.width or value.height != self.height)):
#             raise ValidationError(
#                 self.messages['dimensions'],
#                 code='invalid_dimensions',
#                 params={
#                     'width': self.width,
#                     'height': self.height,
#                     'value': value,
#                 }
#             )
#
#     def __eq__(self, other):
#         return (
#             isinstance(other, self.__class__) and
#             self.size == other.size and
#             self.width == other.width and
#             self.height == other.height
#         )

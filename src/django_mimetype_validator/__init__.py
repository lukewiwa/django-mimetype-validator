import magic
from django.core.exceptions import ValidationError
from django.core.files import File
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext as _


class MimeTypes:
    TEXT_PLAIN = "text/plain"
    TEXT_HTML = "text/html"
    TEXT_CSS = "text/css"
    TEXT_CSV = "text/csv"
    TEXT_JAVASCRIPT = "text/javascript"
    APPLICATION_OCTOCET_STREAM = "application/octet-stream"
    APPLICATION_CSV = "application/csv"
    APPLICATION_MSWORD = "application/msword"
    APPLICATION_GZIP = "application/gzip"
    IMAGE_APNG = "image/apng"
    IMAGE_AVIF = "image/avif"
    IMAGE_BMP = "image/bmp"
    IMAGE_GIF = "image/gif"
    IMAGE_PNG = "image/png"
    IMAGE_JPEG = "image/jpeg"
    IMAGE_SVG = "image/svg"
    IMAGE_WEBP = "image/webp"

    # Compatibility lists since magic doesn't always pick up
    # the specific type and often defaults to plain text
    TEXT_PLAIN_LIST = [TEXT_PLAIN]
    TEXT_HTML_LIST = [TEXT_HTML]
    TEXT_CSS_LIST = [TEXT_PLAIN, TEXT_CSS]
    TEXT_CSV_LIST = [TEXT_PLAIN, TEXT_CSV]
    TEXT_JAVASCRIPT_LIST = [
        TEXT_PLAIN,
        TEXT_JAVASCRIPT,
        # Lot's of historically acceptable MIME types that are deprecated
        "application/javascript",
        "application/ecmascript",
        "application/x-ecmascript",
        "application/x-javascript",
        "text/javascript",
        "text/ecmascript",
        "text/javascript1.0",
        "text/javascript1.1",
        "text/javascript1.2",
        "text/javascript1.3",
        "text/javascript1.4",
        "text/javascript1.5",
        "text/jscript",
        "text/livescript",
        "text/x-ecmascript",
        "text/x-javascript",
    ]
    AUDIO_WAVE_LIST = [
        "audio/wave",
        "audio/wav",
        "audio/x-wav",
        "audio/x-pn-wav",
    ]


@deconstructible
class MimeTypeFileValidator:
    """
    Use the `python-magic` library to validate file MIME types.

    Unashamedly used `django.core.validators.FileExtensionValidator` as
    inspiration for this validator implementation.
    """

    message = _(
        "File MIME type '%(mime_type)s' is not allowed. "
        "Allowed MIME types are: '%(allowed_mime_types)s'."
    )
    code = "invalid_mime_type"

    def __init__(self, allowed_mime_types=None, message=None, code=None):
        self.allowed_mime_types = allowed_mime_types
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code

    def __call__(self, value: File):
        # The file is already open so we'll grab just the part we need
        # to determine the MIME type
        buffer = next(value.chunks(1024))
        value.file.seek(0)
        mime_type = magic.from_buffer(buffer, mime=True)

        if (
            self.allowed_mime_types is not None
            and mime_type not in self.allowed_mime_types
        ):
            raise ValidationError(
                self.message,
                code=self.code,
                params={
                    "mime_type": mime_type,
                    "allowed_mime_types": ", ".join(self.allowed_mime_types),
                },
            )

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and self.allowed_mime_types == other.allowed_mime_types
            and self.message == other.message
            and self.code == other.code
        )

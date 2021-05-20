import pytest
from django.core.files import File

from src.django_mimetype_validator import MimeTypeFileValidator, MimeTypes


@pytest.mark.parametrize(
    "mime_type,test_file",
    (
        (MimeTypes.TEXT_PLAIN_LIST, (".txt", "Hello World!")),
        (MimeTypes.TEXT_HTML_LIST, (".html", "<!DOCTYPE html>\n<html></html>")),
        (MimeTypes.TEXT_CSS_LIST, (".css", ".hello {font-weight: 700;}\n")),
        (MimeTypes.TEXT_CSV_LIST, (".csv", "hello,world,there\n")),
        (MimeTypes.TEXT_JAVASCRIPT_LIST, (".js", "var hello = 'world';\n")),
    ),
    indirect=["test_file"],
)
def test_mimetype_validator_text_files(mime_type, test_file: File):
    validator = MimeTypeFileValidator(allowed_mime_types=mime_type)
    print(test_file.file.read())
    assert validator(test_file) is None

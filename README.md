# Django MIME Type Validator

[![tests](https://github.com/lukewiwa/django-mimetype-validator/actions/workflows/test.yaml/badge.svg)](https://github.com/lukewiwa/django-mimetype-validator/actions/workflows/test.yaml)

A django validator that uses the underlying libmagic library to guess at the mime type of imported files.

## Usage

Add this class to the `FileField` validators in Django models.

```python
from django.db import models

from django_mimetype_validator import MimeTypeFileValidator, MimeTypes


class FileModel(models.Model):

    csv_file = models.FileField(
        blank=False,
        validators=[
            MimeTypeFileValidator(
                allowed_mime_types=MimeTypes.TEXT_CSV_LIST,
        ],
    )
```

Due to the limitations of guessing at file types sometimes `libmagic` will default to `text/plain` if it cannot guess a suitable MIME type. In this case there is a few convenient lists that can be imported and used in the `MimeTypes` class to be generous in what the model will acccept. It's recommended that this is used in tandem with the build in [FileExtensionValidator](https://docs.djangoproject.com/en/3.2/ref/validators/#fileextensionvalidator).

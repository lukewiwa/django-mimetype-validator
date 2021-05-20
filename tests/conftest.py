from pathlib import Path

import pytest
from django.core.files import File


@pytest.fixture
def test_file(request):
    ext, contents = request.param
    FILE_LOCATION = Path(f"/tmp/test{ext}")
    FILE_LOCATION.touch()
    with open(FILE_LOCATION, "w") as f:
        f.write(contents)
    with open(FILE_LOCATION, "r") as f:
        yield File(f)
    FILE_LOCATION.unlink()

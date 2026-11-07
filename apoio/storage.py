from django.conf import settings
from django.core.files.storage import FileSystemStorage


def provas_storage() -> FileSystemStorage:
    return FileSystemStorage(location=settings.PROVAS_DIR, base_url=None)

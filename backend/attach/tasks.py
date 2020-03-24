from celery.decorators import task
from PIL import Image, UnidentifiedImageError
from io import BytesIO
from django.core.files import File

@task(bind=True)
def create_thumb(self, attachment):
    try:
        img = Image.open(attachment.upload)
        img.thumbnail((300, 300))
        buffer = BytesIO()
        img.save(buffer, img.format)
        attachment.thumbnail = File(buffer, name=f"thumb_{attachment.upload.name}")
        attachment.save()
    except UnidentifiedImageError:
        pass

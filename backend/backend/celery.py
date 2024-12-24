from celery import Celery
import os
from PIL import Image

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

app = Celery('backend')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

# @app.task
# def resize_image(image_path, output_path, size=(80, 80)):
#     try:
#         print("task go")
#         with Image.open(image_path) as img:
#             img.thumbnail(size)
#             img.save(output_path)
#         return True
#     except Exception as e:
#         print(f"Ошибка при обработке изображения: {e}")
#         return False
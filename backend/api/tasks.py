from celery import shared_task
from PIL import Image, ImageOps


@shared_task
def resize_image(image_path, output_path, size=(80, 80)):
    try:
        with Image.open(image_path) as img:
            img_cropped = ImageOps.fit(img, size, method=Image.Resampling.LANCZOS)
            img_cropped.thumbnail(size, Image.Resampling.LANCZOS)
            img_cropped.save(output_path, optimize=True, quality=95)
        return True
    except Exception as e:
        print(f"Ошибка при обработке изображения: {e}")
        return False
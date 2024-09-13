import base64
import os

import requests
from celery import shared_task
from django.conf import settings
from django.utils import timezone

from .models import GeneratedImage

engine_id = "stable-diffusion-xl-1024-v1-0"
api_host = "https://api.stability.ai"
api_key = settings.STABILITY_API_KEY

if api_key is None:
    raise Exception("Missing Stability API key.")

@shared_task
def generate_image(prompt):
    response = requests.post(
        f"{api_host}/v1/generation/{engine_id}/text-to-image",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}"
        },
        json={
            "text_prompts": [
                {
                    "text": prompt
                }
            ],
            "cfg_scale": 7,
            "height": 1024,
            "width": 1024,
            "samples": 1,
            "steps": 30,
        },
    )

    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    try:
        data = response.json()
    except ValueError as e:
        print("Failed to parse JSON response:", response.text)
        raise e

    output_dir = os.path.join(settings.MEDIA_ROOT, 'images')

    image_paths = []
    for i, image in enumerate(data.get("artifacts", [])):
        if image.get('finishReason') == 'SUCCESS':
            base64_image = image.get('base64')
            t = timezone.now()
            image_name = f"v1_txt2img_{t}_{i}.png"
            image_path = os.path.join(output_dir, image_name)
            image_content = base64.b64decode(base64_image)
            with open(image_path, 'wb') as f:
                f.write(image_content)
            image_paths.append(image_path)

    if image_paths:
        for image_path in image_paths:
            GeneratedImage.objects.create(prompt=prompt, image_path=image_path)
        return {"image_paths": image_paths}

    return {"error": "No successful image found"}
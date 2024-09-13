from rest_framework.response import Response
from rest_framework.views import APIView

from .tasks import generate_image


class GenerateImagesView(APIView):
    """
    View to generate images based on user prompts.

    Args:
        request (Request): The incoming request object.

    Returns:
        Response: A response containing a list of task IDs.
    """
    def post(self, request):
        
        prompts = request.data.get('prompts', [])
        results = []
        for prompt in prompts:
            result = generate_image.delay(prompt)
            results.append(result.id)
        return Response({"task_ids": results})

from django.http import JsonResponse
from django.views.generic import View
from .forms import UploadForm
from django.middleware.csrf import get_token
from django.utils.decorators import method_decorator

# Create your views here.
class UploadView(View):
    def get(self, request, *args, **kwargs):
        return JsonResponse({ "csrf": get_token(request) })
        
    def post(self, request, *args, **kwargs):
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            attachment = form.save_attachment()
            return JsonResponse({ "upload_token": attachment.upload_token })
        else:
            return JsonResponse({ "error": "Invalid file." }, status=400)
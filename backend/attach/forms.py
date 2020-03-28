from django import forms
from .models import Attachment
    
class UploadForm(forms.Form):
    attachment = forms.FileField(required=True)

    def save_attachment(self):
        files = self.files.getlist("attachment")
        return Attachment.objects.create(upload=files[0])


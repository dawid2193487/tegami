from django import forms
from attach.models import Attachment
    
class ResponseForm(forms.Form):
    message = forms.CharField(label="Message", max_length=6000, widget=forms.Textarea)
    attachments = forms.FileField(widget=forms.FileInput(attrs={'multiple': True}), required=False)

    def save_attachments(self, attached_to):
        files = self.files.getlist("attachments")
        for f in files:
            Attachment.objects.create(upload=f, content_object=attached_to)


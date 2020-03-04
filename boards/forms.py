from django import forms
from attach.models import Attachement
    
class ResponseForm(forms.Form):
    message = forms.CharField(label="Message", max_length=6000, widget=forms.Textarea)
    attachements = forms.FileField(widget=forms.FileInput(attrs={'multiple': True}), required=False)

    def save_attachements(self, attached_to):
        files = self.files.getlist("attachements")
        for f in files:
            Attachement.objects.create(upload=f, content_object=attached_to)


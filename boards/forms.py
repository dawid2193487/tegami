from django import forms
    
class ReplyForm(forms.Form):
    message = forms.CharField(label="Message", max_length=6000, widget=forms.Textarea)

class ThreadForm(forms.Form):
    message = forms.CharField(label="Message", max_length=6000, widget=forms.Textarea)
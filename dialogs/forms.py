from django import forms

# class AudioUploadForm(forms.Form):
#     audio_file = forms.FileField()

class TTSForm(forms.Form):
    text = forms.CharField(label='텍스트', max_length=100)
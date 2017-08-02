from django import forms
from .models import Question
from froala_editor.widgets import FroalaEditor
from ckeditor.widgets import CKEditorWidget
from django.contrib.flatpages.models import FlatPage

class QuestionCreateForm(forms.ModelForm):
    title = forms.CharField(
                    max_length=100,
                    widget=forms.TextInput(attrs={
                        'placeholder': 'Title of interview Question',
                    }),
                    required=False)
    description = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Question
        exclude = ('evaluation', 'rank', 'slug', 'superior')

class QnForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Question
        fields = ['evaluation', 'title', 'description', 'rank']


class FlatpageForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = FlatPage
        fields = '__all__'

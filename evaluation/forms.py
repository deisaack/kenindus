from django import forms
from .models import Question
from .models import Staff, File
# from django.conf import settings
# User = settings.AUTH_USER_MODEL
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()
from .models import validate_file


class FileForm(forms.ModelForm):
    file = forms.FileField(help_text='You May atach a file', validators=[validate_file], required=False)
    class Meta:
        model = File
        fields = ('file',)

class AppraisalForm(forms.ModelForm):
    increase = forms.DecimalField(max_value=1000000, min_value=0.00, required=False, label='Salary To Increase')
    decrease = forms.DecimalField(max_value=1000000, min_value=0.00, required=False, label='Salary To Reduce')
    superior = forms.ModelChoiceField(queryset=User.objects.all().filter(is_staff=True))
    user = forms.ModelChoiceField(widget=forms.HiddenInput, queryset=User.objects.all())
    recoment = forms.CharField(max_length=400, required=False)
    class Meta:
        model = Staff
        fields = ('user', 'position', 'superior', 'increase', 'decrease',)




class StaffCreateForm(forms.ModelForm):
    qs = User.objects.all()
    user = forms.ModelChoiceField(queryset=qs.filter(is_staff=False))
    superior = qs.filter(is_staff=True)
    class Meta:
        model = Staff
        fields = ('staff_no', 'user', 'position', 'salary', 'superior')


class AppraiseSalaryForm(forms.Form):
    amount = forms.DecimalField(help_text='Amount to add to sallary')

class AppraisePosition(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ('position',)

class AppraiseSuperior(forms.ModelForm):
    pass

class QuestionCreateForm(forms.ModelForm):
    class Meta:
        model = Question
        exclude = ('evaluation', 'rank', 'slug', 'superior')

class QnForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['evaluation', 'title', 'description', 'rank']

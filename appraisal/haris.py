from django import forms
from django.forms.formsets import BaseFormSet
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db import IntegrityError, transaction
from django.forms.formsets import formset_factory
from django.shortcuts import redirect, render
from .models import Question, Appraisal

class QuestionForm(forms.ModelForm):
    title = forms.CharField(
                    max_length=100,
                    widget=forms.TextInput(attrs={
                        'placeholder': 'Title of interview Question',
                    }),
                    required=False)
    description = forms.CharField(
                    widget=forms.TextInput(attrs={
                        'placeholder': 'describe the question',
                    }),
                    required=False)

    class Meta:
        model = Question
        fields = ['title', 'description', 'rank']


class AppraisalForm(forms.ModelForm):
    class Meta:
        model = Appraisal
        fields = ['employee', 'superior', 'total']


class BaseQuestionFormSet(BaseFormSet):
    def clean(self):
        if any(self.errors):
            return

        titles = []
        descriptions = []
        duplicates = False

        for form in self.forms:
            if form.cleaned_data:
                title = form.cleaned_data['title']
                description = form.cleaned_data['description']
                rank = form.cleaned_data['rank']

                # Check that no two questions have the same title or description
                if title and description:
                    if title in titles:
                        duplicates = True
                    titles.append(title)

                    if description in descriptions:
                        duplicates = True
                    descriptions.append(description)

                if duplicates:
                    raise forms.ValidationError(
                        'Questions must have unique titles and descriptions.',
                        code='duplicate_questions'
                    )

                # Check that all questions have both an title and description
                if description and not title:
                    raise forms.ValidationError(
                        'All questions must have an title.',
                        code='missing_title'
                    )
                elif title and not description:
                    raise forms.ValidationError(
                        'All questions must have a description.',
                        code='missing_description'
                    )





@login_required
def appraisal_creating(request):
    appraisal = Appraisal()
    QuestionFormSet = formset_factory(QuestionForm, formset=BaseQuestionFormSet)
    appraisal_questions = Question.objects.filter(active=True).order_by('title')
    question_data = [{'title': l.title, 'description': l.description}
                    for l in appraisal_questions]

    if request.method == 'POST':
        appraisal_form = AppraisalForm(request.POST) # whenever required
        question_formset = QuestionFormSet(request.POST)

        if appraisal_form.is_valid() and question_formset.is_valid():
            # Save user info
            appraisal.superior = appraisal_form.cleaned_data.get('superior')
            appraisal.employee = appraisal_form.cleaned_data.get('employee')
            appraisal.total = appraisal_form.cleaned_data.get('total')
            appraisal.save()

            # Now save the data for each form in the formset
            new_questions = []

            for question_form in question_formset:
                # appraisal = app
                title = question_form.cleaned_data.get('title')
                description = question_form.cleaned_data.get('description')
                rank = question_form.cleaned_data.get('rank')

                if title and description:
                    new_questions.append(Question(appraisal=appraisal, title=title, description=description, rank=rank))

            try:
                with transaction.atomic():
                    #Replace the old with the new
                    Question.objects.filter(appraisal=appraisal).delete()
                    Question.objects.bulk_create(new_questions)

                    # And notify our users that it worked
                    messages.success(request, 'You have updated the appraisal.')

            except IntegrityError: #If the transaction failed
                messages.error(request, 'There was an error saving your appraisal.')
                return redirect(reverse('appraisal_settings'))

    else:
        appraisal_form = AppraisalForm()
        question_formset = QuestionFormSet(initial=question_data)

    context = {
        'appraisal_form': appraisal_form,
        'question_formset': question_formset,
    }

    return render(request, 'appraisal/appraise.html', context)
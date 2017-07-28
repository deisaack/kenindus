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
        fields = ['appraisal', 'title', 'description', 'rank']


class AppraisalForm(forms.ModelForm):
    class Meta:
        model = Appraisal
        fields = ['employee', 'superior']


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
        appraisal_form = AppraisalForm(request.POST, appraisal) # whenever required
        question_formset = QuestionFormSet(request.POST)
        if not appraisal_form.is_valid():
            messages.error(request, 'There was an error in the appraisal form.')
            print(appraisal_form.cleaned_data)
        elif not question_formset.is_valid():
            messages.error(request, 'There was an error in the question_formset.')
            print(question_formset.cleaned_data)
        else:
            appraisal.superior = appraisal_form.cleaned_data.get('superior')
            appraisal.employee = appraisal_form.cleaned_data.get('employee')
            try:
                appraisal.save()
                messages.success(request, 'The appraisal was successfully saved.')
            except IntegrityError:
                messages.error(request, 'There appraisal encountered errors while being saved.')
                return redirect(reverse('appraisal:appraisal_list'))

            this_appraisal = appraisal

            # Now save the data for each form in the formset
            new_questions = []
            my_total = 0
            for question_form in question_formset:
                # = Question()
                appraisal = this_appraisal
                title = question_form.cleaned_data.get('title')
                description = question_form.cleaned_data.get('description')
                rank = question_form.cleaned_data.get('rank')
                if appraisal and title and description and rank:
                    question = Question(appraisal=appraisal, title=title, description=description, rank=rank)
                    question.save()
                    my_total += rank

                # if title and description:
                #     new_questions.append(Question(appraisal=appraisal, title=title, description=description, rank=rank))
            appraisal.total =my_total
            appraisal.save()
            # print(new_questions)
            # try:
            #     with transaction.atomic():
                #Replace the old with the new
                # Question.objects.bulk_create(new_questions)
                #
                # And notify our users that it worked
                # messages.success(request, 'You have updated the appraisal.')
            #
            # except IntegrityError: #If the transaction failed
            #     messages.error(request, 'There was an error saving your appraisal.')
            #     return redirect(reverse('appraisal:appraisal_list'))

    else:
        appraisal_form = AppraisalForm()
        question_formset = QuestionFormSet(initial=question_data)

    context = {
        'appraisal_form': appraisal_form,
        'question_formset': question_formset,
    }

    return render(request, 'appraisal/appraise.html', context)
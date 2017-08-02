from django import forms
from django.forms.formsets import BaseFormSet
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db import IntegrityError, transaction
from django.forms.formsets import formset_factory
from django.shortcuts import redirect, render
from .models import Question, Evaluation

class QuestionForm(forms.ModelForm):
    title = forms.CharField(
                    max_length=100,
                    widget=forms.TextInput(attrs={
                        'placeholder': 'Title of interview Question',
                    }),
                    required=True)
    description = forms.CharField(
                    widget=forms.TextInput(attrs={
                        'placeholder': 'describe the question',
                    }),
                    required=True)

    class Meta:
        model = Question
        fields = ['evaluation', 'title', 'description', 'rank']


class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = ['employee',]


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
def evaluation_creating(request):
    evaluation = Evaluation()
    QuestionFormSet = formset_factory(QuestionForm, formset=BaseQuestionFormSet)
    evaluation_questions = Question.objects.filter(active=True).order_by('title')
    question_data = [{'title': l.title, 'description': l.description}
                    for l in evaluation_questions]

    if request.method == 'POST':
        evaluation_form = EvaluationForm(request.POST, evaluation) # whenever required
        question_formset = QuestionFormSet(request.POST)
        if not evaluation_form.is_valid():
            messages.error(request, 'There was an error in the evaluation form.')
        elif not question_formset.is_valid():
            messages.error(request, 'There was an error in the question_formset.')
        else:
            evaluation.employee = evaluation_form.cleaned_data.get('employee')
            try:
                evaluation.save()
                messages.success(request, 'The evaluation was successfully saved.')
            except IntegrityError:
                messages.error(request, 'There evaluation encountered errors while being saved.')
                return redirect(reverse('evaluation:evaluation_list'))

            # this_evaluation = evaluation

            # Now save the data for each form in the formset
            new_questions = []
            my_total = 0
            for question_form in question_formset:
                # = Question()
                # evaluation = this_evaluation
                title = question_form.cleaned_data.get('title')
                description = question_form.cleaned_data.get('description')
                rank = question_form.cleaned_data.get('rank')
                superior = request.user
                if evaluation and title and description and rank:
                    question = Question(evaluation=evaluation, superior=superior, title=title, description=description, rank=rank)
                    question.save()
                    my_total += rank

                # if title and description:
                #     new_questions.append(Question(evaluation=evaluation, title=title, description=description, rank=rank))
            evaluation.total =my_total
            evaluation.save()
            qns = Question.objects.all().filter(evaluation=evaluation).count()
            my_total*=20
            evaluation.percentage = my_total/qns
            evaluation.save()
            # print('The questions here are { }', qns)
            # print(new_questions)
            # try:
            #     with transaction.atomic():
                #Replace the old with the new
                # Question.objects.bulk_create(new_questions)
                #
                # And notify our users that it worked
                # messages.success(request, 'You have updated the evaluation.')
            #
            # except IntegrityError: #If the transaction failed
            #     messages.error(request, 'There was an error saving your evaluation.')
            #     return redirect(reverse('evaluation:evaluation_list'))

    else:
        evaluation_form = EvaluationForm()
        question_formset = QuestionFormSet(initial=question_data)

    context = {
        'evaluation_form': evaluation_form,
        'question_formset': question_formset,
    }

    return render(request, 'evaluation/evaluate.html', context)
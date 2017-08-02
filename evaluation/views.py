from .models import Evaluation, Question
from django.views.generic import (
    DetailView, CreateView, DeleteView,
    UpdateView, FormView, ListView
)
from evaluation.forms import QuestionCreateForm
from django.core.urlresolvers import reverse, reverse_lazy
from .forms import QnForm
from django.urls import reverse
from django.http import HttpResponseForbidden
from django.views.generic import FormView
from django.contrib import messages
from django.views import View
from evaluation.templatetags.my_data_filters import mul, div
from django.contrib.flatpages.models import FlatPage
from .forms import FlatpageForm


class FlatpageCreateView(CreateView):
    model = FlatPage
    form_class = FlatpageForm
    template_name = 'evaluation/flatpage_form.html'
    success_url = reverse_lazy('django.contrib.flatpages.views.flatpage')

    def get_success_url(self):
        return reverse('django.contrib.flatpages.views.flatpage', kwargs={'url': self.object.url})

class FormMessageMixin(object):
    @property
    def form_valid_message(self):
        return NotImplemented

    form_invalid_message = 'Please correct the errors below.'

    def form_valid(self, form):
        messages.success(self.request, self.form_valid_message)
        return super(FormMessageMixin, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, self.form_invalid_message)
        return super(FormMessageMixin, self).form_invalid(form)
#
#
# class DocumentCreateView(FormMessageMixin, CreateView):
#     model = Document
#     fields = ('name', 'file')
#     success_url = reverse_lazy('documents')
#     form_valid_message = 'The document was successfully created!'

class EvaluationDetilView(DetailView):
    model = Evaluation

    def get_context_data(self, **kwargs):
        context = super(EvaluationDetilView, self).get_context_data(**kwargs)
        p = Evaluation.objects.filter(slug=self.kwargs['slug'])
        pk = p.first().id
        qns = Question.objects.filter(evaluation=pk).count()
        qns *= 5
        total = p.first().total
        if total==0 or  qns==0:
            score = 0.0000001
        else:
            score = total/qns
        context['score'] = '%.2f' % score
        context['question_list'] = Question.objects.filter(evaluation=pk)
        return context


class EvaluationDisplay(DetailView):
    model = Evaluation
    template_name = 'evaluation/evaluation_detail.html'


    def get_context_data(self, **kwargs):
        context = super(EvaluationDisplay, self).get_context_data(**kwargs)
        p = Evaluation.objects.filter(slug=self.kwargs['slug'])
        pk = p.first().id
        qns = Question.objects.filter(evaluation=pk).count()
        qns *= 5
        total = p.first().total
        if total==0 or  qns==0:
            score = 0.0000001
        else:
            score = total/qns
        context['score'] = '%.2f' % score
        context['question_list'] = Question.objects.filter(evaluation=pk)
        context['form'] = QnForm()
        return context


class EvaluationImproveFormView(FormMessageMixin, FormView):
    template_name = 'evaluation/evaluation_detail.html'
    form_class = QnForm
    form_valid_message = 'The document was successfully updated!'
    form_invalid_message = 'There are some errors in the form below.'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        rank = form.cleaned_data.get('rank')
        self.object.superior = self.request.user
        self.object.evaluation.total += int(rank)
        self.object.evaluation.save()
        self.object.save()
        this_eval = form.cleaned_data.get('evaluation')
        this_percentage = this_eval.percentage
        this_total = this_eval.total
        new_total = this_total
        pk = this_eval.pk
        qns = Question.objects.all().filter(evaluation=pk).count()
        new_percentage = (new_total*20)/qns
        self.object.evaluation.percentage = new_percentage
        self.object.evaluation.save()
        # print('The evalluations total is %r, and it\'s percentage is %r but we should update to %r because of \n'
        #       '%d questions' % (this_total, this_percentage, new_percentage, qns))
        return super(EvaluationImproveFormView, self).form_valid(form)

    def get_success_url(self):
        return reverse('evaluation:evaluation_detail', kwargs={'slug': self.object.evaluation.slug})


class EvaluationImproveDetail(View):

    def get(self, request, *args, **kwargs):
        view = EvaluationDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = EvaluationImproveFormView.as_view()
        return view(request, *args, **kwargs)

class QuestionDetilView(DetailView):
    model = Question

class QuestionList(ListView):
    model = Question
    queryset = Question.objects.all().filter(evaluation=None)

class QuestionCreateView(CreateView):
    model = Question
    form_class = QuestionCreateForm

class QuestionUpdateView(UpdateView):
    model = Question
    form_class = QuestionCreateForm

class EvaluationList(ListView):
    model = Evaluation
    queryset = Evaluation.objects.all()



# class EvaluationImproveFormView(SingleObjectMixin, FormView):
#     template_name = 'evaluation/evaluation_detail.html'
#     form_class = QnForm
#     model = Question
#     success_url = reverse_lazy('evaluation_list')
#
#     def post(self, request, *args, **kwargs):
#         if not request.user.is_authenticated:
#             return HttpResponseForbidden()
#         self.object = self.get_object()
#         print(self.object)
#         print('=='*30)
#         self.object.save()
#         return super(EvaluationImproveFormView, self).post(request, *args, **kwargs)




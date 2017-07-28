from .models import Appraisal, Question
from django.views.generic import (
    DetailView, CreateView, DeleteView,
    UpdateView, FormView, ListView
)
from appraisal.forms import QuestionCreateForm
from django.core.urlresolvers import reverse, reverse_lazy
from .forms import QnForm
from django.urls import reverse
from django.http import HttpResponseForbidden
from django.views.generic import FormView
from django.contrib import messages
from django.views import View
from appraisal.templatetags.my_data_filters import mul, div
from django.contrib.flatpages.models import FlatPage
from .forms import FlatpageForm


class FlatpageCreateView(CreateView):
    model = FlatPage
    form_class = FlatpageForm
    template_name = 'appraisal/flatpage_form.html'
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

class AppraisalDetilView(DetailView):
    model = Appraisal

    def get_context_data(self, **kwargs):
        context = super(AppraisalDetilView, self).get_context_data(**kwargs)
        p = Appraisal.objects.filter(slug=self.kwargs['slug'])
        pk = p.first().id
        qns = Question.objects.filter(appraisal=pk).count()
        qns *= 5
        total = p.first().total
        score = total/qns
        context['score'] = '%.2f' % score
        context['question_list'] = Question.objects.filter(appraisal=pk)
        return context


class AppraisalDisplay(DetailView):
    model = Appraisal
    template_name = 'appraisal/appraisal_detail.html'


    def get_context_data(self, **kwargs):
        context = super(AppraisalDisplay, self).get_context_data(**kwargs)
        p = Appraisal.objects.filter(slug=self.kwargs['slug'])
        pk = p.first().id
        qns = Question.objects.filter(appraisal=pk).count()
        qns *= 5
        total = p.first().total
        score = total/qns
        context['score'] = '%.2f' % score
        context['question_list'] = Question.objects.filter(appraisal=pk)
        context['form'] = QnForm()
        return context


class AppraisalImproveFormView(FormMessageMixin, FormView):
    template_name = 'appraisal/appraisal_detail.html'
    form_class = QnForm
    form_valid_message = 'The document was successfully updated!'
    form_invalid_message = 'There are some errors in the form below.'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        rank = form.cleaned_data.get('rank')
        self.object.appraisal.total += int(rank)
        self.object.appraisal.save()
        self.object.save()
        return super(AppraisalImproveFormView, self).form_valid(form)

    def get_success_url(self):
        return reverse('appraisal:appraisal_detail', kwargs={'slug': self.object.appraisal.slug})


class AppraisalImproveDetail(View):

    def get(self, request, *args, **kwargs):
        view = AppraisalDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = AppraisalImproveFormView.as_view()
        return view(request, *args, **kwargs)

class QuestionDetilView(DetailView):
    model = Question

class QuestionList(ListView):
    model = Question
    queryset = Question.objects.all().filter(appraisal=None)

class QuestionCreateView(CreateView):
    model = Question
    form_class = QuestionCreateForm

class QuestionUpdateView(UpdateView):
    model = Question
    form_class = QuestionCreateForm

class AppraisalList(ListView):
    model = Appraisal
    queryset = Appraisal.objects.all()



# class AppraisalImproveFormView(SingleObjectMixin, FormView):
#     template_name = 'appraisal/appraisal_detail.html'
#     form_class = QnForm
#     model = Question
#     success_url = reverse_lazy('appraisal_list')
#
#     def post(self, request, *args, **kwargs):
#         if not request.user.is_authenticated:
#             return HttpResponseForbidden()
#         self.object = self.get_object()
#         print(self.object)
#         print('=='*30)
#         self.object.save()
#         return super(AppraisalImproveFormView, self).post(request, *args, **kwargs)




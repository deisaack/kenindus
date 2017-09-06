from evaluation.models import Evaluation, Question, Appraisal, Staff, File
from django.views.generic import (
    DetailView, CreateView, TemplateView,
    UpdateView, ListView
)
from evaluation.forms import QuestionCreateForm
from evaluation.forms import QnForm, StaffCreateForm, AppraisalForm
from django.urls import reverse
from django.views.generic import FormView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.views import View

User = get_user_model()

class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        qs = Evaluation.objects.all()
        labels =[]
        default_items = []
        for e in qs:
            labels.append(e.staff.user.username)
            default_items.append(e.percentage)
        data = {
            'labels': labels,
            'default': default_items,
        }
        return Response(data)

class ChartView(TemplateView):
    template_name = 'evaluation/charts.html'


class StaffCreateView(SuccessMessageMixin, CreateView):
    model = Staff
    form_class = StaffCreateForm
    success_message = 'The staff was successfully created'
    success_url = '/'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.creator = self.request.user
        self.object.user.is_staff = True
        self.object.save()
        self.object.user.save()
        return super(StaffCreateView, self).form_valid(form)


class ApraisalCreateView(SuccessMessageMixin, UpdateView):
    model = Staff
    form_class = AppraisalForm
    slug_field = 'staff_no'
    slug_url_kwarg = 'staff_no'
    template_name = 'evaluation/appraisal_form.html'
    success_message = 'The appraisal was successfull'


    def form_valid(self, form):
        self.object = form.save(commit=False)
        increase = form.cleaned_data.get('increase')
        decrease = form.cleaned_data.get('decrease')
        recoment = form.cleaned_data.get('recoment')
        file = form.cleaned_data.get('file')
        print(file)
        qs = Staff.objects.filter(staff_no=self.kwargs.get('staff_no')).first()
        evaluation = Evaluation.objects.filter(staff=qs).order_by('-id').first().pk
        if self.object.position != qs.position:
            detail = ('Changed position from %s to %s' % (qs.position,  self.object.position))
            Appraisal.objects.create(evaluation_id=evaluation, superior=self.request.user, detail=detail)
        if self.object.superior != qs.superior:
            detail = ('Changed superior from %s to %s' % (qs.superior,  self.object.superior))
            Appraisal.objects.create(evaluation_id=evaluation, superior=self.request.user, detail=detail)
        if increase:
            salary = self.object.salary
            new_salary = salary + increase
            self.object.salary = new_salary
            detail = ('Increased salary from %s to %s' % (salary, new_salary))
            Appraisal.objects.create(evaluation_id=evaluation, superior=self.request.user, detail=detail)
        if decrease:
            salary = self.object.salary
            new_salary = salary - decrease
            self.object.salary = new_salary
            detail = ('Reduced salary from %s to %s' % (salary, new_salary))
            Appraisal.objects.create(evaluation_id=evaluation, superior=self.request.user, detail=detail)
        if recoment:
            detail = ('Given recomendation to:- %s' % recoment)
            Appraisal.objects.create(evaluation_id=evaluation, superior=self.request.user, detail=detail)
        if file:
            print('a file exists')
            File.objects.create(evaluation_id=evaluation, superior=self.request.user, file=file)

        self.object.save()
        # try:
        #     send_text("+254721732519", "Helo isaac at offline")
        # except Exception as e:
        #     messages.error(self.request, 'Message not sent')

        # current_site = get_current_site(self.request)
        # message = render_to_string('evaluation/emails/apraisal_done.html', {
        #     'user'  : qs.user,
        #     'domain': current_site.domain,
        #     'details'   : email_content,
        # })
        # mail_subject = 'My Appraisal'
        # to_email = qs.user.email
        # email = EmailMessage(mail_subject, message, to=[to_email])
        # email.send()
        return super(ApraisalCreateView, self).form_valid(form)


class StaffListView(ListView):
    model = Staff


class StaffDetailView(DetailView):
    model = Staff
    slug_field = 'staff_no'
    slug_url_kwarg = 'staff_no'

    def get_context_data(self, **kwargs):
        context = super(StaffDetailView, self).get_context_data(**kwargs)
        p = Staff.objects.all().filter(staff_no=self.kwargs.get('staff_no'))
        pk = p.first().id
        context['evaluation_list'] = Evaluation.objects.all().filter(staff=pk).order_by('-updated')
        return context


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
        evaluation = Evaluation.objects.filter(staff=self.object.staff).order_by('-id').first().pk
        if evaluation == self.object.pk:
            context['last'] = True
        p = Evaluation.objects.filter(slug=self.kwargs['slug'])
        pk = p.first().id
        context['appraisal_list'] = Appraisal.objects.all().filter(evaluation=pk)
        context['question_list'] = Question.objects.filter(evaluation=pk)
        context['file_list'] = File.objects.all().filter(evaluation=pk)
        if context['question_list']:
            data = []
            labels = []
            for question in context['question_list']:
                labels.append(question.title)
                data.append(question.rank)
            context['chart_labels'] = labels
            context['chart_data'] = data
        return context


class EvaluationDisplay(EvaluationDetilView):
    def get_context_data(self, **kwargs):
        context = super(EvaluationDisplay, self).get_context_data(**kwargs)
        context['form'] = QnForm()
        return context

class EvaluationImproveFormView(SuccessMessageMixin, FormView):
    template_name = 'evaluation/evaluation_detail.html'
    form_class = QnForm
    form_valid_message = 'The document was successfully updated!'
    form_invalid_message = 'There are some errors in the form below.'
    success_message = 'The evaluation update was successful'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        rank = form.cleaned_data.get('rank')
        self.object.superior = self.request.user
        self.object.evaluation.total += int(rank)
        self.object.evaluation.save()
        self.object.save()
        this_eval = form.cleaned_data.get('evaluation')
        this_total = this_eval.total
        new_total = this_total
        pk = this_eval.pk
        qns = Question.objects.all().filter(evaluation=pk).count()
        new_percentage = (new_total*20)/qns
        self.object.evaluation.percentage = new_percentage
        self.object.evaluation.save()
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


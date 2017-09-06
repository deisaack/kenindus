from evaluation.forms import FileForm
from evaluation.models import File
from django.http import JsonResponse
from django.views import View
import time
from django.shortcuts import render, redirect
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import UpdateView
from evaluation.models import Staff, Evaluation

class BasicUploadView(View):
    def get(self, request):
        files_list = File.objects.all()
        return render(self.request, 'files/basic_upload/index.html', {'files': files_list})

    def post(self, request):
        form = FileForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            file = form.save()
            data = {'is_valid': True, 'name': file.file.name, 'url': file.file.url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)

class ApraisalFileView(SuccessMessageMixin, UpdateView):
    model = Staff
    slug_field = 'staff_no'
    slug_url_kwarg = 'staff_no'
    template_name = 'evaluation/appraisal_form.html'
    success_message = 'The appraisal was successfull'
    fields = ('salary',)

    def get_context_data(self, **kwargs):
        context = super(ApraisalFileView, self).get_context_data(**kwargs)
        context['files'] = File.objects.all()
        return context

    def post(self, request, *args, **kwargs):
    # def post(self, request):
        time.sleep(1)  # You don't need this line. This is just to delay the process so you can see the progress bar testing locally.
        form = FileForm(self.request.POST, self.request.FILES)

        if form.is_valid():
            self.object = form.save(commit=False)
            qs = Staff.objects.filter(staff_no=self.kwargs.get('staff_no')).first()
            evaluation = Evaluation.objects.filter(staff=qs).order_by('-id').first().pk
            print(evaluation)
            self.object.superior = self.request.user
            self.object.evaluation_id = evaluation
            self.object.save()
            file = self.object
            data = {'is_valid': True, 'name': file.file.name, 'url': file.file.url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)
    
    # def form_valid(self, form):
    #     self.object = form.save(commit=False)
    #     qs = Staff.objects.filter(staff_no=self.kwargs.get('staff_no')).first()
    #     evaluation = Evaluation.objects.filter(staff=qs).order_by('-id').first().pk
    #     print(evaluation)
    #     self.object.superior = self.request.user
    #     self.object.evaluation = evaluation
    #     self.object.save()
    #     return super(ApraisalFileView, self).form_valid(form)

class ProgressBarUploadView(View):
    def get(self, request):
        files_list = File.objects.all()
        return render(self.request, 'files/progress_bar_upload/index.html', {'files': files_list})

    def post(self, request):
        time.sleep(1)  # You don't need this line. This is just to delay the process so you can see the progress bar testing locally.
        form = FileForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            file = form.save()
            data = {'is_valid': True, 'name': file.file.name, 'url': file.file.url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)


class DragAndDropUploadView(View):
    def get(self, request):
        files_list = File.objects.all()
        return render(self.request, 'files/drag_and_drop_upload/index.html', {'files': files_list})

    def post(self, request):
        form = FileForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            file = form.save()
            data = {'is_valid': True, 'name': file.file.name, 'url': file.file.url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)


def clear_database(request):
    for file in File.objects.all():
        file.file.delete()
        file.delete()
    return redirect(request.POST.get('next'))


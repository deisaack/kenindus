from evaluation.forms import FileForm
from evaluation.models import File
from django.http import JsonResponse
from django.views import View
import time
from django.shortcuts import render, redirect


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


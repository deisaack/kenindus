from .models import Appraisal, Question
from django.views.generic import (
    DetailView, CreateView, DeleteView,
    UpdateView, FormView, ListView
)

class QuestionDetilView(DetailView):
    model = Question

class QuestionList(ListView):
    model = Question
    queryset = Question.objects.all().filter(active=True)

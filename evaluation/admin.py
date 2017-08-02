from django.contrib import admin

# Register your models here.

from .models import (
	Question,
	Evaluation,
)


class QuestionInline(admin.TabularInline):
	model = Question
	extra = 0


class EvaluationAdmin(admin.ModelAdmin):
	inlines = [
		QuestionInline
	]

	class Meta:
		model = Evaluation


admin.site.register(Evaluation, EvaluationAdmin)

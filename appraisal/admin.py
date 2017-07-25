from django.contrib import admin

# Register your models here.

from .models import (
	Question,
	Appraisal,
)


class QuestionInline(admin.TabularInline):
	model = Question
	extra = 0


class AppraisalAdmin(admin.ModelAdmin):
	inlines = [
		QuestionInline
	]

	class Meta:
		model = Appraisal


admin.site.register(Appraisal, AppraisalAdmin)

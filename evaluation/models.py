from django.db import models
from django.conf import settings
from django.contrib import admin
from django.urls import reverse
User = settings.AUTH_USER_MODEL
from django.db.models.signals import pre_save
from django.utils.text import slugify
from autoslug import AutoSlugField


class Position(models.Model):
	title = models.CharField(max_length=100)
	description = models.TextField(default='')

	def __str__(self):
		return self.title

admin.site.register(Position)

class Question(models.Model):
	evaluation = models.ForeignKey('Evaluation', on_delete=models.CASCADE, null=True, blank=True, related_name='+')
	title = models.CharField(max_length=300)
	slug = models.SlugField(null=True, blank=True)
	description = models.CharField(max_length=3000, default='')
	ONE = 1
	TWO = 2
	THREE = 3
	FOUR = 4
	FIVE = 5
	RANK = (
		(ONE, 1),
		(TWO, 2),
		(THREE, 3),
		(FOUR, 4),
		(FIVE, 5),
	)
	rank = models.SmallIntegerField(choices=RANK, null=True, blank=True)
	active = models.BooleanField(default=False)
	date = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	superior = models.ForeignKey(User, on_delete=models.PROTECT, related_name='+', null=True, blank=True)


	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('evaluation:question_detail', kwargs={'slug': self.slug})


admin.site.register(Question)

class Evaluation(models.Model):
	employee = models.ForeignKey('Employee', on_delete=models.PROTECT, related_name='+')
	slug = models.SlugField(unique=True, null=True, blank=True)
	total = models.PositiveIntegerField(default=0)
	percentage = models.DecimalField(max_digits=4, decimal_places=2, default=0)
	complete = models.BooleanField(default=False)
	date = models.DateField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.employee.user.username + ' ' + self.employee.user.email


	def get_absolute_url(self):
		return reverse('evaluation:evaluation_detail', kwargs={'slug': self.slug})




class Employee(models.Model):
	employee_no = models.CharField(max_length=30, null=True, blank=True)
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
	superior = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name='my_superior')
	position = models.ForeignKey('Position', on_delete=models.PROTECT, null=True, blank=True)

	def __str__(self):
		return self.employee_no

admin.site.register(Employee)

class Appraisal(models.Model):
	evaluation = models.ForeignKey(Evaluation, null=True, blank=True)
	details = models.TextField


admin.site.register(Appraisal)


def create_evaluation_slug(instance, new_slug=None):
	slug = slugify(instance.employee_id)
	if new_slug is not None:
		slug = new_slug
	qs = Evaluation.objects.filter(slug=slug).order_by('-id')
	exists = qs.exists()
	if exists:
		from random import randint
		x = randint(0, 100)
		slug = '%s-%s-%s' % (slug, qs.first().id, x)
		return create_evaluation_slug(instance, new_slug=slug)
	return slug

def pre_save_evaluation_receier(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = create_evaluation_slug(instance)



pre_save.connect(pre_save_evaluation_receier, sender=Evaluation)

def create_qn_slug(instance, new_slug=None):
	slug = slugify(instance.title)
	if new_slug is not None:
		slug = new_slug
	qs = Question.objects.filter(slug=slug).order_by('-id')
	exists = qs.exists()
	if exists:
		from random import randint
		x = randint(0, 100)
		slug = '%s-%s-%s' % (slug, qs.first().id, x)
		return create_qn_slug(instance, new_slug=slug)
	return slug

def pre_save_question_receier(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = create_qn_slug(instance)

pre_save.connect(pre_save_question_receier, sender=Question)


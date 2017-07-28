from django.db import models
from django.conf import settings
from django.contrib import admin
from django.urls import reverse
User = settings.AUTH_USER_MODEL
from django.db.models.signals import pre_save
from django.utils.text import slugify
from autoslug import AutoSlugField


class Question(models.Model):
	appraisal = models.ForeignKey('Appraisal', on_delete=models.CASCADE, null=True, blank=True, related_name='+')
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

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('appraisal:question_detail', kwargs={'slug': self.slug})


admin.site.register(Question)

class Appraisal(models.Model):
	employee = models.ForeignKey('Employee', on_delete=models.PROTECT, related_name='+')
	superior = models.ForeignKey('Employee', on_delete=models.PROTECT, related_name='+')
	slug = models.SlugField(unique=True, null=True, blank=True)
	total = models.PositiveIntegerField(default=0)
	date = models.DateField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.employee.user.username + ' ' + self.employee.user.email


	def get_absolute_url(self):
		return reverse('appraisal:appraisal_detail', kwargs={'slug': self.slug})




class Employee(models.Model):
	employee_id = models.CharField(max_length=30, null=True, blank=True)
	user = models.OneToOneField(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.employee_id

admin.site.register(Employee)


class Review(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	QUESTION_CHOICES =	(0 , 'N/A'),(1 , 'Strongly Disagree'), (2 , 'Disagree'), (3 , 'Neutral'),(4 , 'Agree'),	(5 , 'Strongly Agree')
	INSTRUCTION_CHOICES = (0 , 'N/A'),\
	                      (1, 'Rarely Achieves Expectations '),\
	                      (2, 'Sometimes Achieves Expectations'), \
	                      (3, 'Fully Achieves Expectations'), \
	                      (4, 'Fully Achieves and Occasionally Exceeds Expectations	'), \
	                      (5, 'Consistently Exceeds Expectations')
	q1 = models.IntegerField('Is the user competent in what he/she does?',choices=QUESTION_CHOICES, default=0)
	q2 = models.IntegerField('Accomplishments - the extent to which the employee meets expectations in performing the job '
	                         'functions of his/her position as defined in documentation such as the PDQ. ',
	                         choices=INSTRUCTION_CHOICES, default=0)
	q3 = models.IntegerField('Service & Relationships - the extent to which the employee\'s behaviors are directed '
	                         'toward fostering positive working relationships in a diverse workplace, respect for one\'s'
	                         ' fellow workers, and cooperation with students, customers, and visitors. ',
	                         choices=INSTRUCTION_CHOICES, default=0)
	q4 = models.IntegerField('Accountability & Dependability - the extent to which the employee contributes to the '
	                         'effectiveness of the department and the overall mission of the University. ',
	                         choices=INSTRUCTION_CHOICES, default=0)
	q5 = models.IntegerField('Adaptability & Flexibility - the extent to which the employee exhibits openness to new'
	                         ' ideas, programs, systems, and/or structures. ',
	                         choices=INSTRUCTION_CHOICES, default=0)
	q6 = models.IntegerField('Decision Making & Problem Solving - the extent to which the employee makes sound and '
	                         'logical job-related decisions that are in the best interest of the company ',
	                         choices=INSTRUCTION_CHOICES, default=0)
	q7 = models.IntegerField('Atendance and Punctuality to work ', choices=QUESTION_CHOICES, default=0)
	q8 = models.IntegerField('Customer service ', choices=QUESTION_CHOICES, default=0)
	q9 = models.IntegerField('Planning and organization of work ', choices=QUESTION_CHOICES, default=0)
	# q13 = models.IntegerField(' ', choices=INSTRUCTION_CHOICES, default=0)

	date = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)
	superior_comment = models.TextField(default='')
	hr_comment = models.TextField(default='')
	total = models.IntegerField(default='0')

def create_appraisal_slug(instance, new_slug=None):
	slug = slugify(instance.employee_id)
	if new_slug is not None:
		slug = new_slug
	qs = Appraisal.objects.filter(slug=slug).order_by('-id')
	exists = qs.exists()
	if exists:
		from random import randint
		x = randint(0, 100)
		slug = '%s-%s-%s' % (slug, qs.first().id, x)
		return create_appraisal_slug(instance, new_slug=slug)
	return slug

def pre_save_appraisal_receier(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = create_appraisal_slug(instance)



pre_save.connect(pre_save_appraisal_receier, sender=Appraisal)

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


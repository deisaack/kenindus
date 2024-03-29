from django.db import models
from django.conf import settings
from django.contrib import admin
from django.urls import reverse
User = settings.AUTH_USER_MODEL
from django.db.models.signals import pre_save
from django.utils.text import slugify
from .validators import FileValidator

validate_file = FileValidator(min_size= 1024 * 1, max_size=1024 * 5000, content_types=('application/pdf',))


class Position(models.Model):
	title = models.CharField(max_length=100)
	description = models.TextField(default='')

	def __str__(self):
		return self.title

admin.site.register(Position)


class Question(models.Model):
	evaluation = models.ForeignKey('Evaluation', on_delete=models.CASCADE, null=True, blank=True, related_name='+')
	title = models.CharField(max_length=300)
	slug = models.SlugField(null=True, blank=True, editable=False)
	description = models.CharField(max_length=3000, default='')
	ONE = 1
	TWO = 2
	THREE = 3
	FOUR = 4
	FIVE = 5
	RANK = (
		(ONE, ONE),
		(TWO, TWO),
		(THREE, THREE),
		(FOUR, FOUR),
		(FIVE, FIVE),
	)
	rank = models.SmallIntegerField(choices=RANK, null=True, blank=True)
	active = models.BooleanField(default=False)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	superior = models.ForeignKey(User, on_delete=models.PROTECT, related_name='+', null=True, blank=True)


	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('evaluation:question_detail', kwargs={'slug': self.slug})


admin.site.register(Question)

class Evaluation(models.Model):
	staff = models.ForeignKey('Staff', on_delete=models.PROTECT, related_name='+')
	slug = models.SlugField(unique=True, null=True, blank=True)
	total = models.PositiveIntegerField(default=0)
	percentage = models.DecimalField(max_digits=4, decimal_places=2, default=0)
	complete = models.BooleanField(default=False)
	created = models.DateField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.staff.user.username + ' ' + self.staff.user.email

	def get_absolute_url(self):
		return reverse('evaluation:evaluation_detail', kwargs={'slug': self.slug})


class Staff(models.Model):
	staff_no = models.CharField(max_length=30, null=True, blank=True, unique=True)
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
	superior = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name='my_superior')
	position = models.ForeignKey('Position', on_delete=models.PROTECT, null=True, blank=True)
	creator = models.ForeignKey(User, null=True, blank=True, related_name='+')

	def __str__(self):
		return self.staff_no

	def get_absolute_url(self):
		return reverse('evaluation:staff_detail', kwargs={'staff_no': self.staff_no})

admin.site.register(Staff)

import os
def update_filename(instance, filename):
    path = "upload/appraisals/"
    format = str(instance.evaluation_id) + instance.detail[:10] + '.pdf'
    return os.path.join(path, format)

def upload_location(instance, filename):
    path = "upload/appraisals/files/"
    format = str(instance.evaluation_id) + instance.superior.username[:10] + '.pdf'
    return os.path.join(path, format)

class File(models.Model):
	evaluation = models.ForeignKey(Evaluation, null=True, blank=True)
	file = models.FileField('Atach a File', upload_to=upload_location)
	superior = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
	date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		try:
			info = str(self.file).strip().split('/').pop()

			return info
		except:
			return str(self.file.url)

admin.site.register(File)

class Appraisal(models.Model):
	evaluation = models.ForeignKey(Evaluation, null=True, blank=True)
	detail = models.TextField(default='')
	superior = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
	date = models.DateTimeField(auto_now_add=True)
	# file = models.FileField('Atach a File', upload_to=update_filename, null=True, blank=True, validators=[validate_file])

	def __str__(self):
		return self.detail[:50]

admin.site.register(Appraisal)


def create_evaluation_slug(instance, new_slug=None):
	slug = slugify(instance.staff_id)
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

from django.db import models
from django.conf import settings
from django.contrib import admin

User = settings.AUTH_USER_MODEL


class Question(models.Model):
	appraisal = models.ForeignKey('Appraisal', on_delete=models.CASCADE, null=True, blank=True, related_name='+')
	title = models.CharField(max_length=300)
	description = models.CharField(max_length=300, default='')
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

	def __str__(self):
		return self.title
admin.site.register(Question)

class Appraisal(models.Model):
	employee = models.ForeignKey('Employee', on_delete=models.CASCADE, related_name='+')
	superior = models.ForeignKey('Superior', on_delete=models.CASCADE, related_name='+')
	total = models.PositiveIntegerField()
	created = models.DateField(auto_now_add=True, auto_now=False)

	def __str__(self):
		return self.employee.user.username + ' ' + self.employee.user.email


class Employee(models.Model):
	employee_id = models.CharField(max_length=30, null=True, blank=True)
	user = models.OneToOneField(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.employee_id

admin.site.register(Employee)


class EmployeeReview(models.Model):
	user = models.ManyToManyField(User)
	superior = models.ForeignKey('Superior')
	employee = models.ManyToManyField(Employee)
	total = models.PositiveIntegerField(default=0)
	date = models.DateTimeField(auto_now=False, auto_now_add=True)

	def __str__(self):
		return ('%s %s' % (self.user.username, self.date))

class Superior(models.Model):
	department = models.OneToOneField(Employee)

admin.site.register(Superior)


class Review(models.Model):
	superior = models.ForeignKey(Superior, null=True, blank=True)
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

	def __str__(self):
		return ('%s %s' % (self.user.username, self.date.date()))

admin.site.register(Review)


class Category(models.Model):
	name = models.CharField(max_length=30)
	user = models.ForeignKey(User, on_delete=models.CASCADE)

class Product(models.Model):
	name = models.CharField(max_length=30)
	price = models.DecimalField(decimal_places=2, max_digits=10)
	category = models.ForeignKey(Category)
	user = models.ForeignKey(User, on_delete=models.CASCADE)


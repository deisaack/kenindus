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
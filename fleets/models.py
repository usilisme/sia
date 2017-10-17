# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import (
	Model,
	CharField,
)

# Create your models here.
class Airplane (Model):
	CHOICES_MODEL = (
		('A330-300','Airbus A330-300'),
		('A380-800','Airbus A380-800'),
		('777-300ER','Boeing 777-300ER'),
		('B772','Boeing 777-200'),
	)

	Model = CharField(
		max_length = 100,
		blank = True, null = True,
		choices = CHOICES_MODEL
	)

	@property
	def Name(self):
		return ''.join([self.Model,'_',str(self.id),])


	def __str__(self):
		return self.Name
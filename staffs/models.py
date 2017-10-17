# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import (
	Model,
	CharField, BooleanField,  DecimalField,
	PositiveIntegerField,
)

class Staff (Model):
	CHOICES_ROLE = (
		('TECH','Technician'),
		('STWD','Stewardess'),
	)

	name = CharField(
		max_length = 100,
	)

	Role = CharField(
		max_length = 100,
		blank = True, null = True,
		choices = CHOICES_ROLE
		)

	Rating = DecimalField(
		default = 0.0,
		decimal_places = 1, max_digits = 2
	)

	isAvailable = BooleanField(
		default = True
	)

	CurrentCaseCount = PositiveIntegerField(
		default = 0
	)

	MainHandPhoneNo = CharField(
		max_length = 100,
		blank = True, null = 'True'
	)

	AverageFixingTimeMinute = DecimalField(
		default = 0.0,
		decimal_places = 1, max_digits = 10
	)

	def __str__(self):
		return self.name

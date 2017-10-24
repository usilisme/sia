# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import (
	Model,
	CharField, BooleanField,  DecimalField,
	PositiveIntegerField,
)

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
	CHOICES_ROLE =(
		('S','Stewardess'),
		('T','Technician'),
		('X','Unassigned'),
	)

	Role = CharField(
		max_length = 100
		, default = True, null = True
		, choices = CHOICES_ROLE
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

	def __str__(self):
		return ''.join([self.Role,'_',self.username,])

	pass

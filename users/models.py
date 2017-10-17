# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
	CHOICES_ROLE =(
		('S','Stewardess'),
		('T','Technician'),
	)

	Role = models.CharField(
		max_length = 100
		, default = True, null = True
		, choices = CHOICES_ROLE
	)
	pass

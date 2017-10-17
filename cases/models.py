# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django.db.models import (
    Model,
    BooleanField, CharField, 
    DateField, DateTimeField, 
    ImageField, OneToOneField,
    PositiveIntegerField,
    ForeignKey,
)

from users.models import User
from staffs.models import Staff
from fleets.models import Airplane

class CaseHeader (Model):
	CHOICES_PRIORITY = (
				('H','High'),
				('M','Medium'),
				('L','Low')
				)

	CHOICES_PROBLEM_AREA = (
			('Engine','Engine'),
			('Toilet','Toilet'),
			('Seat','Seat'),
		)

	CHOICES_STATUS = (
		('OPENED','OPENED'),
		('RESOLVED','RESOLVED'),
		('IN-PROGRESS','IN-PROGRESS'),
		('RE-OPENED','RE-OPENED'),
		('CLOSED','CLOSED'),
	)

	CHOICES_PORT = (
		('CGK','Jakarta Soekarno Hatta'),
		('LAX','Los Angeles'),
		('NRT','Tokyo Narita Airport'),
		('SIN','Singapore Changi Airport'),
	)

	CHOICES_AIRCRAFT = (
		('Airbus A330-200','Airbus A330-200'),
		('Boeing 737-800','Boeing 737-800'),
	)

	CaseHeaderKey = CharField(
		max_length = 100,
		blank = True, null = True,
	)

	CreatedOn = DateTimeField(
		blank = True, null = True
	)
	LastUpdOn = DateTimeField(
		blank = True, null = True
	)

	Priority = CharField(
		max_length = 100,
		blank = True, null = True,
		choices=CHOICES_PRIORITY
	)

	Status = CharField(
		max_length = 100,
		default = 'OPENED',
		choices = CHOICES_STATUS
	)

	AssignedTo = ForeignKey(
		User,
		related_name = 'AssignedTo',
		blank = True, null = True,
	)

	ProblemArea = CharField(
		max_length = 100,
		blank = True, null = True,
		choices = CHOICES_PROBLEM_AREA
	)

	PortArrival = CharField(
		max_length = 100,
        blank = True, null = True,
		choices = CHOICES_PORT
	)

	isHandledBy = CharField(
		max_length = 100,
		blank = True, null = True,
	)

	isAssignedBy = CharField(
		max_length = 100,
		blank = True, null = True,
	)

	Reporter = ForeignKey(
		#max_length = 100,
		User,
		related_name = 'Reporter',
		blank = True, null = True,
	)

	isReportedBy = CharField(
		max_length = 100,
		blank = True, null = True,
	)

	ImageAttached = ImageField(
		blank = True, null = True,
	)

	FlightNo = CharField(
		max_length = 100,
		blank = True, null = True,
	)

	Airplane = ForeignKey(
		Airplane,
		blank = True, null = True,
	)



	Title = CharField(
		max_length = 100,
		blank = True, null = True,
	)

	Description = CharField(
		max_length = 100,
		blank = True, null = True
	)

	Feedback= CharField(
		max_length = 100,
		blank=True, null=True
	)

	SeatNo = CharField(
		max_length = 100,
		blank = True, null = True,
		default = 'N.A.'
	)

	ToiletNo = CharField(
		max_length = 100,
		blank=True, null=True,
		default = 'N.A.'
	)

	ParkingTimeMinute = PositiveIntegerField(
        blank=True, null=True,
        default = 0
    )

	def __str__(self):
		return self.CaseHeaderKey

	@property
	def Reporter_Name(self):
		return self.Reporter.username

class CaseHistory(models.Model):
	CaseHeaderKey = CharField(
		max_length = 100,
		blank = True, null = True,
	)

	CreatedOn = DateTimeField(
		blank = True, null = True
	)

	Description = CharField(
		max_length = 100,
		blank = True, null = True,
	)

	def __str__(self):
		return self.CaseHeaderKey
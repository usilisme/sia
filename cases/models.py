# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime as dt
import pytz

from django.db import models

from django.db.models import (
    Model,
    NullBooleanField, CharField, 
    DateField, DateTimeField, TimeField,
    ImageField, OneToOneField,
    PositiveIntegerField,
    DecimalField,
    ForeignKey,
)

from users.models import User
from flights.models import Airplane



class CaseHeader (Model):
	CHOICES_PRIORITY = (
				('H','High'),
				('M','Medium'),
				('L','Low')
				)

	CHOICES_PROBLEM_AREA = (
			('Air-Con','Air-Con'),
			('Toilet','Toilet'),
			('Seat','Seat'),
			('Tray','Tray'),
			('IFE','IFE'),
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
	ClosedOn = DateTimeField(
		blank = True, null = True,
	)
	@property
	def Age(self):
		if self.Status == 'CLOSED':
			return self.ClosedOn - self.CreatedOn
		else:
			return pytz.utc.localize(dt.datetime.now()) - self.CreatedOn


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
	Fixer = ForeignKey(
		User,
		related_name = 'Fixer',
		blank = True, null = True,
	)
	ServiceDuration = DecimalField(
		max_digits = 6, decimal_places=2,
		default = 0.0,
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
	@property
	def AirplaneNo(self):
		return self.Airplane.AirplaneNo


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
		return str(self.Title)

	@property
	def Reporter_Name(self):
		return self.Reporter.username

	def save(self,*args,**kwargs):
		if self.Status == 'CLOSED' and self.ClosedOn == None:
			self.ClosedOn = dt.datetime.now()
		super(CaseHeader,self).save(*args,**kwargs)

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

class TimeSlot(Model):
	TimeSlotFr = TimeField(
		blank = True, null = True,
	)
	TimeSlotTo = TimeField(
		blank = True, null = True,
	)
	def __str__(self):
		return self.TimeSlotFr.strftime("%H:%M") + " - " + self.TimeSlotTo.strftime("%H:%M")

class qDefect(Model):
	TimeSlot = ForeignKey(
		TimeSlot,
		blank = True, null = True,
	)
	Airplane = ForeignKey(
		Airplane,
		blank = True, null = True,
	)
	ProblemArea = CharField(
		max_length = 6,
		blank = True, null = True,
	)
	Defect = ForeignKey(
		CaseHeader,
		blank = True, null = True,
	)
	Fixer = ForeignKey(
		User,
		blank = True, null = True,
	)
	isPartAvailable = NullBooleanField(
		blank = True, null = True,
	)
	isPartSupplied = NullBooleanField(
		blank = True, null = True,
	)
	def __str__(self):
		return str(self.id)

class TechnicianStatistic(Model):
	Technician = ForeignKey(
		User,
		blank = True, null = True,
	)
	ProblemArea = CharField(
		max_length = 100,
		blank = True, null = True,
	)
	CountSolved = PositiveIntegerField(
		blank = True, null = True,
		default = 0,
	)
	MeanServiceDuration = DecimalField(
		max_digits = 8, decimal_places=2,
		default = 0.0,
	)

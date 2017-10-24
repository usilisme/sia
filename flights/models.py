# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import (
	Model,
	BooleanField,
	CharField, DateTimeField,
	ForeignKey,
)

class Airplane (Model):
	CHOICES_MODEL = (
		('A330-300','Airbus A330-300'),
		('A380-800','Airbus A380-800'),
		('B77W','Boeing 777-300ER'),
		('B772','Boeing 777-200'),
		('B773','Boeing 777-300'),
	)

	Model = CharField(
		max_length = 100,
		blank = True, null = True,
		choices = CHOICES_MODEL
	)

	RegNo = CharField(
		max_length = 100,
		blank = True, null = True,
	)

	@property
	def Name(self):
		return ''.join([self.Model,'_',self.RegNo,])


	def __str__(self):
		return self.Name

class FlightHistory(Model):
	CHOICES_PORT = (
		('HKG','Hong Kong Intl'),
		('LAX','Los Angeles'),
		('NRT','Tokyo Narita Airport'),
		('SIN','Singapore Changi Airport'),
		('SYD','Sydney Intl')
	)

	FlightNo = CharField(
		max_length = 100,
		blank = True, null = True,
	)

	AirplaneNo = ForeignKey(
		Airplane,
		blank = True, null = True,
	)

	AirplaneType = CharField(
		max_length = 100,
		blank = True, null = True,
	)

	PortDeparture = CharField(
		max_length = 100,
		blank = True, null = True,
		choices = CHOICES_PORT,
	)

	PortArrival = CharField(
		max_length = 100,
		blank = True, null = True,
		choices = CHOICES_PORT,
	)

	TimeDeparture = DateTimeField(
		max_length = 100,
		blank = True, null = True,
	)

class Parking(Model):
	Airplane = ForeignKey(
		Airplane,
		blank = True, null = True
	)
	FlightNoFr = CharField(
		max_length = 100,
		blank = True, null = True,	
	)
	DateTimeFr = DateTimeField(
		blank = True, null = True
	)
	FlightNoTo = CharField(
		max_length = 100,
		blank = True, null = True,	
	)
	DateTimeTo = DateTimeField(
		blank = True, null = True
	)
	Bay = CharField(
		max_length = 100,
		blank = True, null = True,	
	)
	isDelayed = BooleanField(
		default = False
	)

	@property
	def NameKey(self):
		return str(self.Airplane)+" "+ self.DateTimeFr.strftime("%y%m%d%H%M") +" "+ self.DateTimeTo.strftime("%y%m%d%H%M")

	def __str__(self):
		return self.NameKey

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import (
	Model,
	CharField, DateTimeField,
)

class FlightHistory(models.Model):
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

	AirplaneNo = CharField(
		max_length = 100,
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

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from flights.models import (
	Airplane, FlightHistory, Parking
	)

admin.site.register(Airplane)
#admin.site.register(FlightHistory)
admin.site.register(Parking)

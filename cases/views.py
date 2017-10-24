# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from cases.serializers import CaseHeaderSerializer
from cases.models import CaseHeader
from flights.models import FlightHistory

#API
class CaseList(generics.ListCreateAPIView):
	#permission_classes = (IsAuthenticated,)
	serializer_class = CaseHeaderSerializer

	def get_queryset(self):
		user = self.request.user
		queryset = CaseHeader.objects.all().filter(AssignedTo = user)
		return queryset

class CaseResolved(generics.ListCreateAPIView):
	permission_classes = (IsAuthenticated,)
	serializer_class = CaseHeaderSerializer

	def get_queryset(self):
		user = self.request.user
		CurAirplane = FlightHistory.objects.all().filter(FlightNo = self.kwargs['FlightNo']).get().id
		queryset = CaseHeader.objects.all().filter(Airplane_id = CurAirplane)
		return queryset


class CaseDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = CaseHeader.objects.all()
	serializer_class = CaseHeaderSerializer


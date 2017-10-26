# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from cases.models import (
	CaseHeader, CaseHistory,
	TimeSlot,
	qDefect,TechnicianStatistic, Part
)

@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
	list_display = ('id','PartKey','PartName','StockQty',)

@admin.register(CaseHeader)
class DefectAdmin(admin.ModelAdmin):
	list_display = ('id','Airplane'
		,'CreatedOn','ClosedOn','Age'
		,'ProblemArea','Title','Status'
		,'Fixer'
	)
	list_filter = ('Status',)

	fieldsets = (
		(None,{
			'fields': ('CaseHeaderKey',)
		}),
		('Flight Details',{
			'fields': (('FlightNo','Airplane','CreatedOn',),)
		}),
		('Defect Details',{
			'fields': (
			'Priority',
			('Status', 'LastUpdOn','ClosedOn'),
			'ProblemArea',
			'Title',
			'Description',
			'Feedback',
			'SeatNo',
			'ToiletNo',)
		}),
		('Fixer Details',{
			'fields': (('Fixer','ServiceDuration'),)
		}),
		('Reporter Details',{
			'fields': ('Reporter',)
		}),
		('Part Details',{
			'fields': ('Part',)
		})
	)
		

	pass
#admin.site.register(CaseHistory)
#admin.site.register(TimeSlot)

@admin.register(qDefect)
class qDefectAdmin(admin.ModelAdmin):
	list_display = ('id','Status','ServicingPort'
		,'TimeSlot','DeadlineTime','Airplane','Defect','Fixer','isPartAvailable')
	pass

@admin.register(TechnicianStatistic)
class TechStatAdmin(admin.ModelAdmin):
	list_display = ('id','Technician','ProblemArea','CountSolved','MeanServiceDuration')
	pass
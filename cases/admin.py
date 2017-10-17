# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from cases.models import (
	CaseHeader, CaseHistory
)

admin.site.register(CaseHeader)
admin.site.register(CaseHistory)
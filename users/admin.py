# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.models import Group

from users.models import User

admin.site.register(User)

admin.site.unregister(Group)

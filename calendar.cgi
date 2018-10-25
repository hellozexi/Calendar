#!/usr/bin/python
from wsgiref.handlers import CGIHandler
from my_calendar import app

CGIHandler().run(app)
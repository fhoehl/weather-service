# -*- coding: utf-8 -*-

import os
import json
from datetime import datetime
from calendar import timegm

from functools import wraps
from uuid import uuid4
from flask import Flask, request, session, render_template, url_for, jsonify
from flask import abort, redirect, Markup

import records

# Application
# -----------

is_test_run = 'TEST' in os.environ

app = Flask(__name__)
app.debug = True

db = records.Records(offline=is_test_run)

# Routes
# ------

@app.route('/')
def index():
    """Index"""
    return jsonify(message='Hello World!', methods=['GET'])

def respond_with_data(city, date, time, field=None):
    """Find and returns JSON data for a given city, date, time and data field."""
    try:
        timestamp = datetime.strptime(date + time, '%Y%m%d%H%M')
        data = db.find(city.lower(), timegm(timestamp.timetuple()), field)

        if not data:
            error_msg = message='No data for %i-%02d-%02d %02d:%02d' % \
                        (timestamp.year, timestamp.month, timestamp.day, \
                         timestamp.hour, timestamp.minute)

            return jsonify(status='error', message=error_msg)

        return jsonify(**data)
    except ValueError, e:
        return jsonify(status='error', message='Invalid date or time format.')

@app.route('/weather/<city>/<date>/<time>', methods=['GET'])
def get_city_data(city, date, time):
    """Return all the data for a given city, date and time."""
    return respond_with_data(city, date, time)

@app.route('/weather/<city>/<date>/<time>/<field>', methods=['GET'])
def get_city_data_field(city, date, time, field):
    """Return a specific data field for a given city, date and time."""
    return respond_with_data(city, date, time, field)


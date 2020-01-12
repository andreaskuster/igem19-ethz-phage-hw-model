#!/usr/bin/env python3
# encoding: utf-8

"""
    Copyright (C) 2019-2020  Andreas Kuster

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

__author__ = "Andreas Kuster"
__copyright__ = "Copyright 2019-2020"
__license__ = "GPL"

import json
import smtplib
from email.mime import multipart

with open("config.json") as config:
    _CONFIG = json.load(config)


@staticmethod
def send_notification(message: str):
    server = smtplib.SMTP(_CONFIG['email']['server'], _CONFIG['email']['port'])
    server.starttls()
    server.login(_CONFIG['email']['username'], _CONFIG['email']['password'])

    msg = multipart.MIMEMultipart()
    msg['From'] = _CONFIG['email']['username']
    msg['To'] = _CONFIG['email']['username']
    msg['Subject'] = "Alert: {}".format(message)
    server.sendmail(_CONFIG['email']['username'], _CONFIG['email']['username'], msg.as_string())

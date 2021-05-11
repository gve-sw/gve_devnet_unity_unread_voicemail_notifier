#!/usr/bin/env python3
'''Copyright (c) 2020 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.'''


import ADMIN
import MAIL_SERVER
import urllib3
import csv
import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
from datetime import datetime
from unity_notifier_functions import *


print('Generating monthly reports...')

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

server = ADMIN.SERVER
admin = ADMIN.USER
pw = ADMIN.PW

mail_server_usr = MAIL_SERVER.USER
mail_server_pw = MAIL_SERVER.PASSWORD
mail_server_hostname = MAIL_SERVER.HOSTNAME
mail_server_domain = MAIL_SERVER.DOMAIN
it_notifier_addr = MAIL_SERVER.FROM_ADDR

user_file = open('users.txt', 'r')
users = user_file.read()
user_file.close()
user_list = users.splitlines()
manager_dict = defaultdict(list)
mgr_info_dict = {}
today = datetime.now()
month = today.strftime('%B')

for user in user_list:
    user_info = {}
    addIdentifyingInfo(user, server, admin, pw, user_info)
    addCUPIInfo(server, admin, pw, user_info)
    addCUMIInfo(server, admin, pw, user_info)

    manager_dict[user_info['manager']].append(user_info)

for manager, reports in manager_dict.items():
    msg = MIMEMultipart()
    msg['From'] = it_notifier_addr
    msg['To'] = '{}@{}'.format(manager, mail_server_domain)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = 'Monthly Manager Voicemail Report - {}'.format(month)

    filename = '{}_monthly_report_{}.csv'.format(manager, month)
    report_file = open(filename, 'w', newline='')
    w = csv.writer(report_file)
    keys = ['alias', 'billing_id', 'building', 'department', 'display_name',
    'email_address', 'employee_id', 'first_name', 'last_name',
    'mailbox_oldest_unread_msg_days', 'mailbox_unread_msg_count',
    'mailbox_read_msg_count_30_days', 'manager', 'primary_extension', 'title']
    w.writerow(keys)
    for user in reports:
        values = [user['alias'], user['billing_id'], user['building'],
        user['department'], user['display_name'], user['email_address'],
        user['employee_id'], user['first_name'], user['last_name'],
        user['oldest'], user['total_unread'], user['total_read_30days'],
        user['manager'], user['extension'], user['title']]
        w.writerow(values)
    report_file.close()


    manager_info_dict = {}
    addIdentifyingInfo(manager, server, admin, pw, manager_info_dict)

    text = '''{},

The following report is generated from Children's National telecommunications system and
includes information for all of your direct reports that have an assigned extension in our
telecommunications system (and are listed accordingly PeopleSoft).  Please take a moment
to review -

- If staff have more than 20 unread voicemails, ensure the staff member addresses
immediately.
- If a listed employee is no longer active/has been terminated, you are responsible for
clearing their voicemail box and then contacting the Help Desk to deactivate the extension.
- If an employee is listed erroneously (does not report to you), contact the Help Desk.
- If you have any questions about an assigned extension, contact the Help Desk.'''.format(manager_info_dict['first_name'])

    msg.attach(MIMEText(text))

    fil = open(filename, 'rb')
    part = MIMEApplication(
        fil.read(),
        Name=filename
    )
    fil.close()
        # After the file is closed
    part['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
    msg.attach(part)

    smtp = smtplib.SMTP(mail_server_hostname)
    smtp.sendmail(it_notifier_addr, '{}@{}'.format(manager, mail_server_domain), msg.as_string())
    smtp.close()

    print('Report sent to {}'.format(manager))

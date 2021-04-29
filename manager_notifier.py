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
import urllib3
from collections import defaultdict
from unity_notifier_functions import *


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

server = ADMIN.SERVER
admin = ADMIN.USER
pw = ADMIN.PW

user_file = open('users.txt', 'r')
users = user_file.read()
user_file.close()
user_list = users.splitlines()
managers = defaultdict(list)


for user in user_list:
    user_info = {}
    addIdentifyingInfo(user, server, admin, pw, user_info)
    addCUMIInfo(server, admin, pw, user_info)
    addCUPIInfo(server, admin, pw, user_info)

    if user_info['total_unread'] >= '3':
        time_diff = (time.mktime(time.localtime()) - (int(user_info['oldest']) / 1000)) / 86400
        if time_diff > 30:
            managers[user_info['manager']].append(user_info)

for manager in managers:
    from_addr = '{}@emailserver.com'.format(admin)
    to_addr = '{}@emailserver.com'.format(manager)

    mail_server_usr = MAIL_SERVER.USER
    mail_server_pw = MAIL_SERVER.PASSWORD
    mail_server_hostname = MAIL_SERVER.HOSTNAME

    mail_server = smtplib.SMTP(mail_server_hostname, 587)
    mail_server.ehlo()
    mail_server.starttls()
    mail_server.login(mail_server_usr, mail_server_pw)

    header = 'Subject: Voicemail Notifier\n'
    message = header + '\n'

    for report in managers[manager]:
        add_string = report['first_name'] + ' ' + report['last_name'] + ' in building ' + report['building'] + ' has ' + report['total_unread'] + ' unopened voicemails.\n\n'
        message += add_string

    mail_server.sendmail(from_addr, to_addr, message)
    mail_server.quit()

    print('Email sent to ' + manager)
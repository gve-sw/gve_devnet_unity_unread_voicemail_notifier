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
from unity_notifier_functions import *


print('Generating manager emails...')

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

server = ADMIN.SERVER
admin = ADMIN.USER
pw = ADMIN.PW

mail_server_usr = MAIL_SERVER.USER
mail_server_pw = MAIL_SERVER.PASSWORD
mail_server_hostname = MAIL_SERVER.HOSTNAME
mail_server_domain = MAIL_SERVER.DOMAIN
it_notifier_addr = MAIL_SERVER.FROM_ADDR

#user_file = open('users.txt', 'r')
#users = user_file.read()
#user_file.close()
#user_list = users.splitlines()
user_list = getUsers(server, admin, pw)
managers = defaultdict(list)


for user in user_list:
    user_info = {}
    flag = addIdentifyingInfo(user, server, admin, pw, user_info)
    if not flag:
        user_list.remove(user)
        continue
    flag = addCUPIInfo(server, admin, pw, user_info)
    if not flag:
        user_list.remove(user)
        continue
    addCUMIInfo(server, admin, pw, user_info)

    if int(user_info['total_unread']) >= 30:
        time_diff = (time.mktime(time.localtime()) - (int(user_info['oldest']) / 1000)) / 86400
        if time_diff > 5:
            managers[user_info['manager']].append(user_info)

    print('added info about {}'.format(user))

for manager in managers:
    manager_dict = {}
    addIdentifyingInfo(manager, server, admin, pw, manager_dict)

    from_addr = '{}'.format(it_notifier_addr)
    to_addr = '{}@{}'.format(manager, mail_server_domain)

    mail_server = smtplib.SMTP(mail_server_hostname, 587)
    mail_server.ehlo()
    mail_server.starttls()
    mail_server.login(mail_server_usr, mail_server_pw)

    header = 'Subject: Weekly Report - Staff Over 30 Unread Voicemails\n\n'
    message = header + '''{},\n\nOur records indicate that the following employees
have 30 or more unread voicemails in their mailboxes. Please contact these employees to ensure they listen to
their voicemails and address immediately. Our policy requires all staff to listen to voicemails
and either save, delete, or respond to the voicemail, as deemed appropriate, by close of business the following
business day.\n\nIf you have questions about the information below, please contact the Help Desk.\n\n'''.format(manager_dict['first_name'])

    for report in managers[manager]:
        add_string = '{} {} with extension {} has {} unopened voicemails.\n\n'.format(report['first_name'], report['last_name'], report['extension'], report['total_unread'])
        message += add_string

    mail_server.sendmail(from_addr, to_addr, message)
    mail_server.quit()

    print('Email sent to ' + manager)

print("All manager emails sent.")

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
from unity_notifier_functions import *
import urllib3


print('Generating user emails...')

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

    print("Added information about {}".format(user))

    if int(user_info['total_unread']) > 20:
        from_addr = '{}'.format(it_notifier_addr)
        to_addr = '{}@{}'.format(user_info['alias'], mail_server_domain)

        mail_server = smtplib.SMTP(mail_server_hostname, )
        mail_server.ehlo()
        mail_server.starttls()
        mail_server.login(mail_server_usr, mail_server_pw)

        header = 'Subject: Voicemail Alert - You Have 20+ Unread Voicemails\n\n'
        msg_body = '''{},\n\nOur records indicate that you have 20 or more unread voicemails in your mailbox assigned to extension {}. Please
listen to your voicemails and address immediately. If the number of unread voicemails continues to increase, your manager will be
notified. Our policy requires all staff to listen to voicemails and either save, delete, or respond to the voicemail,
as deemed approprate, by close of business the following business day.\n\n If you believe this message was sent in error, and/or have
questions or issues about accessing your voicemail, please contact the Help Desk (476-HELP).'''.format(user_info['first_name'], user_info['extension'])

        message = header + msg_body

        mail_server.sendmail(from_addr, to_addr, message)
        mail_server.quit()

        print('Email sent to {}'.format(user_info['alias']))

print('All user emails sent.')

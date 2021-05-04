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
import csv
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
manager_dict = defaultdict(list)

for user in user_list:
    user_info = {}
    addIdentifyingInfo(user, server, admin, pw, user_info)
    addCUPIInfo(server, admin, pw, user_info)
    addCUMIInfo(server, admin, pw, user_info)

    manager_dict[user_info['manager']].append(user_info)

for manager, reports in manager_dict.items():
    report_file = open('{}_monthly_report.csv'.format(manager), 'w')
    w = csv.writer(report_file)
    w.writerow(reports[0].keys())
    for user in reports:
        w.writerow(user.values())
    report_file.close()

    print('Report generated for {}'.format(manager))

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


from apscheduler.schedulers.blocking import BlockingScheduler
import subprocess

def lazyrun(cmd):
    def run():
        subprocess.run(cmd)
    return run


scheduler = BlockingScheduler()
scheduler.add_job(lazyrun(('python', 'manager_notifier.py')), 'cron', day_of_week='thu', hour=8, minute=30)
scheduler.add_job(lazyrun(('python', 'user_notifier.py')), 'cron', day_of_week='mon-fri', hour=8, minute=31)
scheduler.add_job(lazyrun(('python', 'monthly_report.py')), 'cron', day='3rd thu', hour=8, minute=32)
scheduler.start()

# Unity Unread Voicemail Notifier
This is the Unity Unread Voicemail Notifier source code. Using the CUMI and CUPI APIs of Unity
and Python, we have developed a method to pull the number of unopened voicemails of Unity users
and if the number of unopened voicemails is over a specified threshold, an email is sent to the
user to notify them of their unopened voicemail count and an email is sent to their manager with
the user's location and number of unopened voicemails. 
Additionally, we have developed a method using these APIS to generate a report for each manager
that features information that can be found in a standard Unity Report for each of a manager's 
reports.

## Contacts
* Danielle Stacy (dastacy@cisco.com)
* Gerardo Chaves (gchaves@cisco.com)


## Solution Components
* Cisco Unity REST APIs
* Python


## Installation/Configuration

#### Clone the repo
```
$ git clone https://wwwin-github.cisco.com/gve/GVE_DevNet_Unity_Unread_Voicemail_Notifier
```

#### Installation
```
Create Virtual Environment (MacOS)
$ python3 -m venv VirtualEnvironment
$ source VirtualEnvironment/bin/activate
$ pip install --upgrade pip
$ pip install -r requirements.txt
```


## Setup

#### Unity details

You can deploy this prototype in a lab environment or in your own Unity network.
Fill in the unity server ip address, admin username, and password for your Unity
deployment in ADMIN.py.
```python
SERVER = "unity_server"
USER = "unity_admin"
PASSWORD = "unity password"
```

#### Email Server details
To receive the email notifications, fill in the username, password, and hostname
for your mail server.
```python
USER = r"server\user"
PASSWORD = "server_password"
HOSTNAME = "something.example.com"
```

#### User list
To collect information about users, list their user ids in the user.txt file.

#### Scheduler
Edit how often and when you want the code to run in scheduler.py

By default, manager_notifier.py runs every Thursday at 8:30 AM,
user_notifier.py runs every weekday at 8:30 AM, and monthly_report.py 
runs every 3rd Thursday at 8:30 AM.
```python
scheduler.add_job(lazyrun(('python', 'manager_notifier.py')), 'cron', day_of_week='thu', hour=8, minute=30)
scheduler.add_job(lazyrun(('python', 'user_notifier.py')), 'cron', day_of_week='mon-fri', hour=8, minute=30)
scheduler.add_job(lazyrun(('python', 'monthly_report.py')), 'cron', day='3rd thu', hour=8, minute=30)
```


## Usage
To run the code to send an email notification to a user about their unopened
voicemails:
```
$ python user_notifier.py
```

To run the code to send an email notification to managers about their 
reports' unopened voicemails:
```
$ python manager_notifier.py
```

To run the code to generate a standard Unity Report for each manager
about their reports:
```
$ python monthly_report.py
```

To run each of these scripts at periodic intervals:
```
$ python scheduler.py
```


# Screenshots

![/IMAGES/0image.png](/IMAGES/0image.png)

### LICENSE

Provided under Cisco Sample Code License, for details see [LICENSE](LICENSE.md)

### CODE_OF_CONDUCT

Our code of conduct is available [here](CODE_OF_CONDUCT.md)

### CONTRIBUTING

See our contributing guidelines [here](CONTRIBUTING.md)

#### DISCLAIMER:
<b>Please note:</b> This script is meant for demo purposes only. All tools/ scripts in this repo are released for use "AS IS" without any warranties of any kind, including, but not limited to their installation, use, or performance. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not responsible for any damage or data loss incurred with their use.
You are responsible for reviewing and testing any scripts you run thoroughly before use in any non-testing environment.

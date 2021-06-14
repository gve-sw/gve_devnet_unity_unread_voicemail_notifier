# Unity Unread Voicemail Notifier
This is the Unity Unread Voicemail Notifier source code. Using the CUMI and CUPI APIs of Unity
and Python, we have developed a method to pull the number of unopened voicemails of Unity users.
If the number of unopened voicemails is over a specified threshold, an email is sent to the
user to notify them of their unopened voicemail count, and an email is sent to their manager detailing
their reports who have unopened voicemails over a specified threshold, where the oldest is older than 
a specified number of days old.
Additionally, we have developed a method using these APIs to generate a report for each manager
that features information that can be found in a standard Unity Report for each of a manager's 
reports.

## Contacts
* Danielle Stacy (dastacy@cisco.com)
* Gerardo Chaves (gchaves@cisco.com)



## Solution Components
* Cisco Unity REST APIs
* Python



## Installation


#### Clone the repo
```
$ git clone https://github.com/gve-sw/gve_devnet_unity_unread_voicemail_notifier
```


#### Set up virtual environment
```
Create and enter virtual environment (MacOS)
$ python3 -m venv VirtualEnvironment
$ source VirtualEnvironment/bin/activate
$ pip install --upgrade pip
$ pip install -r requirements.txt
```



## Configuration


#### Unity details
You can deploy this prototype in a lab environment or in your own Unity network. Fill in the unity 
server ip address, admin username, and password for your Unity deployment in ADMIN.py.
```python
SERVER = "unity_server"
USER = "unity_admin"
PASSWORD = "unity password"
```


#### Email Server details
To receive the email notifications, fill in the username, password, hostname, domain name, and email
from which you wish to send the notification emails from for your mail server in MAIL_SERVER.py
```python
USER = r"server\user"
PASSWORD = "server_password"
HOSTNAME = "something.example.com"
DOMAIN = "example.com"
FROM_ADDR = "emailyouwanttosendmessagesfrom@example.com"
```


#### Unity Users
The code has two different ways to retrieve the list of Unity users. By default, the code will retrieve 
the list of users from Unity using an API call. If this method does not work for you, you can put the 
user's usernames in the file users.txt.

If you choose to retrieve the users from the text file, edit the code in manager_notifier.py, 
user_notifier.py, and monthly_report.py.

In manager_notifier.py and user_notifier.py, uncomment the code on lines 38 - 41 and remove line 42.

In monthly_report.py, uncomment the code on lines 46 - 49 and remove line 50.

```python
#user_file = open('users.txt', 'r')
#users = user_file.read()
#user_file.close()
#user_list = users.splitlines()
user_list = getUsers(server, admin, pw)
```


#### Scheduler
Edit how often and when you want the code to run in scheduler.py

By default, manager_notifier.py runs every Thursday at 8:30 AM, user_notifier.py runs every weekday 
at 8:31 AM, and monthly_report.py runs every 3rd Thursday at 8:32 AM.
```python
scheduler.add_job(lazyrun(('python', 'manager_notifier.py')), 'cron', day_of_week='thu', hour=8, minute=30)
scheduler.add_job(lazyrun(('python', 'user_notifier.py')), 'cron', day_of_week='mon-fri', hour=8, minute=31)
scheduler.add_job(lazyrun(('python', 'monthly_report.py')), 'cron', day='3rd thu', hour=8, minute=32)
```

For more information about the python module apscheduler, visit this link:
https://apscheduler.readthedocs.io/en/stable/modules/triggers/cron.html#module-apscheduler.triggers.cron

For more information about CRON expressions in general, visit this link:
https://en.wikipedia.org/wiki/Cron#CRON_expression


#### Email Body
Edit what you want to say in the emails in manager_notifier.py, user_notifier.py, and monthly_report.py.

In manager_notifier.py, you can find the body of the email starting on line 78. This is what it reads by 
default:
```python
message = header + '''{},\n\nOur records indicate that the following employees
have 30 or more unread voicemails in their mailboxes. Please contact these employees to ensure they listen to
their voicemails and address immediately. Our policy requires all staff to listen to voicemails
and either save, delete, or respond to the voicemail, as deemed appropriate, by close of business the following
business day.\n\nIf you have questions about the information below, please contact the Help Desk.\n\n'''.format(manager_dict['first_name'])
```

In user_notifier.py, you can find the body of the email starting on line 68. This is what it reads by 
default:
```python
msg_body = '''{},\n\nOur records indicate that you have 20 or more unread voicemails in your mailbox assigned to extension {}. Please
listen to your voicemails and address immediately. If the number of unread voicemails continues to increase, your manager will be
notified. Our policy requires all staff to listen to voicemails and either save, delete, or respond to the voicemail,
as deemed approprate, by close of business the following business day.\n\n If you believe this message was sent in error, and/or have
questions or issues about accessing your voicemail, please contact the Help Desk.\n\n'''.format(user_info['first_name'], user_info['extension'])
```

In monthly_report.py, you can find the body of the email starting on line 99. This is what it reads by 
default:
```python
text = '''{},

The following report is generated from our telecommunications system and
includes information for all of your direct reports that have an assigned extension in our
telecommunications system (and are listed accordingly in the directory).  Please take a moment
to review -

- If staff have more than 20 unread voicemails, ensure the staff member addresses
immediately.
- If a listed employee is no longer active/has been terminated, you are responsible for
clearing their voicemail box and then contacting the Help Desk to deactivate the extension.
- If an employee is listed erroneously (does not report to you), contact the Help Desk.
- If you have any questions about an assigned extension, contact the Help Desk.\n\n'''.format(manager_info_dict['first_name'])
```


#### Voicemail Thresholds
By default, emails are sent to users when they have 20 or more unopened voicemails and to managers when their 
reports have 30 or more unopened voicemails, where the oldest is 5 days old. 

To change the threshold at which emails are sent to users, edit the line of code in user_notifier.py at line 58.
```python
if int(user_info['total_unread']) > 20:
```

To change the threshold at which emails are sent to managers, 
edit the line of code in manager_notifier.py at line 58.
```python
if int(user_info['total_unread']) >= 30:
```

To change the age for which enauks are sent to managers, edit the line of code 
in manager_notifier.py at line 60.
```python
if time_diff > 5:
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

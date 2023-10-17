from NotificationClass.Notification import Notification
from NotificationClass.NotificationMail import NotificationMail
from NotificationClass.NotificationSMS import NotificationSMS
import random

def notify(notification: Notification):
    notification.send()

def check_type(notification: Notification):
    print(notification)

list_notification = [
    NotificationMail,
    NotificationSMS
]

message = [
    'I called you earlier, please call me back!',
    'I sent a message to you, please check your fucking smartphone!'
]

for x in range(3):
    notification = random.choice(list_notification)(random.choice(message))
    
    check_type(notification)
    notify(notification)

    if isinstance(notification, NotificationMail):
        new_notification = notification * 3

    if isinstance(notification, NotificationSMS):
        print(notification + 'Jhonatan')

    print()


# sms = NotificationSMS('I called you earlier, please call me back')
# email = NotificationMail('I sent a message to you, please check your fucking smartphone')

# notify(sms)
# notify(email)

# check_type(sms)
# check_type(email)
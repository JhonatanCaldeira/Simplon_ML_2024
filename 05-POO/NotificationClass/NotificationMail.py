from NotificationClass.Notification import Notification

class NotificationMail(Notification):
    def __init__(self, message) -> None:
        super().__init__(message)

    def send(self) -> bool:
        print("Sending E-mail: ", self.message)
        return True
    
    def __str__(self) -> str:
        return "This is an object of the NotificationMail class" 

if __name__ == '__main__':

    mail = NotificationMail('Hello World')
    mail.send()
    
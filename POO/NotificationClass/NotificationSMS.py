from NotificationClass.Notification import Notification

class NotificationSMS(Notification):
    def debug(func):
        def _debug(*args, **kwargs):
            result = func(*args, **kwargs)
            print(f'{func.__name__}(args: {args}, kwargs: {kwargs}) -> {result}')
            return result
        return _debug

    def __init__(self, message) -> None:
        super().__init__(message)

    @debug
    def send(self) -> bool:
        print("Sending SMS: ", self.message)
        return True
    
    def __str__(self) -> str:
        return "This is an object of the NotificationSMS class"

if __name__ == '__main__':

    mail = NotificationSMS('Hello World')
    mail.send()
from abc import ABC, abstractmethod

class Notification(ABC):
    def __init__(self, message) -> None:
        self.message = message

    @property
    def message(self):
        return self._message
    
    @message.setter
    def message(self, value):
        self._message = value 

    def __mul__(self, num: int):
        if isinstance(num, int):
            for i in range(num):
                self.send()
        else:
            return False
        
        return True

    def __add__(self, value):
        return self.message + ' ' + str(value)

    @abstractmethod
    def send(self) -> bool:
        pass
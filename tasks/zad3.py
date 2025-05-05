import random
import string

class PasswordGenerator:
    def __init__(self, length = 13, charset = string.ascii_letters + string.digits, count = 10): 
        self.length = length
        self.charset = charset
        self.count = count
        self.index = -1
    
    def __iter__(self):
        return self
        
    def __next__(self):
        self.index += 1
        if self.index < self.count:
            return self._generate_password()
        raise StopIteration()
    
    def _generate_password(self):
        return ''.join(random.choice(self.charset) for _ in range(self.length))
    
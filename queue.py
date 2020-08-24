class Queue:
    
    def __init__(self):
        self.values = []
        return
        
    def isEmpty(self):
        return len(self.values) == 0
    
    def insert(self, value):
        self.values.append(value)
        return
    
    def remove(self):
        value = None
        if not self.isEmpty():
            value = self.values.pop(0)            
        return value
        
    def contents(self):
        return self.values
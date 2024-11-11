class Add:
    def __init__(self, value=0):
        self.total = value 

    def __call__(self, value):
        self.total += value 
        return self

    def __repr__(self):
        return str(self.total)

def add(value):
    return Add(value)

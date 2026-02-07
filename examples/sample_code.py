def complex_function(a, b, c, d, e, f):
    """
    Function with too many arguments and deep nesting.
    """
    if a > 0:
        if b > 0:
            if c > 0:
                if d > 0:
                    print("Extremely nested!")
    
    result = 0
    for i in range(10):
        for j in range(10):
            result += i * j
            
    return result

class DataProcessor:
    def __init__(self, data):
        self.data = data
        
    def process(self):
        # A long comment to simulate a "long" method if we had more code
        if not self.data:
            return None
        
        processed = [x * 2 for x in self.data if x % 2 == 0]
        return processed

def simple_func(x):
    return x + 1

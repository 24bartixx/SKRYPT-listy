def make_generator(function):
    
    def generator():
        i = 1
        while True:
            yield function(i)
            i += 1
            
    return generator()
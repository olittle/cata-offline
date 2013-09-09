from math import exp 

def logist(score, bc):
    x = score + bc 
    y = 1.0 / (1.0 + exp(-x))
    
    return y

if __name__ == "__main__":
    a = logist(0.1, 0.2)
    print a 

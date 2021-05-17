def exponent(x, y, v=None):
    result = x ** y
    return (result * v) if v else result
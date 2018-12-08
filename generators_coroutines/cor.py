

def is_odd():
    while True:
        num = (yield)
        print(num % 2 != 0)


def start(func):
    cr = func()
    cr.__next__()
    return cr


if __name__ == '__main__':
    """
    Coroutines are consumers of data
    Not related for iteration 
    """
    p = start(is_odd)
    p.send(66)
    p.send(100)
    p.send(1)
    p.send(9)


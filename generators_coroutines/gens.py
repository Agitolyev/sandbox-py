def countdown(n=10):
    while n >= 0:
        yield n
        n -= 1


if __name__ == '__main__':
    """
    Generators produce values, used for iterations for example
    """
    for i in countdown():
        print(i)

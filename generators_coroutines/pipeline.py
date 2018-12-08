import random

ALPHABET = [chr(sym) for sym in range(41, 123)]


def rand_char_producer():
    while True:
        yield random.choice(ALPHABET)                                              # Pull from alphabet


def rand_string_producer(num_of_strings, length=42):

    for i in range(num_of_strings):
        yield ''.join([rand_char_producer().__next__() for j in range(length)])    # Pull from rand_char_producer


"""                                                                                 |
 ▲                                                                                  ▲
 |                                                                                  |
 |                                                                                  |
 +---------------- Generators pull data --------------------------------------------+
 
 
 +---------------- Coroutines push data -------------------------------------------+
 |                                                                                  | 
 |                                                                                  |
 ▼                                                                                  ▼
"""


def coroutine(cor):
    """
    :param cor: coroutine to start
    :return: started coroutine
    """
    def started(*args, **kwargs):
        cr = cor(*args, **kwargs)
        cr.__next__()
        return cr
    return started


@coroutine
def upperer(consumer):
    while True:
        string = (yield)
        consumer.send(string.upper())                                # Push data to next coroutine


@coroutine
def string_filter(condition_f, consumer):
    while True:
        string = (yield)
        if condition_f(string):
            consumer.send(string)                                    # Push data to next coroutine


@coroutine
def hasher(consumer):
    import hashlib

    while True:
        inpt = (yield)
        consumer.send(hashlib.sha1(str(inpt).encode()).hexdigest())  # Push data to next coroutine

@coroutine
def printer():
    """
    Sink, prints data to console
    """
    while True:
        inpt = (yield)
        print(inpt)                                                  # Prints data (push to stdout)


if __name__ == '__main__':
    """ Pipelines
    
    producers(Source) -> processor_0 -> processor_1 -> processor_2 -> ... -> processors_n -> end-point (Sink) 
    
    """

    up_n_print = upperer(printer())
    hash_up_n_print = hasher(up_n_print)
    filter_hash_up_print = string_filter(lambda it: it.startswith('A'), hash_up_n_print)

    for line in rand_string_producer(100):
        filter_hash_up_print.send(line)

import time
from contextlib import contextmanager

@contextmanager
def timer(label):
    start = time.time()
    try:
        yield
    finally:
        end = time.time()
        print('%s: %0.6f' % (label, end-start))


@contextmanager
def binary_progress_notifier(label):
    print(label)
    try:
        yield
    finally:
        print('( %s ) - done!' % label)


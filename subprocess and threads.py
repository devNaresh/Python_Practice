__author__ = '__naresh__'

import subprocess
from time import time
from threading import Thread


# proc = subprocess.Popen(['echo', 'Hello from the child!'], stdout=subprocess.PIPE)
# out, err = proc.communicate()
# print(out.decode('utf-8'))
#
# proc = subprocess.Popen(['sleep', '0.3'])
# while proc.poll() is None:
#     print('Waiting')
#
# print('Exit Status', proc.poll())


def test(number):
    for i in range(1, number):
        if number % i == 0:
            yield i


numbers = [2139079, 1214759, 1516637, 1852285]




class TestThread(Thread):
    def __init__(self, number):
        super().__init__()
        self.number = number

    def run(self):
        self.factors = list(test(self.number))

start = time()
threads = []
for number in numbers:
    thread = TestThread(number)
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

end = time()
print("difference = ", end - start)

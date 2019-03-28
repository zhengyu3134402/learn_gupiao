
from redis import *
class UseRedis:

    def __init__(self):
        self.sr = StrictRedis()

    def del_data(self):
        self.sr.flushdb()


def main():
    u = UseRedis()
    u.del_data()


if __name__ == '__main__':
    main()
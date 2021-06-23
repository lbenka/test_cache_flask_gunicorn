from functools import lru_cache
from urllib import request, error
from cachetools import cached, TTLCache
import os
from flask import Flask


class B:
    @cached(cache=TTLCache(maxsize=3, ttl=10))
    def foo(self):
        print("inside foo")
        resource = "http://www.python.org/dev/peps/pep-%04d/" % 20
        try:
            with request.urlopen(resource) as s:
                return s.read()
        except error.HTTPError:
            return "Not Found"

    @staticmethod
    @cached(cache=TTLCache(maxsize=3, ttl=10))
    def foo2():
        print("inside foo2")
        resource = "http://www.python.org/dev/peps/pep-%04d/" % 20
        try:
            with request.urlopen(resource) as s:
                return s.read()
        except error.HTTPError:
            return "Not Found"


@lru_cache(maxsize=5)
def class_factory():
    client = B()
    print(client)
    return client


def main():
    a = class_factory().foo()[:10]
    # print(class_factory.cache_info())

    print(f"pid: {os.getpid()}")
    return a


def main2():
    print(f"pid: {os.getpid()}")
    b = B()
    print(b)
    return b.foo()[:10]


def main3():
    print(f"pid: {os.getpid()}")
    b = B()
    print(b)
    return b.foo2()[:10]

## app here ## 
app = Flask(__name__)


@app.route("/1")
def hello():
    return main()


@app.route("/2")
def main2_route():
    return main2()


@app.route("/3")
def main3_route():
    return main3()

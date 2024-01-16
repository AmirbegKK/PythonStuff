from threading  import Lock, Thread


class SingletonMeta(type):

    _instances = {}
    _lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock: 
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]

class Singleton(metaclass=SingletonMeta):
    def greeting(self):
        print(self.value)
    
    def __init__(self, value) -> None:
        self.value = value

class Singleton2():
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def print_id(self):
        print(id(self))

class SingletonLazy(): # One state different instances
    __instance = None

    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            cls.__instance = SingletonLazy()
        return cls.__instance
    
    def __init__(self) -> None:
        if SingletonLazy.__instance is None:
            pass
        else:
            print('already has')
        
        
    def print_id(self):
        print(id(self.__instance))



def test_singleton(value):
    s1 = Singleton(value)
    s2 = Singleton2()
    s1.greeting()
    s2.print_id()

def test_singleton2(value):
    s2 = Singleton2()
    s2.print_id()

def test_singletonLazy(value):
    s3 = SingletonLazy()
    s3.print_id()


if __name__ == '__main__':
    SingletonLazy.get_instance()
    process1 = Thread(target=test_singletonLazy, args=('hi man',))
    process2 = Thread(target=test_singletonLazy, args=('hi men',))
    process1.start()
    process2.start()




class Singleton(type):
    __cls = dict()

    def __call__(cls, *args, **kwargs):
        if cls not in cls.__cls:
            cls.__cls[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls.__cls[cls]

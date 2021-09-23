class Singleton(type):
    __cls = dict()

    def __call__(cls, *args, **kwds):
        if cls not in cls.__cls:
            cls.__cls[cls] = super(Singleton, cls).__call__(*args, **kwds)
        return cls.__cls[cls]

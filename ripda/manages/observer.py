

class Observer:
    def __init__(self) -> None:
        self.observers = list()

    def notify(self, **kwds) -> None:
        for observer in self.observers:
            observer.recv(**kwds)

    def register(self, observer) -> None:
        self.observers.append(observer)

    def unregister(self, observer) -> None:
        self.observers.remove(observer)

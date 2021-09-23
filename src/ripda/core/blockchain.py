from ripda.manages.singleton import Singleton
from ripda.core.network import Network
import websockets
import json


class Blockchain(metaclass=Singleton):
    
    network = Network()

    
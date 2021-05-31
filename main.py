try:
    import thread
except ImportError:
    import _thread as thread
import time
import os

PATH = os.path.dirname(os.path.realpath(__file__))


def node():
    os.system('python ' + PATH + '/node.py')
    pass

def wallet():
    # os.system('python ' + PATH + '/wallet.py')
    pass

def miner_1QDHV2TfNDCoaMeVerRz6v6eHfDLNtiFNU():
    os.system('python ' + PATH + '/miner_1QDHV2TfNDCoaMeVerRz6v6eHfDLNtiFNU.py')
    pass

def miner_18yvjn9rEBG4npnG8sZTVhUJRpkDzcws7h():
    os.system('python ' + PATH + '/miner_18yvjn9rEBG4npnG8sZTVhUJRpkDzcws7h.py')
    pass

def miner_13H2LNehz6skD7VA6cmwhfwDxuRNSRYcbo():
    os.system('python ' + PATH + '/miner_13H2LNehz6skD7VA6cmwhfwDxuRNSRYcbo.py')
    pass

def miner_14bCyrPDTbY2T5YF1mSH729PhKqzdtbg9Z():
    os.system('python ' + PATH + '/miner_14bCyrPDTbY2T5YF1mSH729PhKqzdtbg9Z.py')
    pass

def init():
    thread.start_new_thread(node, ())
    time.sleep(20)
    # thread.start_new_thread(wallet, ())
    time.sleep(10)
    thread.start_new_thread(miner_1QDHV2TfNDCoaMeVerRz6v6eHfDLNtiFNU, ())
    thread.start_new_thread(miner_13H2LNehz6skD7VA6cmwhfwDxuRNSRYcbo, ())
    thread.start_new_thread(miner_14bCyrPDTbY2T5YF1mSH729PhKqzdtbg9Z, ())
    thread.start_new_thread(miner_18yvjn9rEBG4npnG8sZTVhUJRpkDzcws7h, ())
    while True:
        time.sleep(3.154e+9)
        pass


if __name__ == '__main__':
    init()

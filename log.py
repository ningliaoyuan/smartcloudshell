import time

class log:
    def start(self, msg):
        self.begin = time.time()
        self.beginMsg = msg
        print("Start:", msg)
        return self

    def end(self, msg = None):
        elapsed = time.time() - self.begin
        minutes, seconds = divmod(elapsed, 60)

        if msg is None:
          msg = self.beginMsg
        print("End:", msg, " | elapsed time: {:0>2}:{:05.2f}".format(int(minutes),seconds))

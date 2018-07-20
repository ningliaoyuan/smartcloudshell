import time

class log:
    def start(self, msg):
        self.begin = time.time()
        print("Start:", msg)
        return self

    def end(self, msg = None):
        elapsed = time.time() - self.begin
        minutes, seconds = divmod(elapsed, 60)
        print("End:", msg, " | elapsed time: {:0>2}:{:05.2f}".format(int(minutes),seconds))

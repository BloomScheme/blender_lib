import time


class TimeMeasurement:
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.start()

    def start(self):
        self.start_time = time.time()

    def end(self, message=""):
        self.end_time = time.time()
        self.print_elapsed_time(message)
        self.start()

    def get_elapsed_time(self):
        if self.start_time is None or self.end_time is None:
            raise Exception("start_time or end_time is None")
        return self.end_time - self.start_time

    def print_elapsed_time(self, message=""):
        print(message, "Elapsed time: ", self.get_elapsed_time())

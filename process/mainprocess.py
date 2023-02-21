from threading import Thread, Event
import logging

class mainprocess(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.event = Event()
        self.has_stopped = False


    def run(self):
        while True:
            try:
                if self.has_stopped:
                    break

                self.event.wait(1)
            except:
                import traceback
                logging.error(traceback.format_exc())
            

    def stop(self):
        self.has_stopped = True
        self.event.set()
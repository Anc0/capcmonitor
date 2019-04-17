from threading import Thread


class TemplateListener(Thread):

    """
    Template class, meant as a thread management wrapper for all other components.
    """

    def __init__(self):
        Thread.__init__(self)
        self.kill = False

    def stop_thread(self):
        """
        Set kill to True, which stops the thread.
        """
        self.kill = True

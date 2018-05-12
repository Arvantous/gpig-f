class Historian(object):
    """
    Keeps track of the history of objects.
    """

    def __init__(self):
        self.history = {}

    def record(self, obj):
        timestamp = len(self.history)
        self.history[timestamp] = obj
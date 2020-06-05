import abc


class Predictor():
    def __init__(self):
        pass

    @abc.abstractmethod
    def predict(self, line, lineno, column, path):
        pass

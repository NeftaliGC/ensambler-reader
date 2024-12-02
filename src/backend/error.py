

class Error():
    def __init__(self, line, segment):
        self.line = line
        self.segment = segment
        self.error = None
        self.errorType = ""

    def setError(self, error, errorType):
        self.error = error
        self.errorType = errorType

    def getError(self):
        return f"{self.error}: {errorType}"

    def identidyError(self):
        if self.segment == "stack":
            pass
        elif self.segment == "data":
            pass
        elif self.segment == "code":
            pass

        
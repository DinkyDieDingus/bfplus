
class Executor:
    def __init__(self, instructions):
        self.instructions = instructions

    def finish(self):
        pass

    def beforeInstr(self, i):
        return i

    def afterInstr(self, i):
        return i

    def incPtr(self, i):
        return i

    def decPtr(self, i):
        return i

    def inc(self, i):
        return i

    def dec(self, i):
        return i

    def print(self, i):
        return i

    def input(self, i):
        return i

    def loopStart(self, i):
        return i

    def loopEnd(self, i):
        return i

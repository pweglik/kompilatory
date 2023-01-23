

class Memory:

    def __init__(self, name): # memory name

    def has_key(self, name):  # variable name

    def get(self, name):         # gets from memory current value of variable <name>

    def put(self, name, value):  # puts into memory current value of variable <name>


class MemoryStack:
                                                                             
    def __init__(self, memory=None): # initialize memory stack with memory <memory>

    def get(self, name):             # gets from memory stack current value of variable <name>

    def insert(self, name, value): # inserts into memory stack variable <name> with value <value>

    def set(self, name, value): # sets variable <name> to value <value>

    def push(self, memory): # pushes memory <memory> onto the stack

    def pop(self):          # pops the top memory from the stack



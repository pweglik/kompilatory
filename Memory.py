class Memory:
    def __init__(self):  # memory name
        self.memory = {}

    def has_key(self, name):
        return name in self.memory.keys()

    def get(self, name):
        return self.memory.get(name, None)

    def set(self, name, value):
        self.memory[name] = value


class MemoryStack:
    def __init__(self, memory=None):
        self.stack = [Memory()]

    def get_variable(self, name):
        for memory in reversed(self.stack):
            res = memory.get(name)
            if res is not None:
                return res

        return None

    def set_in_top(self, name, value):
        self.stack[0].set(name, value)

    def set_variable(self, name, value):
        for memory in reversed(self.stack):
            if memory.has_key(name):
                return memory.set(name, value)
        self.set_in_top(name, value)

    def push_memory_to_stack(self):
        self.stack.append(Memory())

    def pop_memory_from_stack(self):
        self.stack.pop()

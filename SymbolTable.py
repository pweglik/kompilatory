#!/usr/bin/env python3

class Symbol: pass

# class VariableSymbol(Symbol):
#     def __init__(self, name, type):
#         self.name = name
#         self.type = type

class VarSymbol:
    def __init__(self, name, type_, dim = 0, size = None):
        self.name = name
        self.type_ = type_
        # if dim == 0 we have a variable. for 1 we have a vector and for 2 we have a matrix
        self.dim = dim
        self.size = size

    # str allows for easy get_type but we still can get the type of variables inside the vector directly
    def __str__(self):
        if self.dim > 0:
            return 'vector'
        else: return self.type_


class SymbolTable(object):

    def __init__(self, parent, name):  # parent scope and symbol table name
        self.parent = parent
        self.name = name
        self.dict = {}

    def put(self, name, symbol):  # put variable symbol or fundef under <name> entry
        self.dict[name] = symbol

    def get(self, name):  # get variable symbol or fundef from <name> entry
        if name in self.dict.keys():
            return self.dict[name]
        elif self.parent is not None:
            return self.parent.get(name)
        else: return None

    def getParentScope(self):
        return self.parent

    def pushScope(self, name):
        return SymbolTable(self, name)

    def popScope(self):
        return self.
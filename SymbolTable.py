#!/usr/bin/env python3

class Symbol: pass

class VarSymbol:
    def __init__(self, name, type_, dim = 0, size = None):
        self.name = name
        self.type_ = type_

        self.dim = dim
        self.size = size

    def __str__(self):
        if self.dim > 0:
            return 'vector'
        else: return self.type_


class SymbolTable(object):
    def __init__(self, parent, name):  
        self.parent = parent
        self.name = name
        self.dict = {}

    def put(self, name, symbol):  
        self.dict[name] = symbol

    def get(self, name):
        if name in self.dict.keys():
            return self.dict[name]
        elif self.parent is not None:
            return self.parent.get(name)
        else: return None

    def pushScope(self, name):
        return SymbolTable(self, name)

    def popScope(self):
        return self.parent
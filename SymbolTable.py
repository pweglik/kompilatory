#!/usr/bin/env python3


class Symbol:
    pass


class VarSymbol:
    def __init__(self, name, type_, shape=None):
        if not type_ in ["int", "float", "bool", "string", "vector"]:
            raise ValueError(f"Invalid type: {type_}")
        self.name = name
        self.type_ = type_
        self.shape = shape

    def __str__(self):
        return f"VarSymbol({self.name}, {self.type_}, {self.shape})"

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, VarSymbol):
            return self.type_ == __o.type_ and self.shape == __o.shape
        else:
            return False
        
    def __hash__(self) -> int:
        return hash((self.type_, self.shape))


class SymbolTable(object):
    def __init__(self, parent, name):
        self.parent = parent
        self.name = name
        self.dict = {}

    def put(self, name: str, symbol: VarSymbol):
        self.dict[name] = symbol

    def get(self, name: str) -> VarSymbol:
        if name in self.dict.keys():
            return self.dict[name]
        elif self.parent is not None:
            return self.parent.get(name)
        else:
            return None

    def pushScope(self, name: str):
        return SymbolTable(self, name)

    def popScope(self):
        return self.parent

def draw_ast(node, layers = 0):
    if type(node) is tuple:
        string = '|  ' * layers + str(node[0])
        print(string)

        for i in range(1, len(node)):
            draw_ast(node[i], layers + 1)

    elif type(node) is list:
        for i in range(len(node)):
            draw_ast(node[i], layers)
    else:
        # primitive or list
        string = '|  ' * layers + str(node)
        print(string)

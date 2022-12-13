def draw_ast(node, layers = 0):
    if type(node) is tuple:
        if node[0] == "IF_TAG":
            draw_ast(node[1][0], layers)
            draw_ast(node[1][1], layers)
        elif node[0] == 'IF_ELSE_TAG':
            draw_ast(node[1][0], layers)
            draw_ast(node[1][1], layers)
            draw_ast(node[1][2], layers)
        else:
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

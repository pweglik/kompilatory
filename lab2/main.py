from parser import SimpleParser
from lexer import SimpleLexer
from draw_ast import draw_ast

if __name__ == '__main__':
    lexer = SimpleLexer()
    parser = SimpleParser()

    text = '''
# control flow instruction

N = 10;
M = 20;

if(N==10)
    print "N==10";
else if(N!=10)
    print "N!=10";


if(N>5) {
    print "N>5";
}
else if(N>=0) {
    print "N>=0";
}

if(N<10) {
    print "N<10";
}
else if(N<=15)
    print "N<=15";

k = 10;
while(k>0)
    k = k - 1;

while(k>0) {
    if(k<5)
        i = 1;
    else if(k<10)
        i = 2;   
    else
        i = 3;
    
    k = k - 1;
}


for i = 1:N
  for j = i:M
    print i, j;
 

for i = 1:N {
    if(i<=N/16)
        print i;
    else if(i<=N/8)
        break;
    else if(i<=N/4)
        continue;
    else if(i<=N/2)
        return 0;
}


{
  N = 100;
  M = 200;  
}

a * b + c;
a + b * c;
    '''


    text='''
    a = [1, 2 , [3, 4]];
    c = a[1][2];
    b[5] = 7;

    for i = 1:N
    for j = i:M
        print i, j;

    for i = 1:N {
        if(i<=N/16)
            print i;
        else if(i<=N/8)
            break;
        else if(i<=N/4)
            continue;
        else if(i<=N/2)
            return 0;
    }
    '''
    
    tokens = lexer.tokenize(text)

    # for t in lexer.tokenize(text):
    #     print(t)

    result = parser.parse(tokens)

    # print()
    # for statement in result:
    #     print(statement)
    # print(f'\n{result}')

    draw_ast(result)

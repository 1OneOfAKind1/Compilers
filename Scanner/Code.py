import string
tokens=[]


def scanner (v) :
    state = "start"
    m = ""
    n = ""
    for c in v:
        if state == "start":
            m += c
            if c in string.ascii_letters:
                state = "ident"
            elif c in string.digits:
                state = "num"
            elif c == ":":
                state = "assign"
            elif c in string.whitespace:
                state = "start"
                m = ""
            elif c == "{":
                state = "comment"
            else:
                state = "done"
        elif state == "ident":
            if c in string.ascii_letters or c in string.digits:
                state = "ident"
                m += c
            else:
                state = "done"
                n="Identfier"
        elif state == "num":
            if c in string.digits:
                state = "num"
                m += c
            else:
                state = "done"
                n="Number"
        elif state == "assign":
            if c == "=":
                state = "done"
                m += c
                n="Assign"
            else:
                state = "done"
        elif state == "comment":
            if c == "}":
                state = "start"
                m = ""
            else:
                state = "comment"
        if state == "done":
            if n=="":
                n="Symbol"
            elif n == "Identfier" :
                if m=="if" or m=="then" or m=="else" or m=="else" or m=="end" or m=="repeat" or m=="until" or m=="read" or m=="write":
                    n=m
            tokens.append((m,n))
            #print(m,n)
            #x=v.find(m)+len(m)
            #y=len(v)-1
            scanner(v[v.find(m)+len(m):len(v)])
            return
    return



with open('testcase.txt') as fp:
   line = fp.readline()
   while line:
       scanner(line+" ")
       line = fp.readline()


with open('output.txt', 'w') as f:
    for i in tokens:
        print(i , file=f)
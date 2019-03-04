import string
from random import random
"""
from graphviz import Graph
from graphviz import Digraph
"""



inc = 0
token=""
level=0


class Tree(object):
    def __init__(self):
        self.left = None
        self.mid = None
        self.right = None
        self.data = None
        self.next = None
        self.before = None


def print_tree(tree):
    global level
    if tree == None: return
    print(("    "*level)+tree.data)
    temp = level
    level = level + 1
    print_tree(tree.left)
    print_tree(tree.mid)
    print_tree(tree.right)
    level = temp
    print_tree(tree.next)
    return

"""
dot = Digraph(filename = 'Parse_tree',format = 'png')
def draw_tree(tree):
    if tree == None: return 0
    x=(random()*1000)+1
    if(tree.data=="if" or tree.data=="repeat" or tree.data=="write" or (1+tree.data.find("read")) or (1+tree.data.find("assign"))):
        dot.node(str(x) , tree.data , shape='square')
    else:
        dot.node(str(x) , tree.data )
    
    y=draw_tree(tree.left)
    if y :
        dot.edge(str(x), str(y))
    y=draw_tree(tree.mid)
    if y :
        dot.edge(str(x), str(y))
    y=draw_tree(tree.right)
    if y :
        dot.edge(str(x), str(y))
    y=draw_tree(tree.next)
    if y :
        dot.edge(str(x), str(y), constraint='false')
    return x
"""


textstr=""
def get_tree(tree):
    global level
    global textstr
    if tree == None: return
    textstr=textstr+(("    "*level)+tree.data)+"\n"
    temp = level
    level = level + 1
    print_tree(tree.left)
    print_tree(tree.mid)
    print_tree(tree.right)
    level = temp
    print_tree(tree.next)
    return







#Scanner
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
                n="identifier"
        elif state == "num":
            if c in string.digits:
                state = "num"
                m += c
            else:
                state = "done"
                n="number"
        elif state == "assign":
            if c == "=":
                state = "done"
                m += c
                n=":="
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
                n=m
            elif n == "identifier" :
                if m=="if" or m=="then" or m=="else" or m=="else" or m=="end" or m=="repeat" or m=="until" or m=="read" or m=="write":
                    n=m
            tokens.append((m,n))
            scanner(v[v.find(m)+len(m):len(v)])
            return
    return




#parser


#match function
def match(expected_token) :
    #if(check_end()):
        #return
    global inc
    global token
    #global endf
    if (tokens[inc][1] == expected_token) :
        old_now = inc
        if (len(tokens) == inc+1):
            #endf = 1
            token = "sc"
        else:
            inc = inc+1
            token = tokens[inc][1]
        return tokens[old_now][0]
    else :
        return

#grammer rules in EBNF

#factor -> (exp)  |  number |  identifier
def factor() :
    temp = Tree()
    if (token=="number"):
        temp.data = "const(" + match("number") + ")"
    elif (token=="identifier"):
        temp.data = "id(" + match("identifier") + ")"
    elif (token=="("):
        match("(")
        temp = exp()
        match(")")
    return temp


#mulop -> *  | /
def mulop():
    temp = Tree()
    temp.data = "op(" + match(token) + ")"
    return temp


#term -> factor {mulop factor}
def term() :
    temp = Tree()
    temp = factor()
    if(token=="*" or token=="/"):
        new_temp = Tree()
        new_temp = mulop()
        new_temp.left = temp
        new_temp.right = factor()
        temp = new_temp
    return temp


#addop -> + | -
def addop() :
    temp = Tree()
    temp.data = "op(" + match(token) + ")"
    return temp


#simple_exp -> term {addop term}
def simple_exp() :
    temp = Tree()
    temp = term()
    if(token=="+" or token=="-"):
        new_temp = Tree()
        new_temp = addop()
        new_temp.left = temp
        new_temp.right = term()
        temp = new_temp
    return temp


#comparison_op -> < | =
def comparison_op() :
    temp = Tree()
    temp.data = "op(" + match(token) + ")"
    return temp


#exp -> simple-exp  [comparison-op simple-exp]
def exp() :
    temp = Tree()
    temp = simple_exp()
    if (token == "<" or token == "=") :
        new_temp = Tree()
        new_temp = comparison_op()
        new_temp.left = temp
        new_temp.right = simple_exp()
        temp= new_temp
    return temp


#write_stmt -> write exp
def write_stmt() :
    temp = Tree()
    temp.data = match("write")
    temp.mid = exp()
    return temp


#read_stmt -> read identifier
def read_stmt() :
    temp = Tree()
    temp.data = match("read") + "(" + match("identifier") + ")"
    return temp


#assign_stmt -> identifier := exp
def assign_stmt() :
    temp = Tree()
    temp.data = "assign(" + match("identifier") + ")"
    match(":=")
    temp.mid = exp()
    return temp


#repeat_stmt -> repeat stmt_sequence until exp
def repeat_stmt() :
    temp = Tree()
    temp.data = match("repeat")
    temp.left = stmt_sequence()
    match("until")
    temp.right = exp()
    return temp


#if_stmt -> if exp then stmt_sequence [else stmt_sequence] end
def if_stmt() :
    temp = Tree()
    temp.data = match("if")
    temp.left = exp()
    match("then")
    temp.mid = stmt_sequence()
    if(token=="else"):
        match("else")
        temp.right = stmt_sequence()
    match("end")
    return temp


#statement -> if_stmt | repeat_stmt | assign_stmt | read_stmt | write_stmt
def statement() :
    temp = Tree()
    if (token=="if") :
        temp = if_stmt()
    elif (token=="repeat") :
        temp = repeat_stmt()
    elif (token=="identifier") :
        temp = assign_stmt()
    elif (token=="read") :
        temp = read_stmt()
    elif (token=="write") :
        temp = write_stmt()
    else:
        return
    return temp


#stmt_sequence -> statement {; statement}
def stmt_sequence() :
    arr = []
    temp = Tree()
    temp = statement()
    arr.append(temp)
    while(token == ";"):
        match(token)
        arr[-1].next = statement()
        arr.append(arr[-1].next)


    return temp


#program -> stmt-sequence
def program():
    return stmt_sequence()



"""
with open('testcase.txt') as fp:
   line = fp.readline()
   while line:
       scanner(line+" ")
       line = fp.readline()


with open('output.txt', 'w') as f:
    for i in tokens:
        print(i, file=f)
"""


def parse(text):
    global token
    for line in text.splitlines():
        scanner(line+" ")
    token = tokens[0][1]
    mytree=program()
    print(mytree)
    #draw_tree(mytree)
    #dot.render(view=False)

def reseting():
    global inc
    global token
    global level
    inc = 0
    token=""
    level=0
    tokens=[]
    #dot.clear()

def parse_text(text):
    global token
    for line in text.splitlines():
        scanner(line+" ")
    token = tokens[0][1]
    mytree=program()
    get_tree(mytree)
    return textstr
    

"""
token = tokens[0][1]
mytree=program()
print_tree(mytree)
draw_tree(mytree)
dot.view()
"""


==================================================================

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Programs\PyQT\projects\Parser Project\ParserGUI.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from Parser import parse_text
import Parser
import string
"""
from random import random
from graphviz import Graph
from graphviz import Digraph
"""


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(605, 463)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.codetext = QtWidgets.QTextEdit(self.centralwidget)
        self.codetext.setObjectName("codetext")
        self.verticalLayout.addWidget(self.codetext)
        self.parsebutton = QtWidgets.QPushButton(self.centralwidget)
        self.parsebutton.setObjectName("parsebutton")
        self.verticalLayout.addWidget(self.parsebutton)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.imageshow = QtWidgets.QLabel(self.centralwidget)
        self.imageshow.setText("")
        self.imageshow.setObjectName("imageshow")
        self.verticalLayout.addWidget(self.imageshow)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.parsebutton.clicked.connect(self.getthecode)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600;\">Write code below</span></p></body></html>"))
        self.parsebutton.setText(_translate("MainWindow", "Parse"))
        self.label_2.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600;\">Image will show below</span></p></body></html>"))

    def getthecode(self):
        mycode = self.codetext.toPlainText()
        x=parse_text(str(mycode))
        """
        pixmap = QtGui.QPixmap("Parse_tree.png")
        self.imageshow.setPixmap(pixmap)
        self.imageshow.setAlignment(QtCore.Qt.AlignCenter)
        """
        self.imageshow.setText(x)
        Parser.reseting()



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


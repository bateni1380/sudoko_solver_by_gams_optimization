#------------------------------------------------
#gams code
#------------------------------------------------
def get_model_text():
    return """
set
    i/1*9/;
alias(i,j,k);

Parameter
    n(i,j);

$GDXIN %gdxincname%
$LOAD n
$GDXIN

integer variable
    result,
    v(i,j);
variable
    z;

binary variable
*x[i,j,k] = 1 -> x(i,j) = k
    x(i,j,k);

integer variable
    v(i,j);

equation
    obj,
    const1,
    const2,
    const3
    const4,
    const5;

obj..
    z =e= 0;

*satr va sotoon
const1(j,k)..
    sum(i,x(i,j,k)) =e= 1;
const2(i,k)..
    sum(j,x(i,j,k)) =e= 1;
const3(i,j)..
    sum(k,x(i,j,k)) =e= 1;

const4(i,j,k)$(n(i,j)=k.val)..
    x(i,j,k) =e= 1;

*block
const5(i,j,k)$( (i.val = 1 or i.val = 4 or i.val = 7) and (j.val = 1 or j.val = 4 or j.val = 7) )..
    x(i,j,k)+x(i,j+1,k)+x(i,j+2,k)+x(i+1,j,k)+x(i+1,j+1,k)+x(i+1,j+2,k)+x(i+2,j,k)+x(i+2,j+1,k)+x(i+2,j+2,k) =e= 1;


model sudoku/obj, const1, const2, const3, const4, const5/;
solve sudoku using MIP minimizing z;
"""
#s="530070000600195000098000060800060003400803001700020006060000280000419005000080079"
#------------------------------------------------
#gams python
#------------------------------------------------
def solve_with_gams(s):
    import os
    BASE_DIR = os.path.abspath('')

    import gams
    ws = gams.workspace.GamsWorkspace(working_directory=BASE_DIR)

    i_python = [str(i) for i in range(1,10)]
    n_python = {}
    
    for i in range(1,10):
        for j in range(1,10):
            n_python[(str(i),str(j))]=int(s[(i-1)*9 + j-1])

    db = ws.add_database()

    i = db.add_set("i",1)
    for ip in i_python:
        i.add_record(ip)

    n = db.add_parameter_dc("n",[i,i])

    for ip in i_python:
        for ipp in i_python:
            n.add_record((ip,ipp)).value = n_python[(ip,ipp)]
            

    opt = ws.add_options()
    opt.defines["gdxincname"] = db.name

    m = ws.add_job_from_string(get_model_text())
    m.run(opt, databases=db)
    x=""
    for rec in m.out_db["x"]:
        if rec.level==1:
            x += rec.key(2)
    return x

#------------------------------------------------
#gams code
#------------------------------------------------
from tkinter import *

root = Tk()
root.geometry('330x370')

class Interface():
    def __init__(self, window):
        self.window = window
        window.title("Simple Sudoku Game")

        font = ('Arial', 20)
        color = 'white'

        solve = Button(window, text = 'Solve', command = self.Solve)
        solve.grid(column=3,row=20)
        clear = Button(window, text = 'Clear', command = self.Clear)
        clear.grid(column = 5,row=20)

       
        self.board  = []
        for row in range(9):
            self.board += [["","","","","","","","",""]]

        for row in range(9):
            for col in range(9):
                
                if (row < 3 or row > 5) and (col < 3 or col > 5):
                    color = 'white' 
                elif (row >= 3 and row < 6) and (col >=3 and col < 6):
                    color = 'white'
                else:
                    color = 'grey'
                
                self.board[row][col] = Entry(window, width = 2, font = font, bg = color, cursor = 'arrow', borderwidth = 2,
                                          highlightcolor = 'yellow', highlightthickness = 0, highlightbackground = 'black', 
                                          textvariable = filledBoard[row][col]) 
                self.board[row][col].grid(row = row, column = col)

    def Solve(self):
        s=""
        for row in range(9):
            for col in range(9):
                if filledBoard[row][col].get() not in ['1','2','3','4','5','6','7','8','9']:
                    s += "0"
                else:
                    s += filledBoard[row][col].get()
        
        s = solve_with_gams(s)
        if len(s)!=81:
            return
        for row in range(9):
            for col in range(9):
                filledBoard[row][col].set(s[row*9 + col])

    
    def Clear(self):
        for row in range(9):
            for col in range(9):
                filledBoard[row][col].set('')


filledBoard = []
for row in range(9): 
    filledBoard += [["","","","","","","","",""]]
for row in range(9):
    for col in range(9):
        filledBoard[row][col] = StringVar(root)    


Interface(root)
root.mainloop()

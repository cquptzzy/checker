import tkinter as tk
from PIL import ImageTk, Image
from board import board
from tkinter.messagebox import *
class GUI():
    def __init__(self):
        # Build game
        self.game=board()
        # Create a window, and some parts in the window
        self.root = tk.Tk()                       #初始化窗口
        self.root.title('checkers')
        self.root.geometry("1000x700")
        self.root.resizable(width=False,height=False)

        menubar = tk.Menu()
        menubar.add_command(label='quit', command=self.root.destroy)
        menubar.add_command(label='Instructions', command=lambda: self.showabout())
        menubar.add_command(label='rule', command=lambda: self.rule())
        # Create three menu options
        # drop out
        # rule
        # And instructions

        # Divide the window into two parts, the display part and the operation part
        self.root.config(menu=menubar)
        self.root.rowconfigure(0, weight=800)
        self.root.columnconfigure(0, weight=800)
        self.root.columnconfigure(1, weight=200)
        self.gameframe = tk.Frame(self.root, width=800, height=800)
        self.gameframe.grid(row=0, column=0)
        self.gameframe.rowconfigure(0,weight=75)
        self.gameframe.rowconfigure(1,weight=75)
        self.gameframe.rowconfigure(2,weight=75)
        self.gameframe.rowconfigure(3,weight=75)
        self.gameframe.rowconfigure(4,weight=75)
        self.gameframe.rowconfigure(5,weight=75)
        self.gameframe.rowconfigure(6,weight=75)
        self.gameframe.rowconfigure(7,weight=75)
        self.gameframe.columnconfigure(0,weight=75)
        self.gameframe.columnconfigure(1,weight=75)
        self.gameframe.columnconfigure(2,weight=75)
        self.gameframe.columnconfigure(3,weight=75)
        self.gameframe.columnconfigure(4,weight=75)
        self.gameframe.columnconfigure(5,weight=75)
        self.gameframe.columnconfigure(6,weight=75)
        self.gameframe.columnconfigure(7,weight=75)

        # Import board pictures
        self.w = tk.Canvas(self.gameframe, width = 700, height = 700, background = "white")
        self.p= ImageTk.PhotoImage(Image.open('b1.jpg'))
        self.w.create_image(350,350, image=self.p)
        self.w.grid(row=0,column=0)
        # Generate some buttons
        self.set_buttom()
        # And update the canvas and prompts
        self.updata()


    def set_buttom(self):
        # Lay out the operating part
        self.gameframe2 = tk.Frame(self.root, width=200, height=800)
        self.gameframe2.rowconfigure(0, weight=1)
        self.gameframe2.rowconfigure(1, weight=1)
        self.gameframe2.rowconfigure(2, weight=1)
        self.gameframe2.rowconfigure(3, weight=1)
        self.gameframe2.rowconfigure(4, weight=1)
        self.gameframe2.rowconfigure(5, weight=1)
        self.gameframe2.rowconfigure(6, weight=1)
        self.gameframe2.rowconfigure(7, weight=1)
        self.gameframe2.rowconfigure(8, weight=1)
        self.gameframe2.rowconfigure(9, weight=1)
        self.gameframe2.rowconfigure(10, weight=1)
        self.gameframe2.rowconfigure(11, weight=1)
        self.gameframe2.rowconfigure(12, weight=1)
        self.gameframe2.rowconfigure(13, weight=1)
        self.gameframe2.columnconfigure(0, weight=1)
        self.gameframe2.columnconfigure(1, weight=1)
        self.gameframe2.grid(row=0,column=1)

        # Create two prompt labels, four input boxes, and two buttons,
        # which are used to implement actions
        self.l1=tk.Label(self.gameframe2,text='which position X                               Y')
        self.l1.grid(row=0,column=0,columnspan=2)
        self.inpx=tk.Entry(self.gameframe2)
        self.inpx.grid(row=1,column=0)
        self.inpy = tk.Entry(self.gameframe2)
        self.inpy.grid(row=1, column=1)
        self.ch=tk.Button(self.gameframe2,text='check',command=lambda: self.che1())
        self.ch.grid(row=2,column=0, columnspan=2)
        self.l1 = tk.Label(self.gameframe2, text='move to X                               Y')
        self.l1.grid(row=3, column=0, columnspan=2)
        self.inpx1 = tk.Entry(self.gameframe2)
        self.inpx1.grid(row=4, column=0)
        self.inpy1 = tk.Entry(self.gameframe2)
        self.inpy1.grid(row=4, column=1)
        self.mo = tk.Button(self.gameframe2, text='move',command=lambda: self.move_to())
        self.mo.grid(row=5, column=0, columnspan=2)
        self.change_diffc = tk.Button(self.gameframe2, text='change difficulty', command=lambda: self.change_difficulty())
        self.change_diffc.grid(row=13, column=0, columnspan=2)
        # Generate a slider and the corresponding difficulty display
        self.difficulty = tk.IntVar()
        self.difficulty.set(4)
        self.diff=tk.Label(self.gameframe2,text='difficulty')
        self.diff.grid(row=12,column=0)
        self.sc = tk.Scale(self.gameframe2, variable=self.difficulty, orient=tk.HORIZONTAL, from_=1, to=4)
        self.sc.grid(row=12,column=1)

        self.l1 = tk.Label(self.gameframe2, text='hint:these piece can be choose')
        self.l1.grid(row=7, column=0, columnspan=2)
        self.l2 = tk.Label(self.gameframe2, text= str(self.filter()[:5]),font=('宋体',15))
        self.l2.grid(row=8, column=0, columnspan=2)
        self.l5 = tk.Label(self.gameframe2, text=str(self.filter()[5:]), font=('宋体', 15))
        self.l5.grid(row=9, column=0, columnspan=2)
        self.l3 = tk.Label(self.gameframe2, text='hint:these posotion can be choose')
        self.l3.grid(row=10, column=0, columnspan=2)





    def change_difficulty(self):
        # Get the corresponding difficulty from the slider
        d=self.difficulty.get()
        d=int(d)
        print(d)
        self.game.get_diffc(self.game,d)
        showinfo(title='info',message='you have change difficulty')

    def che(self):
        # Check if the first two inputs are legal
        x = self.inpx.get()
        y = self.inpy.get()

        l=[x,y]
        for i in l:
            if not i.isdigit():
                return False
        return True

    def che1(self):
        # Check if the first two inputs are legal
        p=self.che()
        if not p:
            showerror('error','input error')
        else:
            x = self.inpx.get()
            y = self.inpy.get()
            x = int(x)
            y = int(y)


            # Then update the prompt information of the canvas part and the operation part
            if (x,y) in self.filter():
                showinfo('','True')
                hint=self.game.find_onechecker_all_action(self.game.state, x, y, 'Player')
                if hint[-1]=='jump':
                    self.l4 = tk.Label(self.gameframe2, text='                     ', font=('宋体', 15))
                    self.l4.grid(row=11, column=0, columnspan=2)
                    self.l4 = tk.Label(self.gameframe2, text=str(hint[0][0]), font=('宋体', 15))
                    self.l4.grid(row=11, column=0, columnspan=2)
                if hint[-1]=='move':
                    self.l4 = tk.Label(self.gameframe2, text='                     ', font=('宋体', 15))
                    self.l4.grid(row=11, column=0, columnspan=2)
                    self.l4 = tk.Label(self.gameframe2, text=str(hint[0]), font=('宋体', 15))
                    self.l4.grid(row=11, column=0, columnspan=2)
                pos,a = hint

                if a=='move':

                    for p in pos:

                        self.w.create_oval(71 * (p[1] + 1) + 20, 71 * (p[0] + 1) + 20, 71 * (p[1] + 2) - 20,71 * (p[0] + 2) - 20, fill='blue')
                elif a=='jump':
                    for p in pos[0]:
                        self.w.create_oval(71 * (p[1] + 1) + 20, 71 * (p[0] + 1) + 20, 71 * (p[1] + 2) - 20,71 * (p[0] + 2) - 20, fill='blue')

            else:
                showerror('illegal input')


    def move_to1(self):
        # Check if 4 inputs are legal
        x1 = self.inpx1.get()
        y1 = self.inpy1.get()
        x = self.inpx.get()
        y = self.inpy.get()
        l = [x, y,x1,y1]
        for i in l:
            if not i.isdigit():
                return False
        x=int(x)
        y=int(y)
        x1=int(x1)
        y1=int(y1)
        can_move=self.game.find_onechecker_all_action(self.game.state,x,y,'Player')

        if can_move[-1]=='move':
            can_move=can_move[0]
        elif can_move[-1]=='jump':
            can_move = can_move[0][0]

        for i,j in can_move:
            if (i,j)==(x1,y1):
                return True

        return False


    def move_to(self):
        # Check if 4 inputs are legal
        p=self.move_to1()
        if not p:
            showerror('error', 'input error')
        else:
            x1 = self.inpx1.get()
            y1 = self.inpy1.get()
            x = self.inpx.get()
            y = self.inpy.get()
            x1=int(x1)
            y1 = int(y1)
            y = int(y)
            x = int(x)
            # Move the corresponding action,
            # update the canvas and prompt information,
            # and switch sides (AI action)
            self.game.do(self.game.state,x,y,x1,y1)
            self.updata()
            self.end_condition()
            self.to_AI()




    def filter(self):
        si = 0
        c_m = self.game.check_can_move(self.game.state, 'Player')
        for i in c_m:
            if i[-1]=='jump':
                si=1
                break
        if si==0:
            return [(p[0],p[1]) for p in c_m]
        elif si==1:
            return [(p[0],p[1]) for p in c_m if p[-1]=='jump']
    def to_AI(self):
        self.ch.configure(state='disable')
        self.mo.configure(state='disable')
        # Move the corresponding action,
        # update the canvas and prompt information,
        # and change sides (the user's turn)
        self.game.evaluate_states()
        self.updata()
        self.end_condition()
        self.ch.configure(state='normal')
        self.mo.configure(state='normal')

    def end_condition(self):
        # Information update on the chessboard
        self.game.pos()
        # User has no pawns
        if self.game.player_number == 0:
            showinfo('AI,WIN')
            self.mo.configure(state='disable')
            self.ch.configure(state='disable')
            self.change_diffc.configure(state='disable')

        # AI has no pawns
        elif self.game.AI_number == 0:

            showinfo('Player,WIN')
            self.mo.configure(state='disable')
            self.ch.configure(state='disable')
            self.change_diffc.configure(state='disable')

        # User can't act anymore
        elif len(self.game.check_can_move(self.game.state,'AI'))==0:
            showinfo('Player,WIN')
            self.mo.configure(state='disable')
            self.ch.configure(state='disable')
            self.change_diffc.configure(state='disable')

        # AI can't act anymore
        elif len(self.game.check_can_move(self.game.state,'Player'))==0:
            showinfo('AI,WIN')
            self.mo.configure(state='disable')
            self.ch.configure(state='disable')
            self.change_diffc.configure(state='disable')

    def updata(self):
        # Import background checkerboard
        self.w.delete('all')
        self.w = tk.Canvas(self.gameframe, width=700, height=700, background="white")
        self.p = ImageTk.PhotoImage(Image.open('b1.jpg'))

        self.w.create_image(350, 350, image=self.p)
        self.w.grid(row=0, column=0)
        si=0
        p=[]
        # Detect where there are pieces
        for i in range(8):
            for j in range(8):
                if self.game.state[j][i]!=0:
                    p.append((j,i))

        # Draw the chess pieces (normal chess pieces are round,
        # kings are triangles,
        # movable pieces plus small green circles,
        # and the movable positions are small blue circles)
        for pi in p:
            if self.game.state[pi[0]][pi[1]].color == 'AI':
                if self.game.state[pi[0]][pi[1]].king==False:
                    self.w.create_oval(71*(pi[1]+1),71*(pi[0]+1),71*(pi[1]+2),71*(pi[0]+2),fill='white')
                elif  self.game.state[pi[0]][pi[1]].king==True:
                    point=[71*(pi[1]+2),71*(pi[0]+2),
                          71*(pi[1]+1),71*(pi[0]+2),
                          71*pi[1]+105,71*(pi[0]+1)]
                    self.w.create_polygon(point,fill='white' )
            else:
                if self.game.state[pi[0]][pi[1]].king == False:
                    self.w.create_oval(71 * (pi[1] + 1), 71 * (pi[0] + 1), 71 * (pi[1] + 2), 71 * (pi[0] + 2), fill='red')
                elif self.game.state[pi[0]][pi[1]].king == True:
                    point = [71 * (pi[1] + 2), 71 * (pi[0] + 2),
                             71 * (pi[1] + 1), 71 * (pi[0] + 2),
                             71 * pi[1] + 105, 71 * (pi[0] + 1)]
                    self.w.create_polygon(point, fill='red')

        c_m=self.game.check_can_move(self.game.state,'Player')
        for i in c_m:
            if i[-1]=='jump':
                si=1
                break
        if si==0:
            for i in c_m:
                self.w.create_oval(71 * (i[1] + 1)+20, 71 * (i[0] + 1)+20, 71 * (i[1] + 2)-20, 71 * (i[0] + 2)-20, fill='green')

        elif si==1:
            for i in c_m:
                if i[-1]=='jump':
                    self.w.create_oval(71 * (i[1] + 1)+20, 71 * (i[0] + 1)+20, 71 * (i[1] + 2)-20, 71 * (i[0] + 2)-20, fill='green')

        self.l2.configure(text= str(self.filter()),font=('宋体',15))

    def showabout(self):
        # Instructions
        showinfo(title='Instructions' ,message='The game interface is divided into two parts, the left is the chessboard, and the right is the operation interface.The chessboard is an 8x8 interface, in which the red chess pieces are operated by the user, ''and the white pieces are operated by the AI. The green dot indicates that the current user can move. The blue dots indicate. Actions that can be performed by selecting a piece.\
        \n The input box on the first line of the operation interface indicates the piece you want to operate (for example, input (5,0) at the beginning of the game),and then you can click the check button to check whether the piece can be moved, and the board will be blue Click (if the chess piece can be moved), the operation interface will also prompt (output the position that can be moved). The input in the second line represents the coordinates of the move of the chess piece input in the first line. Then the user can click the move button to move.The bottom slider and buttons can adjust the difficulty (the game will not be restarted).'
        )

    def rule(self):
        # Rules introduction
        showinfo(title='rule',message='Black moves first and play proceeds alternately. From their initial positions, checkers may only move forward. There are two types of moves that can be made, capturing moves and non-capturing moves. Non-capturing moves are simply a diagonal move forward from one square to an adjacent square. (Note that the white squares are never used.) Capturing moves occur when a player "jumps" an opposing piece. This is also done on the diagonal and can only happen when the square behind (on the same diagonal) is also open. This means that you may not jump an opposing piece around a corner.Capturing Move On a capturing move, a piece may make multiple jumps. If after a jump a player is in a position to make another jump then he may do so. This means that a player may make several jumps in succession, capturing several pieces on a single turn.Forced Captures: When a player is in a position to make a capturing move, he must make a capturing move. When he has more than one capturing move to choose from he may take whichever move suits him')


checker=GUI()
checker.root.mainloop()
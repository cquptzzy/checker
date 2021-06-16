from piece import *

import time
from copy import deepcopy
import math
# Set up a board class
class board():
    def __init__(self,):
        self.state=[]
        # Use a list to represent the board
        self.AI_number=12
        self.player_number=12
        self.AI_king=0
        self.player_king=0
        self.generate()
        self.player_turn=True
        self.depth=2

    #     Obtain the depth of the maximum and minimum algorithm from the outside
    @staticmethod
    def get_diffc(board,depth):
        board.depth=depth


    # Generate checkerboard based on position
    def generate(self):
        for i in range(8):
            self.state.append([])
            for j in range(8):
                # The first three are AI pawns, the last three are the user's pawns
                if i <=2 :
                    if (i+j)%2==1:

                        self.state[i].append(piece(i,j,'AI'))

                    else:
                        self.state[i].append(0)

                elif i>=5:
                    if (i+j)%2==1 :

                        self.state[i].append(piece(i,j,'Player'))

                    else:
                        self.state[i].append(0)
                else:
                    self.state[i].append(0)
        self.printbo(self.state)


    # Check if you can move between two positions
    @staticmethod
    def move(state,o_row,o_col,n_row,n_col,who):
        # Can't move beyond the range
        if n_row >7 or n_col>7 or n_row <0 or n_col<0 or o_row >7 or o_col>7 or o_row <0 or o_col<0:
            return False
        if state[o_row][o_col].color==who and state[n_row][n_col]==0:
            return True
        else:
            return False

    # Check if you can jump between two positions
    @staticmethod
    def jump(state,o_row,o_col,j_row,j_col,n_row,n_col,who):
        if n_row > 7 or n_col > 7 or n_row < 0 or n_col < 0 or o_row > 7 or o_col > 7 or o_row < 0 or o_col < 0:
            return False
        if state[o_row][o_col].color!=who:
            return False
        # The captured piece must belong to the other side
        if state[j_row][j_col]==0 or state[j_row][j_col].color==who:
            return False

        if state[n_row][n_col]!=0:
            return False
        return True

    @staticmethod
    def jumpcu(state,parent,who,sussesor=[]):
        sussesor=[]
        if who=='Player':
            if state[parent[0][0]][parent[0][1]].king==False:
                # If it is a king, judge whether it can jump in 4 directions, if it is not a king, only judge in two directions
                i=-1
                for j in [-1,1]:
                    if board.jump(state,parent[0][0],parent[0][1],parent[0][0]+i,parent[0][1]+j,parent[0][0]+i*2,parent[0][1]+j*2,who):
                        sussesor.append([(parent[0][0]+i*2,parent[0][1]+j*2),(parent[0][0]+i,parent[0][1]+j),parent])
            elif state[parent[0][0]][parent[0][1]].king==True:
                for i in [-1,1]:
                    for j in [-1,1]:
                        if board.jump(state,parent[0][0],parent[0][1],parent[0][0]+i,parent[0][1]+j,parent[0][0]+i*2,parent[0][1]+j*2,who):
                            sussesor.append([(parent[0][0]+i*2,parent[0][1]+j*2),(parent[0][0]+i,parent[0][1]+j),parent])
        if who=='AI':


            if state[parent[0][0]][parent[0][1]].king==False:
                # AI's jumping directions are not consistent
                i=1
                for j in [-1,1]:
                    if board.jump(state,parent[0][0],parent[0][1],parent[0][0]+i,parent[0][1]+j,parent[0][0]+i*2,parent[0][1]+j*2,who):
                        sussesor.append([(parent[0][0]+i*2,parent[0][1]+j*2),(parent[0][0]+i,parent[0][1]+j),parent])
            elif state[parent[0][0]][parent[0][1]].king==True:
                for i in [-1,1]:
                    for j in [-1,1]:
                        if board.jump(state,parent[0][0],parent[0][1],parent[0][0]+i,parent[0][1]+j,parent[0][0]+i*2,parent[0][1]+j*2,who):
                            sussesor.append([(parent[0][0]+i*2,parent[0][1]+j*2),(parent[0][0]+i,parent[0][1]+j),parent])
        # Return all positions where you can jump
        return sussesor

    @staticmethod
    def jumps(state, row, col, who):
        current2 = deepcopy(state)
        ss = []
        # ss stores the corresponding state (ie chessboard)
        ss.append(deepcopy(state))
        waiting = [[(row, col), None, None]]
        res = []
        # Use two lists for depth-first search to achieve multiple jumps
        while waiting:
            cu = waiting[-1]
            # The last element of the list is called each time to implement a depth-first search
            if cu[2] != None:
                if current2[cu[1][0]][cu[1][1]].king:
                    # Detect whether the action of killing kings is performed,
                    # if there is, the next jump search will not be performed
                    current2[cu[1][0]][cu[1][1]] = 0
                    current2[cu[0][0]][cu[0][1]], current2[cu[2][0][0]][cu[2][0][1]] = current2[cu[2][0][0]][cu[2][0][1]], current2[cu[0][0]][cu[0][1]]
                    current2[cu[0][0]][cu[0][1]].beking()
                    ss.append(deepcopy(current2))
                    sus=[]
                else:
                    current2[cu[1][0]][cu[1][1]] = 0
                    current2[cu[0][0]][cu[0][1]], current2[cu[2][0][0]][cu[2][0][1]] = current2[cu[2][0][0]][cu[2][0][1]], current2[cu[0][0]][cu[0][1]]
                    ss.append(deepcopy(current2))
                    sus = board.jumpcu(ss[-1], cu, who)
            else:
                # Use the state transition function to continue the search
                # (only search for jump actions)
                sus = board.jumpcu(ss[-1], cu, who)

            if len(sus) > 0:
                # If you can jump again,
                # save the next state to the waiting list and delete the current state
                for i in sus:
                    waiting.append(i)
                waiting.remove(cu)
            elif len(sus) == 0:
                if len(waiting)>1:
                    n1 = 0
                    p1 = cu[-1]
                    while p1 != None:
                        p1 = p1[-1]
                        n1 += 1
                    n2=0
                    p2=waiting[-2][-1]
                    while p2 != None:
                        p2 = p2[-1]
                        n2 += 1

                    # If the next executable jump action is not found,
                    # the board will be restored to its previous state
                    # (you need to calculate a total of several jumps),
                    # and delete the board that was saved later
                    for i in range(n1-n2+1):
                        ss.pop()
                    waiting.remove(cu)
                    res.append(cu)
                else:
                    waiting.remove(cu)
                    res.append(cu)
                # Extract the restored chessboard
                current2 = deepcopy(ss[-1])
        #     Prevent the initial state from being stored
        if [(row, col), None, None] in res:
            res.remove([(row, col), None, None])
        return res

    @staticmethod
    # Print the chessboard in the terminal
    def printbo(state):
        for i in range(8):
            for j in range(8):
                if state[i][j]==0:
                    print('---',end='')
                elif state[i][j].color=='AI':
                    print('AI ', end='')
                elif state[i][j].color=='Player':
                    print('Pl  ', end='')
            print()


    @staticmethod
    def find_all_available_jump(state,row,col,who):
        # Find all the positions where a chess piece can jump,
        # and the return value is the final position and the captured position, and split
        res=board.jumps(state,row,col,who)
        new=board.get_new(res)
        via=board.get_via(res)
        return new,via

    @staticmethod
    def find_all_available_move(state,row,col,who):
        # Find all pieces that can be moved (non-jumping)
        available=[]
        m = row
        n = col
        if who=='Player':

            if state[m][n].color == who and state[m][n].king==False:
                        if board.move(state,m,n,m-1,n+1,who):
                            available.append([m-1,n+1])
                        if board.move(state,m,n,m-1,n-1,who):
                            available.append([m-1,n-1])
            elif state[m][n].color == who and state[m][n].king == True:
                        if board.move(state,m, n, m - 1, n + 1, who):
                            available.append([m - 1, n + 1])
                        if board.move(state,m, n, m - 1, n - 1, who):
                            available.append([ m - 1, n - 1])
                        if board.move(state,m, n, m + 1, n + 1, who):
                            available.append([ m +1, n + 1])
                        if board.move(state,m, n, m +1, n - 1, who):
                            available.append([ m + 1, n - 1])
        if who == 'AI':

            if state[m][n].color == who and state[m][n].king==False:
                        if board.move(state,m,n,m+1,n+1,who):
                            available.append([m+1,n+1])
                        if board.move(state,m,n,m+1,n-1,who):
                            available.append([m+1,n-1])
            elif state[m][n].color == who and state[m][n].king == True:
                        if board.move(state,m, n, m - 1, n + 1, who):
                            available.append([ m - 1, n + 1])
                        if board.move(state,m, n, m - 1, n - 1, who):
                            available.append([ m - 1, n - 1])
                        if board.move(state,m, n, m + 1, n + 1, who):
                            available.append([ m +1, n + 1])
                        if board.move(state,m, n, m +1, n - 1, who):
                            available.append([ m + 1, n - 1])
        return available
    @staticmethod
    def find_onechecker_all_action(state,row,col,who):
        # Search for moving and jumping actions separately
        available_move=board.find_all_available_move(state,row,col,who)
        available_jump=board.find_all_available_jump(state,row,col,who)
        #If there is a jumping action,
        # only return the jumping pieces to achieve the purpose of compulsory jumping
        if len(available_jump[0])>0:
            return available_jump,'jump'
        else:
            return available_move,'move'


    @staticmethod
    def check_can_move(state,who):
        # Search for the pieces on the entire board, check which pieces can move (movement and jump)
        can_move=[]
        for i in range(8):
            for j in range(8):
                if state[i][j]!=0:
                    if who=='Player' and state[i][j].color=='Player'  :
                        if state[i][j].king==False:

                            if board.jump(state,i,j,i-1,j-1,i-2,j-2,who) or board.jump(state,i,j,i-1,j+1,i-2,j+2,who):
                                can_move.append((i, j,'jump'))
                            elif board.move(state,i,j,i-1,j+1,who) or board.move(state,i,j,i-1,j-1,who):
                                can_move.append((i,j,'move'))
                        elif state[i][j].king==True:

                            if board.jump(state,i,j,i-1,j-1,i-2,j-2,who) or board.jump(state,i,j,i-1,j+1,i-2,j+2,who) or board.jump(state,i,j,i+1,j+1,i+2,j+2,who) or board.jump(state,i,j,i+1,j-1,i+2,j-2,who):
                                can_move.append((i, j,'jump'))
                            elif board.move(state,i,j,i-1,j+1,who) or board.move(state,i,j,i-1,j-1,who) or board.move(state,i,j,i+1,j-1,who) or board.move(state,i,j,i+1,j+1,who):
                                can_move.append((i,j,'move'))
                    if who=='AI' and state[i][j].color=='AI'  :
                        if state[i][j].king==False:

                            if board.jump(state,i,j,i+1,j-1,i+2,j-2,who) or board.jump(state,i,j,i+1,j+1,i+2,j+2,who):
                                can_move.append((i, j,'jump'))
                            elif board.move(state,i,j,i+1,j+1,who) or board.move(state,i,j,i+1,j-1,who):
                                can_move.append((i,j,'move'))
                        elif state[i][j].king==True:

                            if board.jump(state,i,j,i-1,j-1,i-2,j-2,who) or board.jump(state,i,j,i-1,j+1,i-2,j+2,who) or board.jump(state,i,j,i+1,j+1,i+2,j+2,who) or board.jump(state,i,j,i+1,j-1,i+2,j-2,who):
                                can_move.append((i, j,'jump'))
                            elif board.move(state,i,j,i-1,j+1,who) or board.move(state,i,j,i-1,j-1,who) or board.move(state,i,j,i+1,j-1,who) or board.move(state,i,j,i+1,j+1,who):
                                can_move.append((i,j,'move'))

        return can_move

    @staticmethod
    def find_allchecker_all_action(state,who):
        children=[]
        jum=0
        current=deepcopy(state)
        can_move=board.check_can_move(current,who)
        # For pieces that can be moved, find the actions they can perform,
        # and delete the move if they can jump
        for sss in can_move:
            if sss[-1]=='jump':
                jum=1
                break

        for i,j,k in can_move:
            if jum==1 and k=='move':
                continue
            available=board.find_onechecker_all_action(current,i,j,who)
            new = []
            via = []

            if available[-1]=='move' :
                for i1 in available[0]:
                    current1 = deepcopy(current)

                    current1[i][j], current1[i1[0]][i1[1]] = current1[i1[0]][i1[1]], current1[i][j]
                    children.append(current1)

            elif available[-1]=='jump':

                new=available[0][0]
                via=available[0][1]

                for i1 in range(len(new)):
                    current1 = deepcopy(current)
                    current1[i][j], current1[new[i1][0]][new[i1][1]] =  current1[new[i1][0]][new[i1][1]], current1[i][j]
                    for i2 in range(len(via[i1])):
                        current1[via[i1][i2][0]][via[i1][i2][1]]=0
                    children.append(current1)

        # Put the chessboard after the action is completed into the list and return
        return children

    @staticmethod
    def check(row,col,res):
        # Check whether the input coordinates are in the corresponding list
        # (whether actions can be taken)
        a = [row, col]
        if a in res:
            return True
        a = (row, col)
        if a in res:
            return True
        return False



    @staticmethod
    def get_via(res):
        # Process the captured pieces and extract them
        via=[]
        for i in range(len(res)):
            node=[]
            node.append(res[i][1])
            p=res[i][-1]
            while p[1]!=None:
                node.append(p[1])
                p=p[-1]
            via.append(node)
        return via


    @staticmethod
    def get_new(res):
        # Process the pieces that reach the new coordinates and extract them
        new=[]
        for i in range(len(res)):
            new.append(res[i][0])
        return new


    @staticmethod
    def _move(state,row1,col1,row2,col2):
        # Move the pieces on the chessboard
        state[row1][col1],state[row2][col2]=state[row2][col2],state[row1][col1]
        state[row2][col2].move(row2,col2)

    @staticmethod
    def _remove(state,via):
        # Delete a chess piece at a certain coordinate
        sign=0
        for i,j in via:
            if state[i][j].king:
                sign=1
            state[i][j]=0
        return sign

    @staticmethod
    def do(state,row1,col1,row2,col2):
        # Pass in two sets of coordinates, check whether the corresponding action can be performed,
        # and if it is correct, execute the action (used for the user's movement)

        can_move= board.check_can_move(state,'Player')
        sign=0
        for i in range(len(can_move)):
            if can_move[i][2]=='jump':
                sign=1
                break

        if sign==0:
            can_move=[(x,y) for x,y,z in can_move]
            print('you can chose these position to move:',can_move)

        elif sign==1:
            can_move = [(x, y)  for x, y, z in can_move if z=='jump']
            print('Forced jump!!,  you can chose these position to jump:', can_move)


        while True:
            if (row1,col1) not in can_move:
                print('illge input')
                break
            else:
                print('sucessfully input')
                break
        actions=board.find_onechecker_all_action(state,row1,col1,'Player')
        print('you can move or jump:',actions[0])

        if actions[-1]=='move':
            if board.check(row2,col2,actions[0]):
                board._move(state,row1,col1,row2,col2)
                print('ok')
            else:
                print('illegle,move')

        elif actions[-1]=='jump':

            if board.check(row2, col2, actions[0][0]):

                board._move(state,row1,col1,row2,col2)
                a=actions[0][0].index((row2,col2))
                sign=board._remove(state,actions[0][1][a])
                if sign==1:
                    state[row2][col2].beking()
                print('ok')
            else:
                print('illegle,jump')
        # After the execution is complete,
        # check whether there is a chess piece that can become a king
        board.check_beking(state)

    @staticmethod
    def evl(state):
        # Evaluate the current state
        pn=0
        for i in range(8):
            for j in range(8):
                if state[i][j]!=0:
                    pn+=1
        sorce = 0
        # If the total number of chess pieces is greater than 10, a simple evaluation is made,
        # that is, our side gets 2 points for the king and the opponent's king -2 points,
        # our ordinary pieces get 1 point, and the enemy's ordinary pieces get -1 point.
        if pn >10    :


            for i in range(8):
                for j in range(8):
                    if state[i][j]==0:
                        continue
                    elif state[i][j].color=='Player' :
                        if state[i][j].king==True:
                            sorce+=2
                        else :
                            sorce+=1
                    elif state[i][j].color == 'AI':
                        if state[i][j].king == True:
                            sorce -= 2
                        else:
                            sorce -= 1
            #    If the total number of chess pieces is less than 10,
            #    the points will be scored according to the position of the chess pieces
            else:
                for i in range(8):
                    for j in range(8):
                        if state[i][j] == 0:
                            continue
                        elif state[i][j].color == 'Player':
                            if state[i][j].king == True:
                                sorce += 15
                            else:
                                sorce += 1
                                sorce += (8-i)
                        elif state[i][j].color == 'AI':
                            if state[i][j].king == True:
                                sorce -= 15
                            else:
                                sorce -= 1
                                sorce -= i
        return sorce

    @staticmethod
    def check_beking(state):
        # Check whether the pieces on the chessboard meet the conditions of the king
        for i in range(8):
            for j in range(8):
                if state[i][j]!=0:
                    if state[i][j].color=='Player' and i==0:
                        state[i][j].beking()
                    elif state[i][j].color=='AI' and i==7:
                        state[i][j].beking()




    def pos(self):
        # Check the current state of the board
        self.AI_number=0
        self.AI_king=0
        self.player_number=0
        self.player_king=0
        for i in range(8):
            for j in range(8):
                if self.state[i][j]!=0:
                    if self.state[i][j].color=='AI':
                        self.AI_number+=1
                        if self.state[i][j].king==True:
                            self.AI_king+=1
                    elif self.state[i][j].color=='Player':
                        self.player_number +=1
                        if self.state[i][j].king==True:
                            self.player_king+=1


    @staticmethod
    def minimax(state, depth, alpha, beta, who):
        # Max min algorithm
        if depth == 0:
            # Scoring after reaching the leaf node
            return board.evl(state)
        current_state = (deepcopy(state))
        if who == 'Player':
            # Set the maximum value to the worst case
            max_eval = -math.inf
            for child in board.find_allchecker_all_action(current_state,'Player'):
                # Get every possible situation
                board.check_beking(child)
                # Check if a piece becomes the king
                ev = board.minimax(child, depth - 1, alpha, beta, 'AI')
                # Continue to find the next level
                max_eval = max(max_eval, ev)
                # Modify the maximum value
                alpha = max(alpha, ev)
                # Prune if α>β
                if beta <= alpha:
                    break

            return max_eval
        else:
            # The process is the same as above
            min_eval = math.inf
            for child in board.find_allchecker_all_action(current_state,'AI'):
                board.check_beking(child)
                ev = board.minimax(child, depth - 1, alpha, beta, 'Player')
                min_eval = min(min_eval, ev)
                beta = min(beta, ev)
                if beta <= alpha:
                    break

            return min_eval

    def evaluate_states(self):
        # AI's action process
        t1 = time.time()
        current_state = deepcopy(self.state)
        # First find the pieces that can be moved and the corresponding actions
        first_computer_moves = board.find_allchecker_all_action(current_state,'AI')
        # End if there is nothing to move
        if len(first_computer_moves) == 0:
            if self.player_number > self.AI_number:
                print(
                      "Computer has no available moves left, and you have more pieces left.\nYOU WIN!"  )
                exit()
            else:
                print( "Computer has no available moves left.\nGAME ENDED!" )
                exit()
        dict = {}
        for i in range(len(first_computer_moves)):
            # Use the maximum minimum algorithm to pingfen every possible action
            child = first_computer_moves[i]
            value = self.minimax(child, self.depth, -math.inf, math.inf, 'Player' )

            dict[value] = child
        if len(dict.keys()) == 0:
            print( + "Computer has cornered itself.\nYOU WIN!" )
            exit()
        #     And choose the best move (AI pieces are scored with negative numbers)
        new_board = dict[min(dict)]

        self.state = new_board
        t2 = time.time()
        diff = t2 - t1

        print("It took him " + str(diff) + " seconds.")

    # def play(self):
    #     print( "##### WELCOME TO CHECKERS ####" )
    #     print("\nSome basic rules:")
    #     print("1.You enter the coordinates in the form i,j.")
    #     print("2.You can quit the game at any time by pressing enter.")
    #     print("3.You can surrender at any time by pressing 's'.")
    #     print("Now that you've familiarized yourself with the rules, enjoy!")
    #
    #     answer = input("\ndo you want first? [y/n]")
    #
    #     if answer == "y":
    #         self.player_turn=True
    #     elif answer == "n":
    #         self.player_turn = False
    #     else:
    #         print( "Illegal input!, you first " )
    #         self.player_turn = True
    #     self.printbo(self.state)
    #     while True:
    #
    #
    #         if self.player_turn is True:
    #             print("\nPlayer's turn." )
    #             self.do(self.state)
    #             self.check_beking(self.state)
    #             self.pos()
    #             self.printbo(self.state)
    #         else:
    #             print( "Computer's turn." )
    #             print("Thinking...")
    #             self.evaluate_states()
    #             self.check_beking(self.state)
    #             self.pos()
    #             self.printbo(self.state)
    #
    #         if self.player_number == 0:
    #             self.printbo(self.state)
    #             print( "You have no pieces left.\nYOU LOSE!" )
    #             exit()
    #         elif self.AI_number == 0:
    #             self.printbo(self.state)
    #             print( "Computer has no pieces left.\nYOU WIN!" )
    #             exit()
    #         elif self.player_number - self.AI_number == 7:
    #             wish = input("You have 7 pieces fewer than your opponent.Do you want to surrender?")
    #             if wish == "" or wish == "yes":
    #                 print( "Coward." )
    #                 exit()
    #         self.player_turn = not self.player_turn

# B=board()
# B.play()
















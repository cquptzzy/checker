class piece:

    def __init__(self,row,col,color):
        self.row=row
        self.col=col
        self.color=color
        self.king=False

    def beking(self):
        self.king=True

    def getloac(self):
        return (self.row,self.col)

    def move(self,row,col):
        self.col=col
        self.row=row


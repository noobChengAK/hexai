import itertools
from Aiagent import NaiveAgent

class QueenbeeAgent():
    
    def __init__(self, board_size=11, M=100):
        self.board_size = board_size
        self.board = [[0] * 11 for i in range(10)]
        self.redtop = [[float("inf")]*board_size for i in range(board_size)]
        self.redbottom = [[float("inf")]*board_size for i in range(board_size)]
        self.blueleft = [[float("inf")]*board_size for i in range(board_size)]
        self.blueright = [[float("inf")]*board_size for i in range(board_size)]
        self.redpotentials = [[float("inf")]*board_size for i in range(board_size)]
        self.bluepotentials = [[float("inf")]*board_size for i in range(board_size)]
        self.total_potentials = [[float("inf")]*board_size for i in range(board_size)]
        self.red_board_potential = float("inf")
        self.blue_board_potential = float("inf")
        self.blue_attack_mobility = 0
        self.red_attack_mobility = 0
        self.M = M
        self.static_evaluation_value = 0
        self.visited = []
        self.next = []
        self.done = []
        self.notinit = True
    

    def evaluate(self, board=[[0] * 11 for i in range(10)]):
        """ Run all calculations on the given board and store results in instance variables.
            Can remove some variables like self.redtop, self.redpotentials, etc.
            which are not used in the ab-pruning later. Keeping them for debugging purposes.
        """
        self.board = board
        #print("---------------------------------------------------------")
        #print('Evaluating board:', self.board)
        # This defines the blue left:
        i = 0
        j = 0
        while self.notinit:
            if self.board[i][j] == 0:
                bl = self.e_blueleft(i,j)
                if bl != float("inf"):
                    self.notinit = False
                    self.blueleft[i][j] = bl
                    self.done.append((i,j))
            else:
                if i<self.board_size-1:
                    i+=1
                else:
                    i=0
                    j+=1
            if j==self.board_size-1:
                break
        while self.next != []:
                n = self.next[0]
                n1,n2 = n
                self.next.remove(n)
                if (self.board[n1][n2] == 0):
                    bl = self.e_blueleft(n1,n2)
                    self.blueleft[n1][n2] = bl
                    if (bl != float("inf"))&(n not in self.done):
                        self.done.append(n)                
                # #print("N: ",n)
                # #print("BL: ",self.blueleft)
                # #print("Next: ",self.next)
                # #print("Done: ",self.done)      
        #print("FINAL BL: ",self.blueleft)
        # This defines the blue right:
        self.next=[]
        self.done=[]
        self.notinit=True
        i = 0
        j = self.board_size-1        
        while self.notinit:
            if self.board[i][j] == 0:
                bl = self.e_blueright(i,j)
                if bl != float("inf"):
                    self.notinit = False
                    self.blueright[i][j] = bl
                    self.done.append((i,j))
            else:
                if i<self.board_size-1:
                    i+=1
                else:
                    i=0
                    j-=1
            if j==0:
                break
        while self.next != []:
                n = self.next[0]
                n1,n2 = n
                self.next.remove(n)
                if (self.board[n1][n2] == 0):
                    bl = self.e_blueright(n1,n2)
                    self.blueright[n1][n2] = bl
                    if (bl != float("inf"))&(n not in self.done):
                        self.done.append(n)                
                # #print("N: ",n)
                # #print("Neighbors: ",self.get_redneighbors(i,j))
                # #print("BR: ",self.blueright)
                # #print("Next: ",self.next)
                # #print("Done: ",self.done)      
        #print("FINAL BR: ",self.blueright)

        # This defines the red top:
        self.next=[]
        self.done=[]
        self.notinit=True
        i = 0
        j = 0       
        while self.notinit:
            if self.board[i][j] == 0:
                bl = self.e_redtop(i,j)
                if bl != float("inf"):
                    self.notinit = False
                    self.redtop[i][j] = bl
                    self.done.append((i,j))
            else:
                if j<self.board_size-1:
                    j+=1
                else:
                    j=0
                    i+=1
            if i==self.board_size:
                break
        while self.next != []:
                n = self.next[0]
                n1,n2 = n
                self.next.remove(n)
                if (self.board[n1][n2] == 0):
                    bl = self.e_redtop(n1,n2)
                    self.redtop[n1][n2] = bl
                    if (bl != float("inf"))&(n not in self.done):
                        self.done.append(n)                
                # #print("N: ",n)
                # #print("BL: ",self.blueleft)
                # #print("Next: ",self.next)
                # #print("Done: ",self.done)      
        #print("FINAL RT: ",self.redtop)              

        # This defines the red BOTTOM:
        self.next=[]
        self.done=[]
        self.notinit=True
        i = self.board_size-1
        j = 0        
        while self.notinit:
            if self.board[i][j] == 0:
                bl = self.e_redbottom(i,j)
                if bl != float("inf"):
                    self.notinit = False
                    self.redbottom[i][j] = bl
                    self.done.append((i,j))
            else:
                if j<self.board_size-1:
                    j+=1
                else:
                    j=0
                    i-=1
            if i==0:
                break
        while self.next != []:
                n = self.next[0]
                n1,n2 = n
                # #print("N: ",n)
                # #print("RB: ",self.redbottom)
                # #print("Next: ",self.next)
                # #print("Done: ",self.done) 
                self.next.remove(n)
                if (self.board[n1][n2] == 0):
                    bl = self.e_redbottom(n1,n2)
                    self.redbottom[n1][n2] = bl
                    if (bl != float("inf"))&(n not in self.done):
                        self.done.append(n)                
     
        #print("FINAL RB: ",self.redbottom)

        # Calculating potentials and attack mobility
        self.bluepotentials = self.calc_blue_potentials()
        #print("FINAL B_POTENTIALS: ", self.bluepotentials)

        self.redpotentials = self.calc_red_potentials()
        #print("FINAL R_POTENTIALS: ", self.redpotentials)

        self.total_potentials = self.calc_total_potentials()
        #print("FINAL TOTAL_POTENTIALS: ", self.total_potentials)

        self.blue_board_potential = min(itertools.chain.from_iterable(self.bluepotentials))
        if self.blue_board_potential == float("inf"):
            self.blue_board_potential = 1000
        #print("FINAL_BLUE_BOARD_POTENTIAL: ", self.blue_board_potential)

        self.red_board_potential = min(itertools.chain.from_iterable(self.redpotentials))
        if self.red_board_potential == float("inf"):
            self.red_board_potential = 1000
        #print("FINAL_RED_BOARD_POTENTIAL: ", self.red_board_potential)

        self.blue_attack_mobility = list(itertools.chain.from_iterable(self.bluepotentials)).count(self.blue_board_potential)
        #print("FINAL_BLUE_ATTACK_MOBILITY: ", self.blue_attack_mobility)

        self.red_attack_mobility = list(itertools.chain.from_iterable(self.redpotentials)).count(self.red_board_potential)
        #print("FINAL_RED_ATTACK_MOBILITY: ", self.red_attack_mobility)

        # Calculating the static evaluation function on pg40
        self.static_evaluation_value = self.calc_static_eval(M=self.M)
        #print("Static evaluation value: ", self.static_evaluation_value)

        #print()


    def e_redtop(self,i,j):
        connected = False
        if i==0:
            self.visited = [(i,j)]
            neighbors = self.get_redneighbors(i,j)
            for n in neighbors:
                if (n not in self.next)&(n not in self.done):
                    self.next.append(n)            
            val = 1
        else:
            self.visited = [(i,j)]
            neighbors = self.get_redneighbors(i,j)
            vs = []
            for n in neighbors:
                n1,n2=n
                v = self.redtop[n1][n2]
                if (n1 == 0)&(self.board[n1][n2] == 'R'):
                    connected = True                    
                vs.append(v)
            vs.sort()
            # #print(vs)
            if len(vs)>=2:
                val = vs[1] + 1
            else:
                val = float("inf")
            if connected == True:
                val = 1                 
            if val != float("inf"):
                for n in neighbors:
                    if (n not in self.next)&(n not in self.done):
                        self.next.append(n)                      
        return val 

    def e_redbottom(self,i,j):
        connected = False
        if i==self.board_size-1:
            self.visited = [(i,j)]
            neighbors = self.get_redneighbors(i,j)
            for n in neighbors:
                if (n not in self.next)&(n not in self.done):
                    self.next.append(n)            
            val = 1
        else:
            self.visited = [(i,j)]
            neighbors = self.get_redneighbors(i,j)
            # #print("neibors:",neighbors)
            vs = []
            for n in neighbors:
                n1,n2=n
                v = self.redbottom[n1][n2]
                if (n1 ==self.board_size -1)&(self.board[n1][n2] == 'R'):
                    connected = True                
                vs.append(v)
            vs.sort()
            # #print(vs)
            if len(vs)>=2:
                val = vs[1] + 1
            else:
                val = float("inf")
            if connected == True:
                val = 1
            if val != float("inf"):
                for n in neighbors:
                    if (n not in self.next)&(n not in self.done):
                        self.next.append(n)                      
        return val 


    def e_blueleft(self,i,j):
        connected = False
        if j==0:
            self.visited = [(i,j)]
            neighbors = self.get_blueneighbors(i,j)
            for n in neighbors:
                if (n not in self.next)&(n not in self.done):
                    self.next.append(n)            
            val = 1
        else:
            self.visited = [(i,j)]
            neighbors = self.get_blueneighbors(i,j)
            vs = []
            for n in neighbors:
                n1,n2=n
                v = self.blueleft[n1][n2]
                if (n2 ==0)&(self.board[n1][n2] == 'B'):
                    connected = True                    
                vs.append(v)
            vs.sort()
            # #print(vs)
            if len(vs)>=2:
                val = vs[1] + 1               
            else:
                val = float("inf")
            if connected == True:
                val = 1                 
            if val != float("inf"):
                for n in neighbors:
                    if (n not in self.next)&(n not in self.done):
                        self.next.append(n)                      
        return val 

    def e_blueright(self,i,j):
        connected = False
        if j==self.board_size-1:
            self.visited = [(i,j)]
            neighbors = self.get_blueneighbors(i,j)
            for n in neighbors:
                if (n not in self.next)&(n not in self.done):
                    self.next.append(n)            
            val = 1
        else:
            self.visited = [(i,j)]
            neighbors = self.get_blueneighbors(i,j)
            vs = []
            for n in neighbors:
                n1,n2=n
                v = self.blueright[n1][n2]
                if (n2 ==self.board_size -1)&(self.board[n1][n2] == 'B'):
                    connected = True                    
                vs.append(v)
            vs.sort()
            if len(vs)>=2:
                val = vs[1] + 1
            else:
                val = float("inf")
            if connected == True:
                val = 1
            # #print("now evaluating:",i,j)
            # #print("neighbors:",neighbors)
            # #print("value:",val)
            # #print("Connected: ", connected)          
            if val != float("inf"):
                for n in neighbors:
                    if (n not in self.next)&(n not in self.done):
                        self.next.append(n)                      
        return val  
        
    def get_redneighbors(self,i,j):
        neighbors = []
        ns = []
        # get adjacent neighbor,search order:clockwise at 12
        if (i-1 >=0):  
            if(self.board[i-1][j]!='B'):
                neighbors.append((i-1,j))
        if (i-1 >=0)&(j+1<self.board_size):
            if (self.board[i-1][j+1]!='B'):    
                neighbors.append((i-1,j+1))
        if (j+1<self.board_size):
            if(self.board[i][j+1]!='B'):
                neighbors.append((i,j+1))
        if (i+1 < self.board_size):
            if(self.board[i+1][j]!='B'):    
                neighbors.append((i+1,j))
        if (i+1 < self.board_size)&(j-1>=0):
            if(self.board[i+1][j-1]!='B'):
                neighbors.append((i+1,j-1))
        if (j-1 >=0):
            if (self.board[i][j-1]!='B'):
                neighbors.append((i,j-1))
        if (i==0 or i==self.board_size-1):
            for x in range(self.board_size):
                if (self.board[i][x]!='B'):
                    neighbors.append((i,x))
        
        for n in neighbors:
            n1,n2 = n
            value = self.board[n1][n2]
            if n not in self.visited:
                self.visited.append(n)
                if value == 'R':
                    if n not in self.done:
                        self.done.append(n)
                    ns.append(n)
                    ns += self.get_redneighbors(n1,n2)
                elif value == 'B':
                    if n not in self.done:
                        self.done.append(n)
                else:
                    ns.append(n)
        # #print("inside neighbor",ns)
        return ns


    def get_blueneighbors(self,i,j):
        neighbors = []
        ns = []
        # get adjacent neighbor,search order:clockwise at 12
        if (i-1 >=0):  
            if(self.board[i-1][j]!='R'):
                neighbors.append((i-1,j))
        if (i-1 >=0)&(j+1<self.board_size):
            if (self.board[i-1][j+1]!='R'):    
                neighbors.append((i-1,j+1))
        if (j+1<self.board_size):
            if(self.board[i][j+1]!='R'):
                neighbors.append((i,j+1))
        if (i+1 < self.board_size):
            if(self.board[i+1][j]!='R'):    
                neighbors.append((i+1,j))
        if (i+1 < self.board_size)&(j-1>=0):
            if(self.board[i+1][j-1]!='R'):
             neighbors.append((i+1,j-1))
        if (j-1 >=0):
            if (self.board[i][j-1]!='R'):
                neighbors.append((i,j-1))
        if (j==0 or j==self.board_size-1):
            for x in range(self.board_size):
                if (self.board[x][j]!='R'):
                    neighbors.append((x,j))
        # #print(neighbors)
        for n in neighbors:
            n1,n2 = n
            value = self.board[n1][n2]
            if n not in self.visited:
                self.visited.append(n)
                if value == 'B':
                    if n not in self.done:
                        self.done.append(n)
                    ns.append(n)
                    ns += self.get_blueneighbors(n1,n2)
                elif value == 'R':
                    if n not in self.done:
                        self.done.append(n)
                else:
                    ns.append(n)
        return ns


    def calc_red_potentials(self):
        res = [None for i in range(self.board_size)]
        for i in range(self.board_size):
            res[i] = [sum(x) for x in zip(self.redtop[i], self.redbottom[i])]
        return res

    def calc_blue_potentials(self):
        res = [None for i in range(self.board_size)]
        for i in range(self.board_size):
            res[i] = [sum(x) for x in zip(self.blueleft[i], self.blueright[i])]
        return res

    def calc_total_potentials(self):
        res = [None for i in range(self.board_size)]
        for i in range(self.board_size):
            res[i] = [sum(x) for x in zip(self.redpotentials[i], self.bluepotentials[i])]
        return res

    def calc_static_eval(self, M=100):
        return M * (self.blue_board_potential - self.red_board_potential) - (self.blue_attack_mobility - self.red_attack_mobility)
    

class QueenbeeAgentTest():
    """A class to see the results on different boards
    """
    # TODO: Add expected return values for tests

    def testBoardSimpleExample1(self):
        agent = QueenbeeAgent()
        board = [[0] * 5 for i in range(5)]
        board[1][2]="B"
        board[1][3]='B'
        agent.evaluate(board)


    def testBoardTwoBridge1(self):
        agent = QueenbeeAgent()
        board = [[0] * 5 for i in range(5)]
        # Based on Figure5.4-Pg41
        board[2][1]="B"
        board[3][1]="R"
        board[4][1]='R'
        board[1][3]='B'
        agent.evaluate(board)


    def testBoardTwoBridge2(self):
        agent = QueenbeeAgent()
        board = [[0] * 5 for i in range(5)]
        # Based on Figure5.3-Pg40
        board[1][4]="B"
        board[2][2]="B"
        board[3][1]='R'
        board[3][2]='R'
        agent.evaluate(board)

    def testBoardTwoBridge11(self):
        agent = QueenbeeAgent()
        board = [[0] * 11 for i in range(11)]
        board[4][4]="B"
        board[4][5]="R"
        board[4][8]="R"
        board[4][9]="B"
        board[5][5]="R"
        board[5][6]="R"
        board[5][7]="B"
        board[5][8]="B"
        board[5][9]="R"
        board[6][4]="B"
        board[6][5]="B"
        board[6][6]="B"
        board[6][7]="R"
        board[7][1]="B"
        board[7][2]="B"
        board[8][0]="B"
        board[8][1]="R"
        board[9][1]="R"
        board[10][1]="R"        
        agent.evaluate(board)

    def testBoard11size(self):
        agent = QueenbeeAgent()
        board = [[0] * 11 for i in range(11)]
        board[4][4]="B"
        board[4][5]="R"
        board[4][8]="R"
        board[4][9]="B"
        board[5][5]="R"
        board[5][6]="R"
        board[5][7]="B"
        board[5][8]="B"
        board[5][9]="R"
        board[6][4]="B"
        board[6][5]="B"
        board[6][6]="B"
        board[6][7]="R"
        board[7][1]="B"
        board[8][0]="B"
        board[8][1]="R"
        board[9][1]="R"       
        agent.evaluate(board)       

if __name__ == "__main__":
    testAgent = QueenbeeAgentTest()
    # testAgent.testBoardSimpleExample1()
    # testAgent.testBoardTwoBridge1()
    # testAgent.testBoardTwoBridge2()
    # testAgent.testBoardTwoBridge11()
    # testAgent.testBoard11size()

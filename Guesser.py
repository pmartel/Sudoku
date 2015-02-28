""" this holds the guessing part of the solver. """
class Guesser():
    possibilities = [] #array of all possibilites by cell
    # these two lists are treated as stacks guessIdx stores the cells guessed
    # guessStack holds the possible guesses for each guessIdx.
    guessIdx=[]
    guessStack=[]
    possibilities =[]
    
    def __init__(self, solver ):
        self.guessIdx =[]
        self.guessStack = []
        self.solver = solver
        #self.findPossibilities()
        pass

    def findPossibilities(self):
        ''' set up a list of all possibilities for the game as it is now '''
        self.possibilities = []
        game = self.solver.game
        for n in range(game.numCells):
            self.possibilities.append(self.solver.findOptions(n,1))
            pass
        pass
    
     def getGuesses(self):
        self.findPossibilities()
        bad = False 
        game = self.solver.game
        for n in range(game.numCells):
            o1 = possibilities[n]
            if len(o1) == 0:
                #bad value, try backing out
                print('no options for cell',n)
                bad = True
                break
            # if o1 is a singleton, the cell has a fixed value
            elif len(o1) > 1: 
                if len(o1) < len(opt):
                    opt = o1
                    shortest =n
                    pass
                pass
            pass
        # At this point, if bad is true, we have to back up. Otherwise, we
        # append to the
        return [bad, shortest, opt]
        pass
        

    

""" This  is the solver code that was in SudokuGame.  Making it a class
makes it easier to keep things like guess stacks arount """
import collections # for named tuples

class SudokuSolver():
    guessStack = []
    def __init__(self,game):
        self.game=game

    def guessingSolve(self):
        game = self.game
        guessStack=[]
        idxStack=[]
        bad = False
        print('guessing solver')
        while True:
            # try the deterministic solver
            game.solve()
            blanks = game.countEmpty()
            if blanks == 0:
                break
            # find the shortest options list.  If there's a cell with an empty list
            # the game is bad, retry.  A singleton list doesn't count; that's just
            # a filled cell
            opt = game.digList
            cells = game.cell
            for n in range(game.numCells):
                o1 = game.findOptions(n,1)
                if len(o1) == 0:
                    #bad value, try backing out
                    print('no options for cell',n)
                    bad = True
                    break
                elif len(o1) > 1: 
                    if len(o1) < len(opt):
                        opt = o1
                        shortest =n
                        pass
                pass
            if bad:
                break
            #this might go into a structure or class, but for now, two lists
            guessStack.append(opt)
            idxStack.append(shortest)
            # now take the last element in idxStack as a cell,
            # and the first element of the last element of guessStack and
            # put it into the cell
            print( 'guessing cell',n,'is',opt[0])
            cells[shortest].setv(opt[0])
    
    
    pass

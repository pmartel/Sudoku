"""Display the sudoku to the console using unicode box characters.
    which are '\u2500 to '\u257f  A pdf is in the directory above this."""

# these tubles have the left, character space, internal line, heavy line
# and right symbols
topLine = ( '\u250f', '\u2501', '\u252f', '\u2533', '\u2513' )
charLine = ('\u2503', ' ','\u2502', '\u2503', '\u2503'  )
lightLine = ('\u2520', '\u2500','\u253c','\u2542','\u2528')
heavyLine = ('\u2523', '\u2501','\u253f','\u254b','\u252b')
botLine = ('\u2517','\u2501','\u2537','\u253b','\u251b')

testData = '123456789'

def pr(s):
    print(s,end="")

def fixedLine( lineArr, n ):
    pr(lineArr[0])
    for c in range(n):
        for c1 in range(n):
            pr(lineArr[1])
            if c1 < n-1:
                pr(lineArr[2])
            elif c < n-1:
                pr(lineArr[3])
            else:
                pr(lineArr[4])
    print('')
    
def varLine( lineArr, data, n ):
    pr(lineArr[0])
    for c in range(n):
        for c1 in range(n):
            pr(data[c*n+c1])
            if c1 < n-1:
                pr(lineArr[2])
            elif c < n-1:
                pr(lineArr[3])
            else:
                pr(lineArr[4])
    print('')
    
def BoxPrint( n = 3 ) :
    """ draw an n^2 x n^2 box """
    #top line
    fixedLine(topLine,n)
    # middle lines
    for r in range(n):
        for r1 in range(n):
            varLine(charLine, testData,n)
    #bottom line
    fixedLine(botLine,n)
    
    
            

BoxPrint()

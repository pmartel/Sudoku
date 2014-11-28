"""Display the sudoku to the console using unicode box characters.
    which are '\u2500 to '\u257f  A pdf describing them
    is in the directory above this,
    C:\Users\Phil\Desktop\Computer Languages\Python."""

# these tubles have the left, character space, internal line, heavy line
# and right symbols

#Bote the 'heavy-line' symbols are too wide.  the 'double-line' version works 
topLine = ( '\u2554', '\u2550', '\u2564', '\u2566', '\u2557' )
charLine = ('\u2551', ' ','\u2502', '\u2551', '\u2551'  )
lightLine = ('\u255f', '\u2500','\u253c','\u256b','\u2562')
heavyLine = ('\u2560', '\u2550','\u256a','\u256c','\u2563')
botLine = ('\u255a','\u2550','\u2567','\u2569','\u255d')


def pr(s):
    print(s,end="")

def prsp(s):
    print(s,end=" ")

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
    
def BoxPrint( data, n = 3 ) :
    """ draw an n^2 x n^2 box and fill it from the n^2 list of n^2
        length strings 'data' """
    #top line
    fixedLine(topLine,n)
    # middle lines
    for r in range(n):
        for r1 in range(n):
            row = r * n + r1
            varLine(charLine, data[row],n)
            if r1 < n-1:
                fixedLine(lightLine,n)
            elif r < n-1:
                fixedLine(heavyLine,n)
            else:
                #bottom line
                fixedLine(botLine,n)
                
    
    
            
if __name__ == '__main__':
    testData = ['1234','4321','2143','4123']
    BoxPrint(testData,2)

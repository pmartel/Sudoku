""" test how to get row.col from box"""
for b in range(9):
	print('b',b)
	print('row',(b//3)*3)
	print('col',(b*3)%9)

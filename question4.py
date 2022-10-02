
from tempfile import tempdir


class node:
    def __init__(self, top, right,bottom,left) -> None:
        self.top = top
        self.right = right
        self.bottom = bottom
        self. left = left
        self.heuristic = min(top,left,right,bottom)
        self.link = []
        self.open = [True,True,True,True]
    def print(self):
        print(self.top,self.right,self.bottom,self.left)
paired_values = []
container = []
with open('input.txt') as topo_file:
    count = 0
    for line in topo_file:
        if count == 0:
            n,m = map(int, line.strip().split(' '))
           
        else:
            top,right,bottom,left = map(int, line.strip().split(' '))
            paired_values = paired_values + [top,right,bottom,left]
            container.append(node(top, right,bottom,left))
        count = count + 1
board = [[0 for x in range(m)] for y in range(n)]



print(n)
print(m)
for item in container:
    item.print()

for item in board:
    print(item)


unique_values = []
for value in paired_values:
    if paired_values.count(value) == 1:
        unique_values.append(value)
heuristic_values = [x for x in paired_values if x not in unique_values]
heuristic_values = set(heuristic_values)
print(heuristic_values)
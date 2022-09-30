
class node:
    def __init__(self, top, right,bottom,left) -> None:
        self.top = top
        self.right = right
        self.bottom = bottom
        self. left = left
    def print(self):
        print(self.top,self.right,self.bottom,self.left)

container = []
with open('input.txt') as topo_file:
    count = 0
    for line in topo_file:
        if count == 0:
            n,m = map(int, line.strip().split(' '))
           
        else:
            top,right,bottom,left = map(int, line.strip().split(' '))
            container.append(node(top, right,bottom,left))
        count = count + 1
bored = [[0 for x in range(m)] for y in range(n)]
print(n)
print(m)
bored[0][1] = 3
for item in container:
    item.print()

for item in bored:
    print(item)
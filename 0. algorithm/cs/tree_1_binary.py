import math


class Node:
    def __init__(self, item):
        self.item = item
        self.left = self.right = None


class BinaryTree:
    def __init__(self):
        self.root = None

    # 전위순회
    def preoder(self, n):
        if n:
            print(n.item, '', end='')
            if n.left:
                self.preoder(n.left)
            if n.right:
                self.preoder(n.right)

    # 중위순회
    def inoder(self, n):
        if n:
            if n.left:
                self.preoder(n.left)
            print(n.item, '', end='')
            if n.right:
                self.preoder(n.right)

    # 후위순회
    def postoder(self, n):
        if n:
            if n.left:
                self.preoder(n.left)
            if n.right:
                self.preoder(n.right)
            print(n.item, '', end='')

    # 레벨오더
    def levelorder(self):
        queue = [self.root]
        while queue:
            node = queue.pop(0)
            print(node.item, '', end='')
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

    # 트리 구성
    def addnode(self, n, index):

        if index == 1:
            self.root = n
        else:
            parent = self.getparent(index)
            mod = index % 2
            if mod == 0:
                parent.left = n
            else:
                parent.right = n

    # 부모노드 반환 레벨 오더로 부모를 찾아가는 concept
    def getparent(self, idx):
        pidx = math.trunc(idx/2)
        nowidx = 0
        queue = [self.root]
        while queue:

            node = queue.pop(0)
            nowidx = nowidx+1
            if nowidx == pidx:
                return node

            if node.left:
                queue.append(node.left)

            if node.right:
                queue.append(node.right)


if __name__ == '__main__':
    tree = BinaryTree()
    nodeList = [None, 10, 20, 30, 40, 50, 60, 70, 80]

    for i in range(len(nodeList)):
        tempItem = nodeList[i]
        if tempItem is None:
            continue
        tree.addnode(Node(tempItem), i)

    print("전위순회 : ", end='')
    tree.preoder(tree.root)
    print()

    print("중위순회 : ", end='')
    tree.inoder(tree.root)
    print()

    print("후위순회 : ", end='')
    tree.postoder(tree.root)
    print()

    print("레벨오더 : ", end='')
    tree.levelorder()

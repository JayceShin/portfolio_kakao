import math


class Node:
    def __init__(self, item):
        self.item = item
        self.left = self.right = None


class BST:
    def __init__(self):
        self.root = None

    def insert(self, n):

        if self.root:
            current = self.root
        else:
            self.root = n
            return

        while True:
            if n.item < current.item:
                # left
                if current.left:
                    current = current.left
                else:
                    current.left = n
                    break
            else:
                # right
                if current.right:
                    current = current.right
                else:
                    current.right = n
                    break

    def searchCount(self, value):

        ans = 0

        if self.root:
            current = self.root
        else:
            print("Not Node in tree")
            return 0

        while True:
            ans = ans + 1
            if current.item == value:
                return ans
            if current.left and value < current.item:
                current = current.left
            elif current.right and value > current.item:
                # right search
                current = current.right
            else:
                return 0

    def delete(self, value):
        if self.root:
            current = self.root
            grand = self.root
        else:
            print("Not Node in tree")
            return False

        while True:
            if current.item == value:
                if current.left and current.right:
                    # 노드 2개
                    parent = current
                    child = current.right

                    while child.left:
                        parent = child
                        child = parent.left

                    if grand.item > current.item:
                        grand.left = child
                    else:
                        grand.right = child

                    if child.right:
                        parent.left = child.right

                    child.left = current.left
                    return True

                elif current.left or current.right:
                    # 노드 1개
                    if current.left:
                        child = current.left
                    else:
                        child = current.right

                    if grand.item > current.item:
                        grand.left = child
                    else:
                        grand.right = child

                    return True

                else:
                    if grand.item > current.item:
                        grand.left = None
                    else:
                        grand.right = None

                    return True
            else:
                if current.item > value:
                    if current.left:
                        grand = current
                        current = current.left
                    else:
                        return False
                else:
                    if current.right:
                        grand = current
                        current = current.right
                    else:
                        return False


if __name__ == '__main__':
    nodeList = [1, 2, 15, 7, 11, 10, 12, 3, 4, 20]
    bst = BST()

    for i in range(len(nodeList)):
        bst.insert(Node(nodeList[i]))

    print(bst.searchCount(15))
    print(bst.delete(15))

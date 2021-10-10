import math


class Merge:
    def __init__(self, list):
        self.list = list

    def merge(self, left, mid, right):

        i = left
        j = mid+1
        start = left
        temp = [None for i in range(0, len(self.list))]

        while i <= mid and j <= right:
            if self.list[i] < self.list[j]:
                temp[start] = self.list[i]
                start = start + 1
                i = i + 1
            else:
                temp[start] = self.list[j]
                start = start+1
                j = j + 1

        while i == mid:
            temp[start] = self.list[i]
            i = i+1
            start = start+1

        while j == right:
            temp[start] = self.list[j]
            j = j+1
            start = start+1

        for i in range(len(temp)):
            if temp[i] is not None:
                self.list[i] = temp[i]

    def sort(self, left, right):
        # left right 같아지는 시점이 종료지점
        if left < right:
            mid = math.trunc((left + right)/2)
            self.sort(left, mid)
            self.sort(mid+1, right)
            self.merge(left, mid, right)


if __name__ == '__main__':
    a = [21, 10, 12, 20, 25, 13, 15, 22]
    merge = Merge(a)
    merge.sort(0, len(a)-1)
    print(a)

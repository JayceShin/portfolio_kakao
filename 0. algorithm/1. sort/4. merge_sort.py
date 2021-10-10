import math


class Merge:
    def __init__(self, array):
        self.array = array

    # point
    # 1. left(i)가 mid가 될 때 까지
    # 2. mid+1(j)이 right가 될 때 까지
    # 3. 변경 시작 지점(start)은 left
    # 4. 남아있는 것(i!=mid & j!=right)도 옮겨줌
    # 5. temp를 array에 덮어 씌움
    def merge(self, left, mid, right):

        i = left
        j = mid+1
        start = left
        temp = [None for i in range(0, len(self.array))]

        while i <= mid and j <= right:
            if self.array[i] < self.array[j]:
                temp[start] = self.array[i]
                start = start + 1
                i = i + 1
            else:
                temp[start] = self.array[j]
                start = start+1
                j = j + 1

        while i == mid:
            temp[start] = self.array[i]
            i = i+1
            start = start+1

        while j == right:
            temp[start] = self.array[j]
            j = j+1
            start = start+1

        for i in range(len(temp)):
            if temp[i] is not None:
                self.array[i] = temp[i]

    # point
    # left 먼저 쭉 내려 간 뒤에 right랑 하나씩 병합
    # 시간복잡도는 합병 단계수 * 비교
    # => O(nlogn)
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

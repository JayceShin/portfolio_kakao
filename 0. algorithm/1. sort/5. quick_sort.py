class Quick:
    def __init__(self, array):
        self.array = array

    def partition(self, low, high):
        pivot = self.array[(low + high) // 2]
        while low <= high:
            while self.array[low] < pivot:
                low += 1
            while self.array[high] > pivot:
                high -= 1
            if low <= high:
                self.swap(high, low)
                low, high = low + 1, high - 1
        return low

    # point
    def sort(self, left, right):
        if left < right:
            pivot = self.partition(left, right)
            self.sort(left, pivot-1)
            self.sort(pivot+1, right)

    # noinspection PyMethodMayBeStatic
    def swap(self, i, j):
        temp = self.array[i]
        self.array[i] = self.array[j]
        self.array[j] = temp


if __name__ == '__main__':
    a = [70, 20, 50, 10, 30, 40]
    quick = Quick(a)
    quick.sort(0, len(a)-1)
    print(a)

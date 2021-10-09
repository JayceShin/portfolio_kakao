class Bubble:
    def __init__(self):
        pass

    # point "처음 인덱스", "밀어"
    # 계속 "처음 인덱스"부터 시작하여 한칸씩 큰수/작은수를 뒤로 "밀어"낸다
    # outer : i = 0 to n-2
    # inner : j = 1 to n-1-i
    # compare : a[j-1] & a[j]
    # 모든 경우 다 돌기 때문에 시간복잡도 일정
    # => O(N^2)
    def sort(self, array, direction):
        if direction == "asc":
            for i in range(len(array)-1):
                for j in range(1, len(array)-i):
                    now = array[j-1]
                    compare = array[j]
                    if array[j-1] > array[j]:
                        self.swap(array, j-1, j)
        else:
            pass

    # noinspection PyMethodMayBeStatic
    def swap(self, array, i, j):
        temp = array[i]
        array[i] = array[j]
        array[j] = temp


if __name__ == '__main__':
    a = [2, 1, 5, 4, 3]
    bubble = Bubble()
    bubble.sort(a, "asc")
    print(a)

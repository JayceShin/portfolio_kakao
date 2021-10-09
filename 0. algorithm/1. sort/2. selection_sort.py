class Selction:
    def __init__(self):
        pass

    # point "최소/최대", "선택"
    # 배열의 처음부터 끝까지 돌며 값을 비교하여 최소/최대값을 "선택"하고 교환
    # 마지막 숫자는 이미 정렬되어 있음
    # 따라서 바깥쪽은 n-1번 루프
    # 최소/최대값을 "선택"하는 루프는 바깥쪽의 역순이기에 역시 n-1번 루프
    # 최소/최대값을 "선택"하기 위해 모든 경우를 따져야함 -> best, worst가 없이 동일
    # => O(N^2)
    def sort(self, array, direction):

        if direction == "asc":
            for i in range(0, len(array) - 1):
                now = array[i]
                minValue = 99999

                for j in range(i + 1, len(array)):
                    if array[j] < minValue:
                        idx = j
                        minValue = array[j]

                if now > minValue:
                    self.swap(array, i, idx)
        else:
            for i in range(0, len(array) - 1):
                now = array[i]
                maxValue = -99999

                for j in range(i + 1, len(array)):
                    if array[j] > maxValue:
                        idx = j
                        maxValue = array[j]

                if now < maxValue:
                    self.swap(array, i, idx)

    # noinspection PyMethodMayBeStatic
    def swap(self, array, i, j):
        temp = array[i]
        array[i] = array[j]
        array[j] = temp


if __name__ == '__main__':
    a = [2, 1, 5, 4, 3]
    selection = Selction()
    selection.sort(a, "asc")
    print(a)

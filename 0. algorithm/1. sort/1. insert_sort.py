class Insert:
    def __init__(self):
        pass

    # point "자기자리", "삽입", "앞이 정렬되었으면 그만"
    # 두번째 인자부터 한칸씩 앞이랑 비교하면서 "자기자리"를 찾아 "삽입"한다
    # 레코드 수가 적을 경우 구현이 쉬워 유리
    # 많은 레코드 이동을 포함하기에 레코드가 정렬되어있을때 유리
    # 이미 정렬되어 있을 경우 한번의 비교만 하면 됨 -> 바로 앞이 조건에 안맞으면 그 앞에도 안맞으니
    # => BEST O(N)
    # 최악은 역순일 경우 각 반복마다 비교 이동이 발생
    # => WORST O(N^2)
    def sort(self, array, direction):
        if direction == "asc":
            for i in range(1, len(array)):
                now = array[i]
                for j in range(1, i+1):
                    compare = array[i-j]
                    if now < compare:
                        self.swap(array, i-j, i-j+1)
                    else:
                        break
        else:
            for i in range(1, len(array)):
                now = array[i]
                for j in range(1, i+1):
                    compare = array[i-j]
                    if now > compare:
                        self.swap(array, i-j, i-j+1)
                    else:
                        break

    # noinspection PyMethodMayBeStatic
    def swap(self, array, i, j):
        temp = array[i]
        array[i] = array[j]
        array[j] = temp


if __name__ == '__main__':
    a = [2, 1, 5, 4, 3]
    insert = Insert()
    insert.sort(a, "asc")
    print(a)

from collections import deque


def solution(n, a, cards):
    ans = 0
    queue = deque()

    for i in range(n):

        if len(cards) == i:
            if i == a:
                queue.append(chr(0))
            break

        if i != a:
            queue.append(cards[i])
        else:
            queue.append(chr(0))
            queue.append(cards[i])

    match = int(len(queue)/2)
    nowgame = 0
    before = None

    while queue:

        if len(queue) == 1:
            break

        if match == nowgame:
            if len(queue) % 2 != 0:
                temp = queue.popleft()
                queue.append(temp)

            nowgame = 0
            match = int(len(queue)/2)
            continue
        
        nowcard = queue.popleft()
        nextcard = queue.popleft()

        if nowcard == nextcard:
            # 일반 카드가 비기면 둘다 빠짐
            continue
        else:
            # 무적 카드가 들어간 경우
            if nowcard == chr(0) or nextcard == chr(0):
                maxcard = max(nowcard, nextcard)
                winner = compete(maxcard, maxcard)

                if winner != before:
                    queue.append(chr(0))
                    before = winner
            else:
                # 일반 카드
                winner = compete(nowcard, nextcard)
                queue.append(winner)

        nowgame = nowgame + 1

    # 처음 케이스 빼줌
    return ans-1


# return Win Character
def compete(cfirst, cnext):

    result = abs(ord(cfirst)-ord(cnext))

    if result == 1:
        win = "R"
    elif result == 2:
        win = "P"
    elif result == 3:
        win = "S"
    else:
        if cfirst == "R":
            win = "P"
        elif cfirst == "S":
            win = "R"
        else:
            win = "S"
            
    return win


if __name__ == '__main__':
    people = 6
    me = 2
    cardInfo = "PPSRP"

    # R - S = 1/ -1 -> R = -1
    # R - P = 2/ -2 -> P = -2
    # P - S = 3/ -3 -> S = 3

    print(solution(people, me, cardInfo))

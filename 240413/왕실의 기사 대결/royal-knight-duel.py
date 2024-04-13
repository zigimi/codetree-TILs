import copy
from collections import deque
l, n, q = map(int, input().split())
mymap = []
mymapwithkisa = [[0 for _ in range(l)] for _ in range(l)]
idxs = [[0, 0] for _ in range(n+1)]
sizes = [[0, 0] for _ in range(n+1)]
ks = [0]
ksum = [0] * (n+1)
die = []
for _ in range(l):
    mymap.append(list(map(int, input().split())))

for i in range(n):
    r, c, h, w, k = map(int, input().split())
    r -= 1
    c -= 1
    for idx1 in range(h):
        for idx2 in range(w):
            mymapwithkisa[r+idx1][c+idx2] = i+1
    idxs[i+1] = [r, c]
    sizes[i+1] = [h, w]
    ks.append(k)

dirs = [[-1, 0], [0, 1], [1, 0], [0, -1]]
ends = [0, l-1, l-1, 0]
for _ in range(q):
    i, d = map(int, input().split())

    if i in die:
        continue

    # 기사 이동
    mymapwithkisacopy = [[0 for _ in range(l)] for _ in range(l)]
    idxscopy = copy.deepcopy(idxs)

    myq = deque()
    myq.append(i)
    # 박스 찾기
    check = [False] * (n+1)
    check[i] = True
    minmovex = idxs[i][0]
    minmovey = idxs[i][1]
    maxmovex = idxs[i][0] + sizes[i][0]
    maxmovey = idxs[i][1] + sizes[i][1]
    while myq:
        newi = myq.popleft()
        startx = idxs[newi][0]
        starty = idxs[newi][1]
        endx = startx + sizes[newi][0]
        endy = starty + sizes[newi][1]

        idxscopy[newi][0] += dirs[d][0]
        idxscopy[newi][1] += dirs[d][1]

        minmovex = min(minmovex, startx)
        minmovey = min(minmovey, starty)
        maxmovex = max(maxmovex, endx)
        maxmovey = max(maxmovey, endy)

        if d%2:
            for idx1 in range(ends[d], starty, -dirs[d][1]):
                for idx2 in range(startx, endx):
                    if mymapwithkisa[idx2][idx1] != 0 and mymapwithkisa[idx2][idx1] not in die and check[mymapwithkisa[idx2][idx1]] == False:
                        check[mymapwithkisa[idx2][idx1]] = True
                        myq.append(mymapwithkisa[idx2][idx1])
        else:
            for idx1 in range(ends[d], startx, -dirs[d][0]):
                for idx2 in range(starty, endy):
                    if mymapwithkisa[idx1][idx2] != 0 and mymapwithkisa[idx1][idx2] not in die and check[mymapwithkisa[idx1][idx2]] == False:
                        check[mymapwithkisa[idx1][idx2]] = True
                        myq.append(mymapwithkisa[idx1][idx2])

    # print(minmovex, minmovey, maxmovex, maxmovey)
    # 가능 여부

    # 2. 튀어 나가는 가
    if minmovex+dirs[d][0] < 0 or minmovey+dirs[d][1] < 0 or maxmovex+dirs[d][0] > l or maxmovey+dirs[d][1] > l:
        continue

    cant = False
    tmpks = [0] * (n+1)
    # 1. 벽이 있는 가
    for idx1 in range(minmovex, maxmovex):
        for idx2 in range(minmovey, maxmovey):
            nownum = mymapwithkisa[idx1][idx2]
            if nownum in die:
                continue
            if nownum != 0 and mymap[idx1+dirs[d][0]][idx2+dirs[d][1]] == 2:
                cant = True
                break
            # elif check[nownum] == True:
            #     if d%2 and nownum not in myin[idx1]:
            #         mymapwithkisacopy[idx1][idx2] = 0
            #         myin[idx1].append(nownum)
            #     elif d%2 == 0 and nownum not in myin[idx2]:
            #         mymapwithkisacopy[idx1][idx2] = 0
            #         myin[idx2].append(nownum)
            #     if nownum != i and mymap[idx1+dirs[d][0]][idx2+dirs[d][1]] == 1:
            #         tmpks[nownum] += 1
            #     mymapwithkisacopy[idx1+dirs[d][0]][idx2+dirs[d][1]] = nownum

        if cant:
            break
    if cant:
        # print(minmovex, minmovey, maxmovex, maxmovey)
        continue

    for k in range(1, n + 1):
        if check[k]:
            for idx1 in range(idxs[k][0], idxs[k][0]+sizes[k][0]):
                for idx2 in range(idxs[k][1], idxs[k][1]+sizes[k][1]):
                    if k != i and mymap[idx1 + dirs[d][0]][idx2 + dirs[d][1]] == 1:
                        tmpks[k] += 1
                    # mymapwithkisacopy[idx1][idx2] = 0
                    mymapwithkisacopy[idx1+dirs[d][0]][idx2+dirs[d][1]] = k
        else:
            for idx1 in range(idxs[k][0], idxs[k][0]+sizes[k][0]):
                for idx2 in range(idxs[k][1], idxs[k][1]+sizes[k][1]):
                    mymapwithkisacopy[idx1][idx2] = k

    # print(tmpks)
    for k in range(1, n+1):
        ks[k] -= tmpks[k]
        ksum[k] += tmpks[k]
        if ks[k] < 1:
            die.append(k)

    # if d%2:
    #     for idx in range(idxs[i][0], idxs[i][0]+sizes[i][0]):
    #         mymapwithkisacopy[idx][idxs[i][1]] = 0
    # else:
    #     for idx in range(idxs[i][1], idxs[i][1]+sizes[i][1]):
    #         mymapwithkisacopy[idxs[i][0]][idx] = 0

    mymapwithkisa = copy.deepcopy(mymapwithkisacopy)
    idxs = copy.deepcopy(idxscopy)

answer = 0
for i in range(1, n+1):
    if i not in die:
        answer += ksum[i]

print(answer)
    # check = [False] * (l+1)
    # moves = deque()
    # moves.append(i)
    # check[i] = True
    # while moves:
    #     tmpnum = moves.popleft()
    #     nowidx_from = [idxs[tmpnum][0]+dirs[d][0], idxs[tmpnum][1]+dirs[d][1]]
    #     nowidx_to = [nowidx_from[0] + sizes[tmpnum][0], nowidx_from[1] + sizes[tmpnum][1]]
    #     for idx1 in range(nowidx_from[0], nowidx_to[0] + 1):
    #         for idx2 in range(nowidx_from[1], nowidx_to[1] + 1):
    #             if not -1 < idx1 < l and -1 < idx2 < l:
    #                 cant = True
    #                 break
    #             newnum = mymapwithkisa[idx1][idx2]
    #             # 지도 업데이트
    #             if -1 < idx1-dirs[d][0] < l and -1 < idx2-dirs[d][1] < l:
    #                 mymapwithkisacopy[idx1][idx2] = mymapwithkisa[idx1-dirs[d][0]][idx2-dirs[d][1]]
    #             else:
    #                 mymapwithkisacopy[idx1][idx2] = 0
    #
    #             if newnum != 0 and check[newnum] == False:
    #                 check[newnum] = True
    #                 moves.append(newnum)
    #
    #
    # cant = False
    #
    # moves = deque()
    # for idx1 in range(nowidx_from[0], nowidx_to[0]+1):
    #     for idx2 in range(nowidx_from[1], nowidx_to[1]+1):
    #         moveidxx = idx1+dirs[d][0]
    #         moveidxy = idx2+dirs[d][1]
    #         moves.append([moveidxx, moveidxy])
    #
    # while moves:
    #     tmp = moves.popleft()
    #     moveidxx = tmp[0]
    #     moveidxy = tmp[1]
    #     if mymap[moveidxx][moveidxy] == 2:
    #         cant = True
    #         break
    #     if mymapwithkisa[moveidxx][moveidxy] != 0:
    #         newmoveidxx = moveidxx + dirs[d][0]
    #         newmoveidxy = moveidxy + dirs[d][1]
    #         moves.append([newmoveidxx, newmoveidxy])
    #         mymapwithkisacopy[newmoveidxx][newmoveidxy] = mymapwithkisa[moveidxx][moveidxy]
    #
    #
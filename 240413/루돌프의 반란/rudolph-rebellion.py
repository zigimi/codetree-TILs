import copy
from collections import deque
from collections import defaultdict
n, m, p, c, d = map(int, input().split())
rx, ry = map(int, input().split())
rx-=1
ry-=1
santas = {}
scores = {}
prefate = []
newfate = []
reverseSantas = defaultdict(int)
for i in range(p):
    num, sx, sy = map(int, input().split())
    santas[num] = [sx-1, sy-1]
    scores[num] = 0
    reverseSantas[(sx-1, sy-1)] = num

santas = dict(sorted(santas.items()))

for _ in range(m):
    prefate = newfate[:]
    newfate = []
    #루돌프
    mindist = n**2+n**2+1
    minx = n
    miny = n
    mins = -1
    for s in santas:
        tmpx = santas[s][0]
        tmpy = santas[s][1]
        tmpdist = (tmpx - rx)**2 + (tmpy - ry)**2
        if tmpdist < mindist:
            mindist = tmpdist
            mins = s
            minx = tmpx
            miny = tmpy
        elif tmpdist == mindist:
            if tmpx > minx:
                mindist = tmpdist
                mins = s
                minx = tmpx
                miny = tmpy
            elif tmpx == minx:
                if tmpy > miny:
                    mindist = tmpdist
                    mins = s
                    minx = tmpx
                    miny = tmpy
    if rx > minx:
        movex = -1
    elif minx > rx:
        movex = 1
    else:
        movex = 0
    if ry > miny:
        movey = -1
    elif miny > ry:
        movey = 1
    else:
        movey = 0

    rx += movex
    ry += movey

    # 충돌 - 루돌프
    smovex = movex*c
    smovey = movey*c
    fail = []
    for s in santas:
        sx = santas[s][0]
        sy = santas[s][1]
        if santas[s] == [rx, ry]:
            newfate.append(s)
            del reverseSantas[(sx, sy)]
            scores[s] += c
            newsx = sx+smovex
            newsy = sy+smovey
            if not (-1 < newsx < n and -1 < newsy < n):
                fail.append(s)
                continue
            elif reverseSantas[(newsx, newsy)] != 0:
                # 상호 작용
                tmps = s
                while [newsx, newsy] in santas.values():
                    tmpnum = reverseSantas[(newsx, newsy)]
                    reverseSantas[(newsx, newsy)] = tmps
                    santas[tmps] = [newsx, newsy]

                    newsx += movex
                    newsy += movey
                    tmps = tmpnum

                    if not (-1 < newsx < n and -1 < newsy < n):
                        fail.append(s)
                        break
                    elif reverseSantas[(newsx, newsy)] == 0:
                        santas[tmps] = [newsx, newsy]
                        reverseSantas[(newsx, newsy)] = tmps
                        break
            else:
                reverseSantas[(newsx, newsy)] = s
                santas[s] = [newsx, newsy]

    # print(santas)
    # 실패 산타 삭제
    for s in fail:
        del santas[s]

    if not santas:
        break

    fail = []

    # 산타의 움직임
    for s in santas:
        if s in prefate or s in newfate:
            continue
        mindist = n ** 2 + n ** 2 + 1
        minmove = [0, 0]
        tmpx = santas[s][0]
        tmpy = santas[s][1]

        if rx < tmpx and [tmpx-1, tmpy] not in santas.values():
            tmpdist = (rx-(tmpx-1))**2+(ry-tmpy)**2
            if tmpdist < mindist:
                mindist = tmpdist
                minmove = [-1, 0]
        if ry > tmpy and [tmpx, tmpy+1] not in santas.values():
            tmpdist = (rx - tmpx) ** 2 + (ry - (tmpy+1)) ** 2
            if tmpdist < mindist:
                mindist = tmpdist
                minmove = [0, 1]
        if rx > tmpx and [tmpx+1, tmpy] not in santas.values():
            tmpdist = (rx - (tmpx+1)) ** 2 + (ry - tmpy) ** 2
            if tmpdist < mindist:
                mindist = tmpdist
                minmove = [1, 0]
        if ry < tmpy and [tmpx, tmpy-1] not in santas.values():
            tmpdist = (rx - tmpx) ** 2 + (ry - (tmpy - 1)) ** 2
            if tmpdist < mindist:
                mindist = tmpdist
                minmove = [0, -1]

        santas[s] = [tmpx+minmove[0], tmpy+minmove[1]]

        # 충돌 - 산타
        del reverseSantas[(tmpx, tmpy)]
        if santas[s] == [rx, ry]:
            newfate.append(s)
            smovex = -minmove[0] * d
            smovey = -minmove[1] * d

            scores[s] += d
            newsx = rx + smovex
            newsy = ry + smovey
            if not (-1 < newsx < n and -1 < newsy < n):
                fail.append(s)
                continue
            elif reverseSantas[(newsx, newsy)] != 0:
                # 상호 작용
                tmps = s
                while [newsx, newsy] in santas.values():
                    tmpnum = reverseSantas[(newsx, newsy)]
                    reverseSantas[(newsx, newsy)] = tmps
                    santas[tmps] = [newsx, newsy]

                    newsx += -minmove[0]
                    newsy += -minmove[1]
                    tmps = tmpnum

                    if not (-1 < newsx < n and -1 < newsy < n):
                        fail.append(s)
                        break
                    elif reverseSantas[(newsx, newsy)] == 0:
                        santas[tmps] = [newsx, newsy]
                        reverseSantas[(newsx, newsy)] = tmps
                        break
            else:
                reverseSantas[(newsx, newsy)] = s
                santas[s] = [newsx, newsy]
        else:
            # del reverseSantas[(tmpx, tmpy)]
            reverseSantas[(tmpx+minmove[0], tmpy+minmove[1])] = s
        # print("after")
        # print(santas)

    # 실패 산타 삭제
    for s in fail:
        del santas[s]

    if not santas:
        break

    # 점수 부여
    for s in scores:
        if s in santas.keys():
            scores[s] += 1

    # print(fail)

    # print(movex, movey)

    # print(rx, ry)
    # print(santas)
    # print(scores)
keys = sorted(scores.keys())
for i in keys:
    print(scores[i], end=" ")
# print(scores.values())
# print(scores)
import copy
import heapq
n, m, k = map(int, input().split())
mymap = []
# attackpriority = []
# attackedpriority = []
# attack = {}
recent = {}
for i in range(n):
    mymap.append(list(map(int, input().split())))
    for j in range(m):
        if mymap[-1][j] != 0:
            recent[(i, j)] = -1

def dfs(i, j, dx, dy, dist, att, route):
    global mindist, minroute
    if mymap[i][j] == 0:
        return
    if i == dx and j == dy and mindist > dist:
        mindist = dist
        minroute = copy.deepcopy(route)
        return
    if check[i][j] == False:
        check[i][j] = True
        route.append([i, j])
        dfs(i, (j+1)%m, dx, dy, dist+1, att, route)
        dfs((i+1)%n, j, dx, dy, dist+1, att, route)
        dfs(i, (j-1+m)%m, dx, dy, dist+1, att, route)
        dfs((i-1+n) % n, j, dx, dy, dist+1, att, route)
        route.pop()
        check[i][j] = False

for i in range(k):
    attacked = []
    # 공격자 선정
    # tmp = heapq.heappop(attackpriority)
    tmpx = 0
    tmpy = 0
    minattack = 5001
    for j in range(n):
        for k in range(m):
            if mymap[j][k] > 0:
                if mymap[j][k] < minattack:
                    minattack = mymap[j][k]
                    tmpx = j
                    tmpy = k
                elif minattack == mymap[j][k]:
                    if recent[(j, k)] > recent[(tmpx, tmpy)]:
                        minattack = mymap[j][k]
                        tmpx = j
                        tmpy = k
                    elif recent[(j, k)] == recent[(tmpx, tmpy)]:
                        if j+k > tmpx+tmpy:
                            minattack = mymap[j][k]
                            tmpx = j
                            tmpy = k
                        elif j+k == tmpx+tmpy:
                            if k > tmpy:
                                minattack = mymap[j][k]
                                tmpx = j
                                tmpy = k
    mymap[tmpx][tmpy] += n+m
    recent[(tmpx, tmpy)] = i
    # tmp[0] += n+m
    # tmp[1] = -i
    # heapq.heappush(attackpriority, tmp)
    attacked.append([tmpx, tmpy])
    # 공격
    # tmped = heapq.heappop(attackedpriority)
    tmpedx = n-1
    tmpedy = m-1
    maxattack = 0
    for j in range(n):
        for k in range(m):
            if mymap[j][k] > 0:
                if mymap[j][k] > maxattack:
                    maxattack = mymap[j][k]
                    tmpedx = j
                    tmpedy = k
                elif maxattack == mymap[j][k]:
                    if recent[(j, k)] < recent[(tmpx, tmpy)]:
                        maxattack = mymap[j][k]
                        tmpedx = j
                        tmpedy = k
                    elif recent[(j, k)] == recent[(tmpx, tmpy)]:
                        if j + k < tmpedx + tmpedy:
                            maxattack = mymap[j][k]
                            tmpedx = j
                            tmpedy = k
                        elif j + k == tmpedx + tmpedy:
                            if k < tmpedy:
                                maxattack = mymap[j][k]
                                tmpedx = j
                                tmpedy = k
    attacked.append([tmpedx, tmpedy])
    # 레이저 공격
    mindist = n*m+1
    check = [[False for _ in range(m)] for _ in range(n)]
    minroute = []
    att = mymap[tmpx][tmpy]//2
    dfs(tmpx, tmpy, tmpedx, tmpedy, 0, att, [])
    # 공격
    mymap[tmpedx][tmpedy] = max(mymap[tmpedx][tmpedy] - mymap[tmpx][tmpy], 0)
    # 레이저
    if minroute:
        for j in range(1, len(minroute)):
            mymap[minroute[j][0]][minroute[j][1]] = max(mymap[minroute[j][0]][minroute[j][1]]-att, 0)
            attacked.append(minroute[j])
    # 포탄
    else:
        mymap[(tmpedx-1+n)%n][(tmpedy-1+m)%m] = max(mymap[(tmpedx-1+n)%n][(tmpedy-1+m)%m]-att, 0)
        mymap[(tmpedx-1+n)%n][tmpedy] = max(mymap[(tmpedx-1+n)%n][tmpedy]-att, 0)
        mymap[(tmpedx-1+n)%n][(tmpedy+1)%m] = max(mymap[(tmpedx-1+n)%n][(tmpedy+1)%m]-att, 0)
        mymap[tmpedx][(tmpedy+1)%m] = max(mymap[tmpedx][(tmpedy+1)%m]-att, 0)
        mymap[(tmpedx+1)%n][(tmpedy+1)%m] = max(mymap[(tmpedx+1)%n][(tmpedy+1)%m]-att, 0)
        mymap[(tmpedx+1)%n][tmpedy] = max(mymap[(tmpedx+1)%n][tmpedy]-att, 0)
        mymap[(tmpedx+1)%n][(tmpedy-1+m)%m] = max(mymap[(tmpedx+1)%n][(tmpedy-1+m)%m]-att, 0)
        mymap[tmpedx][(tmpedy-1+m)%m] = max(mymap[tmpedx][(tmpedy-1+m)%m]-att, 0)
        attacked.append([(tmpedx-1+n)%n, (tmpedy-1+m)%m])
        attacked.append([(tmpedx-1+n)%n, tmpedy])
        attacked.append([(tmpedx-1+n)%n, (tmpedy+1)%m])
        attacked.append([tmpedx, (tmpedy+1)%m])
        attacked.append([(tmpedx+1)%n, (tmpedy+1)%m])
        attacked.append([(tmpedx+1)%n, tmpedy])
        attacked.append([(tmpedx+1)%n, (tmpedy-1+m)%m])
        attacked.append([tmpedx, (tmpedy-1+m)%m])

    # for j in range(n):
    #     print(mymap[j])
    # print()
    for j in range(n):
        for k in range(m):
            if [j,k] not in attacked and mymap[j][k] > 0:
                mymap[j][k] += 1

    # for j in range(n):
    #     print(mymap[j])
    # print()

mymax = 0
for i in range(n):
    for j in range(m):
        if mymap[i][j] > mymax:
            mymax = mymap[i][j]
print(mymax)
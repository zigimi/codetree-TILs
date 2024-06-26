import copy
from collections import deque
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

def bfs(i, j, dx, dy):
    global minroute
    q = deque()
    q.append([[i, j]])
    check[i][j] = True
    while q:
        tmp = q.popleft()
        if mymap[tmp[-1][0]][tmp[-1][1]] == 0:
            continue

        if tmp[-1][0] == dx and tmp[-1][1] == dy:
            minroute = copy.deepcopy(tmp)
            break

        i = tmp[-1][0]
        j = tmp[-1][1]

        if check[i][(j+1)%m] == False:
            check[i][(j + 1) % m] = True
            tmptmp = copy.deepcopy(tmp)
            tmptmp.append([i, (j + 1) % m])
            q.append(tmptmp)
        if check[(i+1)%n][j] == False:
            check[(i + 1) % n][j] = True
            tmptmp = copy.deepcopy(tmp)
            tmptmp.append([(i+1)%n, j])
            q.append(tmptmp)
        if check[i][(j-1+m)%m] == False:
            check[(i + 1) % n][j] = True
            tmptmp = copy.deepcopy(tmp)
            tmptmp.append([i, (j-1+m)%m])
            q.append(tmptmp)
        if check[(i-1+n) % n][j] == False:
            check[(i - 1 + n) % n][j] = True
            tmptmp = copy.deepcopy(tmp)
            tmptmp.append([(i-1+n) % n, j])
            q.append(tmptmp)

for i in range(k):
    if len(recent) == 1:
        break
    attacked = []
    # 공격자 선정
    # tmp = heapq.heappop(attackpriority)
    tmpx = -1
    tmpy = -1
    minattack = 5001
    for j in range(n):
        for k in range(m):
            if mymap[j][k] > 0:
                if mymap[j][k] < minattack:
                    minattack = mymap[j][k]
                    tmpx = j
                    tmpy = k
                elif minattack == mymap[j][k]:
                    if tmpx == tmpy == -1 or recent[(j, k)] > recent[(tmpx, tmpy)]:
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

    # 공격
    # tmped = heapq.heappop(attackedpriority)
    tmpedx = -1
    tmpedy = -1
    maxattack = 0
    for j, k in recent.keys():
        if mymap[j][k] > 0 and not (j == tmpx and k == tmpy):
            if mymap[j][k] > maxattack:
                maxattack = mymap[j][k]
                tmpedx = j
                tmpedy = k
            elif maxattack == mymap[j][k]:
                if tmpedx == tmpedy == -1 or recent[(j, k)] < recent[(tmpedx, tmpedy)]:
                    maxattack = mymap[j][k]
                    tmpedx = j
                    tmpedy = k
                elif recent[(j, k)] == recent[(tmpedx, tmpedy)]:
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
    # dfs(tmpx, tmpy, tmpedx, tmpedy, 0, att, [])
    bfs(tmpx, tmpy, tmpedx, tmpedy)
    # 공격
    mymap[tmpedx][tmpedy] = max(mymap[tmpedx][tmpedy] - mymap[tmpx][tmpy], 0)
    # 레이저
    if minroute:
        for j in range(1, len(minroute)-1):
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
        if [tmpx, tmpy] in attacked:
            mymap[tmpx][tmpy] += att
            
    attacked.append([tmpx, tmpy])
    # print(minroute)
    # for j in range(n):
    #     print(mymap[j])
    # print()

    keys = list(recent.keys())
    for j, k in keys:
            if mymap[j][k] == 0:
                del recent[(j,k)]
                continue
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
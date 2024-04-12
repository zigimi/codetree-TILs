import copy
n, m, k = map(int, input().split())
mymap = []
runner = []

answer = 0
for i in range(n):
    mymap.append(list(map(int, input().split())))

for i in range(m):
    runner.append(list(map(int, input().split())))
    runner[-1][0] -= 1
    runner[-1][1] -= 1

out = list(map(int, input().split()))
out[0] -= 1
out[1] -= 1

for i in range(k):
    mindis = 2*n+1
    minx = n
    miny = n
    goal = []
    for j in range(len(runner)):
        # if j in goal:
        #     continue
        # print(runner[j])
        # dis = abs(runner[j][0]-out[0])+abs(runner[j][1]-out[1])
        if runner[j][0]-out[0] < 0 and mymap[runner[j][0]+1][runner[j][1]] == 0:
            runner[j][0] += 1
            answer += 1
            # print(1)
        elif runner[j][0]-out[0] > 0 and mymap[runner[j][0]-1][runner[j][1]] == 0:
            runner[j][0] -= 1
            answer += 1
            # print(2)
        else:
            if runner[j][1]-out[1] < 0 and mymap[runner[j][0]][runner[j][1]+1] == 0:
                runner[j][1] += 1
                answer += 1
                # print(3)
            elif runner[j][1]-out[1] > 0 and mymap[runner[j][0]][runner[j][1]-1] == 0:
                runner[j][1] -= 1
                answer += 1
                # print(4)
        # print("->", runner[j])
        if runner[j][0] == out[0] and runner[j][1] == out[1]:
            goal.append(runner[j])
            continue

        # print(answer)
        tmpdis = max(abs(runner[j][0]-out[0]), abs(runner[j][1]-out[1]))
        if tmpdis < mindis:
            mindis = tmpdis
            if runner[j][0] <= out[0]:
                fx = max(out[0] - tmpdis, 0)
                lx = out[0] + (tmpdis - (out[0] - fx))
            else:
                lx = min(out[0] + tmpdis, n - 1)
                fx = out[0] - (tmpdis - (lx - out[0]))

            if runner[j][1] <= out[1]:
                fy = max(out[1] - tmpdis, 0)
                ly = out[1] + (tmpdis - (out[1] - fy))
            else:
                ly = min(out[1] + tmpdis, n - 1)
                fy = out[1] - (tmpdis - (ly - out[1]))

        elif tmpdis == mindis:
            if runner[j][0] <= out[0]:
                tmpfx = max(out[0] - tmpdis, 0)
                tmplx = out[0] + (tmpdis - (out[0] - fx))
            else:
                tmplx = min(out[0] + tmpdis, n - 1)
                tmpfx = out[0] - (tmpdis - (lx - out[0]))

            if runner[j][1] <= out[1]:
                tmpfy = max(out[1] - tmpdis, 0)
                tmply = out[1] + (tmpdis - (out[1] - fy))
            else:
                tmply = min(out[1] + tmpdis, n - 1)
                tmpfy = out[1] - (tmpdis - (ly - out[1]))

            if fx > tmpfx:
                fx = tmpfx
                lx = tmplx
                fy = tmpfy
                ly = tmply

            elif fx == tmpfx:
                if fy > tmpfy:
                    fy = tmpfy
                    ly = tmply

    for j in goal:
        runner.remove(j)

    if not runner:
        break

    # 미로회전
    minsize = mindis #max(abs(minx-out[0]), abs(miny-out[1]))
    # if minx <= out[0]:
    #     fx = max(out[0] - minsize, 0)
    #     lx = out[0] + (minsize - (out[0] - fx))
    # else:
    #     lx = min(out[0] + minsize, n - 1)
    #     fx = out[0] - (minsize - (lx - out[0]))
    #
    # if miny <= out[1]:
    #     fy = max(out[1] - minsize, 0)
    #     ly = out[1] + (minsize - (out[1] - fy))
    # else:
    #     ly = min(out[1] + minsize, n - 1)
    #     fy = out[1] - (minsize - (ly - out[1]))


    rot = []
    for j in range(fx, lx+1):
        rot.append(mymap[j][fy:ly+1][:])

    newrunner = []
    moveout = False
    for j in range(fx, lx+1):
        for k in range(fy, ly+1):
            mymap[fx+(k-fy)][ly-(j-fx)] = rot[j-fx][k-fy]
            if mymap[fx+(k-fy)][ly-(j-fx)] > 0:
                mymap[fx+(k-fy)][ly-(j-fx)] -= 1
            if j == out[0] and k == out[1] and not moveout:
                out[0] = fx+(k-fy)
                out[1] = ly-(j-fx)
                moveout = True
            if [j, k] in runner:
                cnt = runner.count([j, k])
                for _ in range(cnt):
                    newrunner.append([fx+(k-fy), ly-(j-fx)])
                    runner.remove([j, k])
    runner.extend(newrunner)
    # print(runner)
    # print(out)
    # print()

print(answer)
print(str(out[0]+1) +  " " + str(out[1]+1))
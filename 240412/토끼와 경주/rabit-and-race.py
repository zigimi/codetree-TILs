qs = int(input())
pids = []
rabbits = {}
jumps = {}
score = {}
dist = {}
for _ in range(qs):
    q = list(map(int, input().split()))
    if q[0] == 100:
        n = q[1]
        m = q[2]
        p = q[3]
        pids = q[4:4+2*p:2][:]
        pids.sort()
        for i in range(0, p):
            rabbits[pids[i]] = [0, 0]
            jumps[pids[i]] = 0
            score[pids[i]] = 0
            dist[pids[i]] = q[5+2*i]

    elif q[0] == 200:
        for i in range(q[1]):
            # 우선순위
            sortjumps = sorted(jumps.items(), key=lambda x:x[1])
            minnum = sortjumps[0][0]
            minx = rabbits[sortjumps[0][0]][0]
            miny = rabbits[sortjumps[0][0]][1]
            minsum = minx + miny
            if len(sortjumps) > 1 and sortjumps[0][1] == sortjumps[1][1]:
                for j in range(1, p):
                    if sortjumps[0][1] == sortjumps[j][1]:
                        tmpx = rabbits[sortjumps[j][0]][0]
                        tmpy = rabbits[sortjumps[j][0]][1]
                        tmpsum = tmpx + tmpy
                        if tmpsum < minsum:
                            minnum = sortjumps[j][0]
                            minx = tmpx
                            miny = tmpy
                            minsum = tmpsum

                        elif tmpsum == minsum:
                            if tmpx < minx:
                                minnum = sortjumps[j][0]
                                minx = tmpx
                                miny = tmpy
                                minsum = tmpsum

                            elif tmpx == minx:
                                if tmpy < miny:
                                    minnum = sortjumps[j][0]
                                    minx = tmpx
                                    miny = tmpy
                                    minsum = tmpsum

                                elif tmpy == miny:
                                    if sortjumps[j][0] < minnum:
                                        minnum = sortjumps[j][0]
                                        minx = tmpx
                                        miny = tmpy
                                        minsum = tmpsum
                    else:
                        break
            jumps[minnum] += 1
            dirs = [[-1, 0],[1, 0], [0, -1], [0, 1]]
            move = [rabbits[minnum][:] for _ in range(4)]
            # 이동
            d = dist[minnum]
            cnt = 0
            while cnt < d:
                for j in range(4):
                    if -1 < move[j][0] + dirs[j][0] < n and -1 < move[j][1] + dirs[j][1] < m:
                        move[j][0] += dirs[j][0]
                        move[j][1] += dirs[j][1]
                    else:
                        dirs[j][0] *= -1
                        dirs[j][1] *= -1
                        move[j][0] += dirs[j][0]
                        move[j][1] += dirs[j][1]
                cnt+=1
            # 우선순위 구하기
            mindir = 0
            mindirsum = sum(move[mindir])
            for j in range(1, 4):
                tmpdirsum = sum(move[j])
                if tmpdirsum > mindirsum:
                    mindir = j
                    mindirsum = tmpdirsum
                elif tmpdirsum == mindirsum:
                    if move[mindir][0] < move[j][0]:
                        mindir = j
                        mindirsum = tmpdirsum
                    elif move[mindir][0] == move[j][0]:
                        if move[mindir][1] < move[j][1]:
                            mindir = j
                            mindirsum = tmpdirsum
            rabbits[minnum] = move[mindir]
            for k in pids:
                if k != minnum:
                    score[k] += mindirsum+2

        maxsum = 0
        maxnum = -1
        maxx = -1
        maxy = -1
        for idx in pids:
            if jumps[idx] == 0:
                continue
            tmpsum = sum(rabbits[idx])
            if tmpsum > maxsum:
                maxsum = tmpsum
                maxnum = idx
                maxx = rabbits[idx][0]
                maxy = rabbits[idx][1]
            elif tmpsum == maxsum:
                if rabbits[idx][0] > maxx:
                    maxsum = tmpsum
                    maxnum = idx
                    maxx = rabbits[idx][0]
                    maxy = rabbits[idx][1]
                elif rabbits[idx][0] == maxx:
                    if rabbits[idx][1] > maxy:
                        maxsum = tmpsum
                        maxnum = idx
                        maxx = rabbits[idx][0]
                        maxy = rabbits[idx][1]
                    elif rabbits[idx][1] == maxy:
                        if idx > maxnum:
                            maxsum = tmpsum
                            maxnum = idx
                            maxx = rabbits[idx][0]
                            maxy = rabbits[idx][1]
        score[maxnum] += q[2]

    elif q[0] == 300:
        dist[q[1]] *= q[2]
    else:
        print(max(score.values()))
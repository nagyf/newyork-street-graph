import sys
import os
import snap
import threading
import time
from subprocess import call

def main():
    if len(sys.argv) != 2:
        print('File name must be provided')
        sys.exit(-1)

    filename = sys.argv[1]
    filenameWOExt = filename.split('.')[0].split('/')[-1]
    graph = snap.LoadEdgeList(snap.PNEANet, filename, 0, 1, '\t')
    snap.PrintInfo(graph, "New York", filenameWOExt + '_info.txt', False)

    Rnd = snap.TRnd(123124)
    erdosRenyi = snap.GenRndGnm(snap.PNEANet, graph.GetNodes(), graph.GetEdges(), True, Rnd)
    snap.PrintInfo(erdosRenyi, "Erdos-Renyi", 'erdos_renyi_info.txt', False)

    printGenericInformation(graph, 'New York street network')
    printGenericInformation(erdosRenyi, 'Erdos-Renyi random graph')

    # Plot everything in the plots directory
    os.chdir(os.path.join(os.path.abspath(sys.path[0]), 'plots'))
    saveDegreeDistribution(graph, 'deg_dist_ny.tab')
    saveDegreeDistribution(erdosRenyi, 'deg_dist_er.tab')

    tNy = threading.Thread(target=testRobustness, args=(graph, 'robustness_ny_rand.tab', 100, True))
    tEr = threading.Thread(target=testRobustness, args=(erdosRenyi, 'robustness_er_rand.tab', 100, True))
    tNy.start()
    tEr.start()

    while True:
        tNy.join(600)
        tEr.join(600)
        if not tNy.isAlive() and not tEr.isAlive():
            break

    tNy = threading.Thread(target=testRobustness, args=(graph, 'robustness_ny_max.tab', 10, False))
    tEr = threading.Thread(target=testRobustness, args=(erdosRenyi, 'robustness_er_max.tab', 10, False))
    tNy.start()
    tEr.start()

    while True:
        tNy.join(600)
        tEr.join(600)
        if not tNy.isAlive() and not tEr.isAlive():
            break

    call(['gnuplot', 'deg_dist.plt'])
    call(['gnuplot', 'robustness_rand.plt'])
    call(['gnuplot', 'robustness_max.plt'])

def saveDegreeDistribution(graph, filename):
    degToCntV = snap.TIntPrV()
    snap.GetDegCnt(graph, degToCntV)
    with open(filename, 'w') as f:
        for item in degToCntV:
            dist = float(item.GetVal2()) / float(graph.GetNodes())
            f.write('%d\t%f\n' % (item.GetVal1(), dist))

def printGenericInformation(graph, name):
    print("Generic informations of %s" % name)
    print('Nodes', graph.GetNodes())
    print('Edges', graph.GetEdges())
    print('Average degree (In+Out)', float(graph.GetEdges()) / float(graph.GetNodes()))
    print('Diameter', snap.GetBfsFullDiam(graph, 10))
    print('Clustering coefficient', snap.GetClustCf(graph))
    print('Triangles', snap.GetTriangleCnt(graph))
    print('---------------------------------------')

def testRobustness(graph, filename, times = 100, random = True):
    results = []
    with open(filename, 'w') as f:
        for i in range(times):
            print('%s test no.: %d' % (filename, i))
            if random:
                results = runRobustnessTestRandomly(graph)
            else:
                results = runRobustnessTestMax(graph)
            f.write('\n\n')
            for data in results:
                f.write('%f\t%f\n' % (data[0], data[1]))

def runRobustnessTestRandomly(graph, rounds = 30):
    graph = cloneGraph(graph)
    result = []
    rnd = snap.TRnd()
    rnd.Randomize()
    originalEdgesCnt = graph.GetEdges()
    for i in range(rounds):
        fractionRemoved = 1.0 - float(graph.GetEdges()) / float(originalEdgesCnt)
        result.append((fractionRemoved, snap.GetMxSccSz(graph)))
        for n in range(originalEdgesCnt / rounds):
            graph.DelEdge(graph.GetRndEId(rnd))
    return result

def runRobustnessTestMax(graph, rounds = 30):
    graph = cloneGraph(graph)
    result = []
    originalNodesCnt = graph.GetNodes()
    for i in range(rounds):
        fractionRemoved = 1.0 - float(graph.GetNodes()) / float(originalNodesCnt)
        result.append((fractionRemoved, snap.GetMxSccSz(graph)))
        for n in range(originalNodesCnt / rounds):
            graph.DelNode(snap.GetMxDegNId(graph))
    return result

def cloneGraph(graph):
    cloned = snap.ConvertGraph(type(graph), graph)
    return cloned

def getTimeMs():
    return int(round(time.time() * 1000))

if __name__ == '__main__':
    main()
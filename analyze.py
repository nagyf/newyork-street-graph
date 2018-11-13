import sys
import os
import snap
from subprocess import call

def main():
    if len(sys.argv) != 2:
        print('File name must be provided')
        sys.exit(-1)

    filename = sys.argv[1]
    filenameWOExt = filename.split('.')[0].split('/')[-1]

    graph = snap.LoadEdgeList(snap.PNGraph, filename, 0, 1, '\t')

    snap.PrintInfo(graph, "New York", filenameWOExt + '_info.txt', False)
    print('Nodes', graph.GetNodes())
    print('Edges', graph.GetEdges())
    print('Average degree (In+Out)', float(graph.GetEdges()) / float(graph.GetNodes()))
    print('Diameter', snap.GetBfsFullDiam(graph, 10))
    print('Clustering coefficient', snap.GetClustCf(graph))
    print('Triangles', snap.GetTriangleCnt(graph))

    # Plot everything in the plots directory
    os.chdir(os.path.join(os.path.abspath(sys.path[0]), 'plots'))
    saveDegreeDistribution(graph, 'deg_dist_ny.tab')
    
    Rnd = snap.TRnd()
    erdosRenyi = snap.GenRndGnm(snap.PNGraph, graph.GetNodes(), graph.GetEdges(), True, Rnd)
    saveDegreeDistribution(erdosRenyi, 'deg_dist_er.tab')

    call(['gnuplot', 'deg_dist.plt'])

def saveDegreeDistribution(graph, filename):
    degToCntV = snap.TIntPrV()
    snap.GetDegCnt(graph, degToCntV)
    with open(filename, 'w') as f:
        for item in degToCntV:
            dist = float(item.GetVal2()) / float(graph.GetNodes())
            f.write('%d\t%f\n' % (item.GetVal1(), dist))

if __name__ == '__main__':
    main()
import sys
import snap

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
    degToCntV = snap.TIntPrV()
    snap.GetDegCnt(graph, degToCntV)

    degreeDistribution = {}
    for item in degToCntV:
        degreeDistribution[item.GetVal1()] = float(item.GetVal2()) / float(graph.GetNodes())
        print "%d nodes with degree %d with distribution %f" % (item.GetVal2(), item.GetVal1(), degreeDistribution[item.GetVal1()])

    snap.PlotInDegDistr(graph, filenameWOExt, "New York City streets In Degree")
    snap.PlotOutDegDistr(graph, filenameWOExt, "New York City streets Out Degree")
    snap.PlotClustCf(graph, filenameWOExt, "New York City streets Clustering coefficient")
    snap.PlotSccDistr(graph, filenameWOExt, "Strongly Connected Components distribution")
    snap.PlotWccDistr(graph, filenameWOExt, "Weakly Connected Components distribution")
    # snap.DrawGViz(graph, snap.gvlDot, filenameWOExt + ".png", "New York")

if __name__ == '__main__':
    main()
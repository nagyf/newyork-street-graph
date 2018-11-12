import sys
import math
import simplekml
import xml.etree.ElementTree as ET

def main():
    if len(sys.argv) != 2:
        print('File name must be provided')
        sys.exit(-1)
    filename = sys.argv[1]
    filenameWOExt = filename.split('.')[0]
    tree = ET.parse(filename)
    root = tree.getroot()

    # Find out which property stores the line geometry
    geometryId = root.find("{http://graphml.graphdrawing.org/xmlns}key[@attr.name='geometry']").attrib['id']

    newId = 0
    nodeMap = {}
    kml = simplekml.Kml()
    for node in root.iter('{http://graphml.graphdrawing.org/xmlns}node'):
        lat = float(node.find("{http://graphml.graphdrawing.org/xmlns}data[@key='d3']").text)
        lon = float(node.find("{http://graphml.graphdrawing.org/xmlns}data[@key='d4']").text)
        nodeMap[node.attrib['id']] = (newId, lat, lon)
        kml.newpoint(name="Point %s" % newId, coords=[(lat, lon)])
        newId += 1
    kml.save(filenameWOExt + '.kml')

    kml = simplekml.Kml()
    with open(filenameWOExt + '.txt', 'w') as output:
        for edge in root.iter('{http://graphml.graphdrawing.org/xmlns}edge'):
            source = nodeMap[edge.attrib['source']] 
            target = nodeMap[edge.attrib['target']]
            geometry = edge.find("{http://graphml.graphdrawing.org/xmlns}data[@key='" + geometryId + "']")
            if(geometry is not None):
                ls = kml.newlinestring()
                ls.coords.addcoordinates(linestringToCoordinates(geometry.text))
            else:
                ls = kml.newlinestring()
                ls.coords.addcoordinates([(source[1], source[2]), (target[1], target[2])])

            output.write(str(source[0]) + '\t' + str(target[0]) + '\t' + str(source[1]) + '\t' + str(source[2]) + '\t' + str(target[1]) + '\t' + str(target[2]) + '\n')

    kml.save(filenameWOExt + '_roads.kml')

def linestringToCoordinates(linestring):
    coordinates = linestring.split('LINESTRING (')[1].split(')')[0].split(',')
    return [(c.strip().split(' ')[1], c.strip().split(' ')[0]) for c in coordinates]

if __name__ == '__main__':
    main()
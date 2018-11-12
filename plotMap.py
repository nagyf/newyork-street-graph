import sys
import mapnik

def main():
    if len(sys.argv) != 3:
        print('File names must be provided')
        sys.exit(-1)
    filenameIntersections = sys.argv[1]
    filenameRoads = sys.argv[2]
    render(filenameIntersections, filenameRoads)

def render(filenameIntersections, filenameRoads):
    filenameWOExt = filenameIntersections.split('.')[0]
    # Setup the map
    map_canvas = mapnik.Map(14030, 9922)
    map_canvas.background = mapnik.Color('white')

    map_canvas.append_style('intersections', createIntersectionStyle())
    map_canvas.layers.append(createIntersectionLayer(filenameIntersections, 'intersections'))

    map_canvas.append_style('roads', createRoadStyle())
    map_canvas.layers.append(createRoadLayer(filenameRoads, 'roads'))

    # Save the map
    map_canvas.zoom_all()
    mapnik.render_to_file(map_canvas, filenameWOExt + '.png', 'png')

def createIntersectionStyle():
    style = mapnik.Style()
    rule = mapnik.Rule()
    point_symbolizer = mapnik.MarkersSymbolizer()
    point_symbolizer.allow_overlap = True
    point_symbolizer.opacity = 0.5
    rule.symbols.append(point_symbolizer)
    style.rules.append(rule)
    return style

def createIntersectionLayer(filename, stylename):
    layer = mapnik.Layer(stylename)
    layer.datasource = mapnik.Ogr(file=filename, layer_by_index=0)
    layer.styles.append(stylename)
    return layer

def createRoadStyle():
    style = mapnik.Style()
    rule = mapnik.Rule()
    line_symbolizer = mapnik.LineSymbolizer()
    line_symbolizer.allow_overlap = True
    line_symbolizer.opacity = 0.5
    rule.symbols.append(line_symbolizer)
    style.rules.append(rule)
    return style

def createRoadLayer(filename, stylename):
    layer = mapnik.Layer(stylename)
    layer.datasource = mapnik.Ogr(file=filename, layer_by_index=0)
    layer.styles.append(stylename)
    return layer

if __name__ == '__main__':
    main()
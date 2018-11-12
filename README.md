# Introduction
This collection of python scripts can be used to analyze the New York City Street graph.

## Install

```
1. Activate virtualenv
> . venv/bin/activate

2. Install dependencies
> pip install -r requirements.txt
```

## Usage

To transform the input data, run:
```
> python2.7 xmltograph.py input/manhatten.graphml
> python2.7 xmltograph.py input/newyork.graphml
```

To plot the road network on a map, run:
```
> python2.7 plotMap.py input/manhatten.kml input/manhatten_roads.kml
> python2.7 plotMap.py input/newyork.kml input/newyork.kml
```

set title "New York City streets degree distribution."
set key bottom right
set logscale y 10
set mxtics 1
set format y "10^{%L}"
set mytics 10
set grid
set xlabel "Node degree"
set ylabel "In-Out Degree distribution"
set tics scale 1
set terminal png font arial 10 size 1000,800
set output 'deg_dist.png
plot 	"deg_dist_ny.tab" using 1:2 title "" with linespoints pt 13 lw 2 lt rgb "salmon", \
        "deg_dist_er.tab" using 1:2 title "" with linespoints pt 13 lw 2 lt rgb "dark-gray", \
        "deg_dist_gr.tab" using 1:2 title "" with linespoints pt 13 lw 2 lt rgb "black"
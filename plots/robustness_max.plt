set title "New York City streets robustness (max)"
set nokey
set mxtics 1
set mytics 1
set grid
set xlabel "Fractions of removed edges"
set ylabel "Relative size S"
set tics scale 1
set terminal png font arial 10 size 1000,800
set output 'robustness_max.png'
datafile0 = 'robustness_0_max.tab'
datafile1 = 'robustness_1_max.tab'
datafile2 = 'robustness_2_max.tab'
stats datafile0 nooutput
plot for [IDX=0:STATS_blocks-1] \
    datafile0 \
    index IDX \
    using 1:2 \
    with lines \
    lt rgb "salmon", \
    for [IDX=0:STATS_blocks-1] \
    datafile1 \
    index IDX \
    using 1:2 \
    with lines \
    lt rgb "dark-gray", \
    for [IDX=0:STATS_blocks-1] \
    datafile2 \
    index IDX \
    using 1:2 \
    with lines \
    lt rgb "green"
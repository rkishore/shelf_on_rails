set size 1, 1.5
set terminal postscript eps enhanced  color dashed  "Times-Roman" 14
#set style data linespoints
set pointsize 0.5


set nokey

set yrange [0:200] 
set xrange [0:100]
set multiplot

#set xtics 0,20,80
#set ytics 0,0.5,3.5
#set noxlabel
set ylabel "Price ($)"
set format x "%g"
set format y "%g"	

set origin 0, 1
set size 1, .5
#set label 11 "Express" at graph 0.2,0.7 center font "Times-Roman,18"
set key right top
set yrange [0:1000]
set xlabel "Itemlist ID: MAXIMUM PRICED ITEMS"
plot	"../data/overall_itemlist_br_max_with_disc.txt" using 1:3 title "Banana Republic" pt 1, \
	"../data/overall_itemlist_j.crew_max_with_disc.txt" using 1:3 title "J.Crew" pt 2, \
	"../data/overall_itemlist_express_max_with_disc.txt" using 1:3 title "Express" pt 3





#set noylabel 
set format y "%g"

set origin 0, 0.5
set size 1, 0.5
#set label 11 "J.Crew" at graph 0.2,0.7 center font "Times-Roman,18"
set xlabel "Item ID: MEDIAN PRICED ITEMS"
set ylabel "Price ($)"
plot	"../data/overall_itemlist_br_median_with_disc.txt" using 1:3 title "Banana Republic" pt 1, \
	"../data/overall_itemlist_j.crew_median_with_disc.txt" using 1:3 title "J.Crew" pt 2, \
	"../data/overall_itemlist_express_median_with_disc.txt" using 1:3 title "Express" pt 3




#set noylabel 
set format y "%g"

set origin 0, 0
set size 1, 0.5
#set label 11 "Banana Republic" at graph 0.2,0.7 center font "Times-Roman,18"
set xlabel "Item ID: MINIMUM PRICED ITEMS"
set ylabel "Price ($)"
plot	"../data/overall_itemlist_br_min_with_disc.txt" using 1:4 title "Banana Republic" pt 1, \
	"../data/overall_itemlist_j.crew_min_with_disc.txt" using 1:4 title "J.Crew" pt 2, \
	"../data/overall_itemlist_express_min_with_disc.txt" using 1:4 title "Express" pt 3


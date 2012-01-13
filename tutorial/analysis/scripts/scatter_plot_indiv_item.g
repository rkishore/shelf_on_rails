set size 1, 1.5
set terminal postscript eps enhanced  color dashed  "Times-Roman" 14
#set style data linespoints
set pointsize 0.25


set nokey

set yrange [0:200] 
set xrange [0:500]
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
set xlabel "Item ID: Express"
plot	"../data/overall_item_with_disc_express.txt" using 1:2 title "Base Price" pt 1, \
	"../data/overall_item_with_disc_express.txt" using 1:3 title "Sale Price" pt 2, \
	"../data/overall_item_with_disc_express.txt" using 1:4 title "Discount in %" pt 3

#"../data/overall_item_with_disc_express.txt" using 1:2 title "Base Price" with linesp lt 1 pt 1, \
#	"../data/overall_item_with_disc_express.txt" using 1:3 title "Sale Price" with linesp lt 2 pt 2, \
#	"../data/overall_item_with_disc_express.txt" using 1:4 title "Discount in %" with linesp lt 4 pt 4

#set nokey




#set noylabel 
set format y "%g"

set origin 0, 0.5
set size 1, 0.5
#set label 11 "J.Crew" at graph 0.2,0.7 center font "Times-Roman,18"
set xlabel "Item ID: J.Crew"
set ylabel "Price ($)"
plot	"../data/overall_item_with_disc_j.crew.txt" using 1:2 title "Base Price"  pt 1, \
	"../data/overall_item_with_disc_j.crew.txt" using 1:3 title "Sale Price"  pt 2, \
	"../data/overall_item_with_disc_j.crew.txt" using 1:4 title "Discount in %" pt 4
#set nokey


#set noylabel 
set format y "%g"

set origin 0, 0
set size 1, 0.5
#set label 11 "Banana Republic" at graph 0.2,0.7 center font "Times-Roman,18"
set xlabel "Item ID: BR"
set ylabel "Price ($)"
plot	"../data/overall_item_with_disc_br.txt" using 1:2 title "Base Price" pt 1, \
	"../data/overall_item_with_disc_br.txt" using 1:3 title "Sale Price" pt 2, \
	"../data/overall_item_with_disc_br.txt" using 1:4 title "Discount in %" pt 4
#set nokey

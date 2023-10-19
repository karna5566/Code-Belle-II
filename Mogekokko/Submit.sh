#!/bin/bash
#Sample = $1
#nfiles = $2
#Energy_L = $3
#Energy_H = $4
for i in {1000,4000,8000}; do
	id_args=""
	for j in $(seq $i $(($i+$2-1))); do
		id_args="$id_args $j"
	done
	List=$id_args
	arr=($List)
	#nohup python3 Fo.py -s $1 -id $id_args -e $3 $4 > ./Fit_result/fit_output/chi_$1_${arr[0]}_$3_$4.txt &
	nohup python3 Jo.py -s $1 -id $id_args -e $3 $4 -v clusterTiming
done


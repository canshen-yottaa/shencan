#!/bin/bash
#author: Jiang Liu <jiangliu@yottaa.com>
diskarray=(`cat /proc/diskstats |grep -E "\bsd[a-z]\b|\bxvd[a-z]\b|\bhd[a-z]"|grep -i "\b$1\b"|awk '{print $3}'|sort|uniq   2>/dev/null`)
length=${#diskarray[@]}
printf "{\n"
printf  '\t'"\"data\":["
for ((i=0;i<$length;i++))
do
    printf '\n\t\t{'
    printf "\"{#DISK_NAME}\":\"${diskarray[$i]}\"}"
if [ $i -lt $[$length-1] ];then
    printf ','
fi
done
printf  "\n\t]\n"
printf "}\n"
#!/bin/bash
#array=(aa bb cc)

#array=
array=($(cat tomcat-quanfangzhen.txt|awk '{print $1}'|uniq))
printf "{\n"
printf '\t"data1":[\n'
for ((i=0;i<${#array[@]};i++))
do
  printf '\t\t\n'
  num=$(echo $((${#array[@]}-1)))
  if [ "$i" == ${num} ];
  then
    printf "\t\t\"${array[$i]}\"\n"
  else
    printf "\t\t\"${array[$i]}\",\n"
    #printf "\t\t\t\"{#DISK_NAME}\":\"${array[$i]}\"},\n"
  fi
done
printf "\t]\n"
printf "}\n"

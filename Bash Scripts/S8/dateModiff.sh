#!/bin/bash
args="$1"
dateModiff(){
    name=${args:1}
    name=${name::-1}
    fileName2="ModifDateOf${name}_journal"
    echo "File/Dir Name $name" >> "$fileName2"
    stat $1 | sed -n '6p' |  cut -d ":" -f2- | cut -d "+" -f1 >> "$fileName2"  
}

dateModiff "$1"

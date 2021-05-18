#!/bin/bash

dateAcces(){
    name=${1:1}
    name=${name::-1}
    fileName="AccesDateOf${name}_journal"
    echo "File/Dir Name $name" >> "$fileName" 
    stat /etc | sed -n '5p' |  cut -d ":" -f2- | cut -d "+" -f1 >>  "$fileName"
}

dateAcces "$1"

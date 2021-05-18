#!/bin/bash 

#===============================================================================
#
#          FILE: monitorEtc.sh
# 
#         USAGE: ./monitorEtc.sh 
# 
#   DESCRIPTION: Count :directory, dirr content; and plot them.
# 
#       OPTIONS:  -T : trace/map file and parent dirr
#                 -t : trace/map directory 
#                 -n : count files  
#                 -N : Show dirr owner
#                 -d : write last acces date of file/directory in a file
#                 -m : write last modif date of file/directory in a file
#                 -s : 'Dashboard' GNU box plot of number of files and number 
#                      of dirrs
#  REQUIREMENTS: /path/of/dirr/
#          BUGS: ---
#         NOTES: ---
#        AUTHOR:  
#  ORGANIZATION: 
#       CREATED: 05/17/2021 02:23
#      REVISION:  ---
#===============================================================================

source dateAcces.sh

help(){
    less help.txt
}

termMenu(){
        echo "Choisir une tache :"
                        echo "1)   -h: Pour afficher le help détaillé à partir d’un fichier texte"
                        echo "2)   -g : graphical menu with YAD"   
                        echo "3)   -v : software version and @uthors"
                        echo "4)          -T : trace/map file and parent dirr"
                        echo "5)          -t : trace/map directory "
                        echo "6)          -n : count files  "
                        echo "7)          -N : Show dirr owner"
                        echo "8)          -d : write last acces date of file/directory in a file"
                        echo "9)          -m : write last modif date of file/directory in a file"
                        echo "10)         -s : 'Dashboard' GNU box plot of number of files and number "
                        echo "0)   Quitter"
                        read choix
}



interMode(){
    DIALOG=${DIALOG=dialog}
    tmpFile=`tmpFile 2> /dev/null` || tmpFile=/tmp/test$$
    trap "rm -f $tmpFile" 0 1 2 5 15
    
    $DIALOG --backtitle "Monitor" \
            --title "Menu" --clear \
            --radiolist "Choose here" 100 61 8 \
            1 " display help " off \
            2 "Authors And version" off \
            3 "Affiche File Function Of Arg" off \
            4 "Affiche  Dir Function Of Arg" off \
            5 "Count dirs and files to file " off \
            6 "Show Dir Ownership" off \
            7 "Show last Acees Date of Arg" off \
            8 "Show last Modif Date of Arg" off \
            9 "show Dashboard " off  2> $tmpFile
    
    
    valret=$?
    choice=`cat $tmpFile`

                case $valret in 
                1)
                    help
                    ;;
                2)
                    authors
                    ;;
                3)
                    afficheFile "$1"
                    ;;
                4)
                    afficheDir "$1"
                    ;;
                5)
                    NB
                    ;;
                6)
                    dirrUser
                    ;;
                7)
                    dateAcces1
                    ;;
                8)
                    dateModif2
                    ;;
                9)
                    stat
                    ;;


                esac
                        case $choice in

                1)
                    help
                    ;;
                2)
                    authors
                    ;;
                3)
                    afficheFile "$1"
                    ;;
                4)
                    afficheDir "$1"
                    ;;
                5)
                    NB
                    ;;
                6)
                    dirrUser
                    ;;
                7)
                    dateAcces1
                    ;;
                8)
                    dateModif2
                    ;;
                9)
                    stat
                    ;;
                esac        
}
authors(){
    echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    echo "                --- x --- "
    echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    echo "Versio 0.0.1"
}
afficheFile(){ 
    name=${1:1}
    name=${name::-1}
    fileName="FilesOf${name}_journal.txt"
    find $1 -maxdepth 1 -type f | tee "$fileName"
}

afficheDir(){
    name=${1:1}
    name=${name::-1} 
    fileName="DirrsOf${name}_journal.txt"
    find $1 -maxdepth 1 -type d | tee "$fileName"
}



NB(){
    dirCount=$(find $1 -maxdepth 1 -type d  | wc -l)
    filesCount=$(find $1 -maxdepth 1 -type f  | wc -l)
    echo "#type count" >> count
    echo "files $filesCount" >> count
    echo "dirrrs $dirCount" >> count
}

dirrUser(){
    a=$(ls -alF $1 | grep -Ei ' ./' | cut -d " " -f3) 
    echo "User of $1 is $a"
}

dateAcces1(){
    dateAcces "$1"
}


dateModif2(){
    /bin/bash ./dateModiff.sh "$1"
}

stat(){
    FILE=./count
    if test -f "$FILE"; then
        gnuplot -p -e ' 
        set xlabel "\FileXDir\n\n\n" font "Times-Roman,25";
        set ylabel "\Count\n" font "Times-Roman,25";
        set style data histograms;
        plot "./count" using 2:xtic(2) title "FilesxDirsCount"'    
    else
        echo "DataFile Not found , try with -N /path/to/dirr then do this again"
    fi
}



options=$(getopt -l "affichF:,affichD:,count:lasAcs:,lastM:,stat,authors,graph,help,termMenu" -o "T:t:n:N:d:m:svi:hM:" -a -- "$@")
eval set -- "$options"
while  ; do
    case $1 in
        -T|--affichF)
            afficheFile "$2"
            exit 0
            ;;
        -t|--affichD)
            afficheDir "$2"
            exit 0
            ;;
        -n|--count)
            NB "$2"
            exit 0
            ;;
        -N|--nlasAcs)
            dirrUser "$2"
            exit 0
            ;;
        
        -d|--lasAcs)
            dateAcces1 "$2"
            exit 0
            ;;
        -m|--lastM)
            dateModif2 "$2"
            exit 0
            ;;
        -s|--stat)
            stat
            exit 0
            ;;
        
        -h|--help)
            help
            exit 0
            ;;
        -i|--graph)
            interMode
            exit 0
            ;;
        -v|--authors)
            authors
            exit 0
            ;;
        
        * )
          echo "No Options specified"
          cat help.txt
          exit 0 
          ;;
  
    esac
done    

if ((options == 2))
then
    echo "directorys"
fi

   
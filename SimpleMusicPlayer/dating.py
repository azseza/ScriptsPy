import random
import simpleaudio as sa
import numpy as np
import time
import os
import turtle as tr

def read_txt_file(path_a_lire):
    '''
    lecture du fishier txt et retourne : 
    leurs noms dans une liste
    les partitions dans une liste
    raises a file not found error in case the file is empty
    '''
    numnamePartition = []
    partition = []
    file = open(path_a_lire, 'r')
    lines = file.readlines()
    for line in lines:
        song = ''
        if line[0] == '#':
            numnamePartition.append(line)
            song = ''
        else:
            partition.append(line)
    numnamePartition.insert(0,partition.pop(0))
    try:
        assert (len(numnamePartition) != 0 ) and (len(partition) != 0 )
    except AssertionError :
        raise FileNotFoundError
    return partition, numnamePartition


def append_text_file(path_fishier_bd, aDict):
    '''
    append the original partitions.txt file (path_fishier_bd) 
    with a dict countaing one or more partiions 
    '''
    with open(path_fishier_bd, 'w') as f : 
        x = aDict.keys()
        for i in x:
            f.write(x[i])
    print("Done !!")

def makeDict(numnomPartition, partition):
    '''
    returns a dict countaining song with song number & partition 
    '''
    #partition = partition[:-1]
    daDict = {numnomPartition[i]: partition[i] for i in range(len(numnomPartition))} 
    return daDict

def list_partitions(daDict, printEm = False):
    '''
    returns a list countaininf all the partitions in the file
    '''
    x = daDict.keys()
    if printEm :
        j = 1 
        for i in x : 
            print("~"+str(j)+"//"+"partition"+ str(i))
    return x 

def makeItMusic(aString):
    '''
    takes a string of notes , separated with spaces, returnes a tupple of tupples
    countaining the pair (note,duration)
    '''
    mapNotes = {"DO" : 264, "RE" : 297,"MI" : 330,"FA" : 352,"SOL" : 396, "LA" : 440, "SI" : 495, "Z" : -1}
    mapTimes = {"r" : 1000, "b" : 500, "c" : 125, "n" : 250}
    a = tuple(aString.rsplit())
    toPlay = tuple()
    timeee=list()
    notesss = list()
    index = 0
    for notes in a : 
        note = notes[:-1]
        tim = notes[-1]
        if tim == "p":
            flag = index-1
            timeee.append(timeee[flag])
        else:
            timeee.append(mapTimes[tim])
            notesss.append(mapNotes[note])
        index += 1 
    toPlay = zip(notesss,timeee)
    return toPlay
            
def playMeNote(note, time):
    '''
    takes two intigers
    note : int ; frequency en Hz de la note 
    time : int ; temps pour le quel il faut jouer la note
    '''
    sample_rate = 44100
    time /= 1000
    t = np.linspace(0, time, int(time * sample_rate), False)
    tone = np.sin(((t* note) *(6)) * np.pi)
    audio = np.hstack((tone,))
    audio *= 32767 / np.max(np.abs(audio))
    audio = audio.astype(np.int16)
    play_obj = sa.play_buffer(audio, 1, 2, sample_rate)
    play_obj.wait_done()

def playMyJam(daDict, index=0, play_all=True):
    '''
    plays all the tunes in the dict(comming from the *.txt file)
    or just playing a single note if index is given and play_all is false
    '''
    colors = ["red","blue","green"]
    tr.bgcolor("black")
    n = 0
    keyy = list(daDict.keys())
    ind = keyy[index-1]
    if play_all:
        for key in daDict.keys():
            print("playing this  "+str(key))
            x = list(makeItMusic(daDict[key]))
            for a in x:
                playMeNote(a[0],a[1])
                tr.up()
                colorrr = random.choice(colors)
                tr.color(colorrr)
                n = n%1000
                tr.pensize(n)
                tr.down()
                tr.forward(n)
                tr.left(60)
                n = (n+1)%360
    else:
        x = list(makeItMusic(daDict[ind]))
        for a in x:
            playMeNote(a[0],a[1])
            tr.up()
            tr.color(colors[n%3])
            tr.width(n/100+1)
            tr.down()
            tr.forward(n)
            tr.left(60)
            x = (n+1)%360
    try:
         turtle.bye()
    except : 
        print("tank you..")

def makeRandumMarkov(coefs, how_many):
    '''
    genere un chanson a partir de coefs de markov
    retourne un string contenat les nottes ainsi que leurs temps
    '''
    times = ["b", "r", "n", "c"]
    a =''
    for x in range(how_many):
        key=random.choice(list(coefs.keys()))
        keyy = list(coefs[key][1].keys())
        for note in keyy:
            a += str(note)+random.choice(times)+' ' 
    return a

def makeMarkovnotStatistic(coefs, how_many):
    '''
    genere une chanson a partir de coed de markov
    retourne un string contenant les notes ainsi que leurs temps
    '''
    a = ''
    times = ["b", "r", "n", "c"]
    #sort coefs
    max = 0
    for i in range(len(list(coefs.keys()))):    
        for key in coefs.keys():
            if coefs[key][0]>=max:
                maxk = key 
        for tic in coefs[maxk][1].keys():
            a += (tic+random.choice(times)+' ')*coefs[maxk][1][tic]+' '
        coefs.pop(maxk)
    return a

def markovV1(aDict, index, version):
    key = list(aDict.keys())
    dkey = key[index]
    to_study = aDict[dkey]
    daNotes = ["DO", "RE", "MI", "FA", "SOL", "LA","SI"]
    mapNote = {"DO" : 0, "RE" : 0,"MI" : 0,"FA" : 0,"SOL" : 0, "LA" : 0, "SI" : 0}
    coefs = {"DO" : [0,mapNote], "RE" :[0, mapNote],"MI" :[0, mapNote],"FA" :[0,mapNote],"SOL" : [0,mapNote]
            , "LA" : [0,mapNote], "SI" : [0,mapNote]}
    #mettre les notes dans un tuple
    notes = to_study.split(' ')
    #suppression des temps de notes de la chanson
    occ = 0 
    for i in range(len(notes)) : 
        if notes[i][-1] == '\n':
            notes[i] = notes[i][:-1]
        notes[i] = notes[i][:-1]
    #loop through the notes:
    for key, value in enumerate(notes):
        if value in daNotes:
            coefs1=calcOcc(notes[key:])
            coefs[value][1] = coefs1
            coefs[value][0] += 1
        else:
            pass
    #deleting null occurences
    for i, (oc, cof) in enumerate(coefs.items()):
        for i, (n, o) in enumerate(cof[1].copy().items()):
            if o == 0 :
                cof[1].pop(n)
    if version == 1 : 
        hm = random.randint(5,15)
        song = makeRandumMarkov(coefs, hm)
    elif version == 2 :
        hm = random.randint(5,15)
        song = makeMarkovnotStatistic(coefs, hm)
    songReturned ={ 0 : song}
    return songReturned

def calcOcc(note):
    mapNote = {"DO" : 0, "RE" : 0,"MI" : 0,"FA" : 0,"SOL" : 0, "LA" : 0, "SI" : 0}
    daNotes = ["DO", "RE", "MI", "FA", "SOL", "LA","SI"]
    for key, value in enumerate(note):
        if value in daNotes:
            mapNote[value]+=1
        else:
            pass
    return mapNote

def markovV2(aDict, version):
    '''
    appliquer markov a tout le fishier (dict)
    '''
    final = dict()
    keys = list(aDict.keys())
    for i in range(len(keys)):
        final.update(markovV1(aDict,i,version))
    return final
   

def choosemarkov(dadict):
    menu2=True
    while menu2:
        print("""
        1.Apply markov to a database
        2.Apply markov to partition
        """)
        menu2=input()
        if menu2=="1":
            markovdb(dadict)
        elif menu2=="2":
            markovpart(dadict)
        break
        
             

def markovpart(dadict):
    menu4=True
    list_of_partitions = list(list_partitions(dadict,printEm=False))
    while menu4:
        print(""""
        APPLIQUER MARKOV SUR UNE PARTITION
        Choisir une version:
        1.Version1: prendre en compte le nombre d'occurences
        2.Version2: sans prendre en compte le nombre d'occurences
        """)
        menu4=input()
        if menu4=="1":
            print('markov version1')
            print("choisir une partition")
            for i in range(len(list_of_partitions)):
                print(str(i+1)+" -"+list_of_partitions[i])
            index = int(input("Which one ? "))
            to_p = markovV1(dadict, index, 1)
            playMyJam(to_p, play_all = False)
        elif menu4=="2":
            print("markov version2")
            print("choisir une partition")
            for key, value in enumerate(list_of_partitions):
                print(str(key+1)+" -"+list_of_partitions[key])
            index = int(input("Which one ? "))
            to_p = markovV1(dadict, index, 2 )
            playMyJam(to_p, play_all = False)
        break

def markovdb(dadict):
    menu3=True
    while menu3:
        print("""
        APPLIQUER MARKOV SUR LA BD
        Choisir la version:
        1.Version1: Prendre en compte le nombre d'occurences
        2.Version2: Sans prendre en compte le nombre d'occurences
        """)
        menu3=input()
        if menu3=="1":
            print('markov version1')
            to_p = markovV2(dadict,1)
            playMyJam(to_p, play_all=False)
        elif menu3=="2":
            print("markov version2")
            to_p = markovV2(dadict, 2)
            playMyJam(to_p, play_all=True)
        break
                
def Transformation(dadict):
    menu1=True
    a = list(dadict.keys())
    while menu1:
        print(""""
        1.Inverse
        2.Transposition
        3.Markov""")
        menu1=input("Donnez votre choix")
        if menu1=="1":
            print("Inverser avec combien de pas")
            b = int(input())
            print("Appliquer l'inversion sur quelle chanson ")
            list_of_partitions = list_partitions(dadict, printEm=True)
            index = int(input("choix"))
            indexx = a[index]
            listt = conversion(dadict[indexx])
            string = deconvert(Inverse(b, listt))
            smtr = {0 : string}
            playMyJam(smtr, index=0, play_all=False)
        elif menu1=="2":
            print("Transposition")
            print("Appliquer la Transposition sur quelle intervalle")
            list_of_partitions = list_partitions(dadict, printEm=True)
            index = int(input("choix")) - 1 
            indexx = a[index]
            listt = conversion(dadict[indexx])
            k = int(input("Transposer de Combien ? "))
            b = int(input("Inverser Dans une intervalle de ? "))
            string = deconvert(Transpose(k,b,listt))
            smtr = {0: string}
            playMyJam(smtr, index=0, play_all=False)
        elif menu1=="3":
            print("Markov application")
            choosemarkov(dadict)
        break



def deconvert(codeNotes):
    mapNote = {"DO" : 0, "RE" : 2,"MI" : 3,"FA" : 4,"SOL" : 5, "LA" : 6, "SI" : 7, "Z":8}
    aString = ''
    times = ["b", "r", "n", "c"]
    for code in codeNotes:
        for key, values in mapNote.items():
            if code == values:
                aString += key+random.choice(times)+' '
    times = ["b", "r", "n", "c"]
    return aString

def conversion(aString):
    codedNotes = []
    daNotes = ["DO", "RE", "MI", "FA", "SOL", "LA","SI"]
    mapNote = {"DO" : 0, "RE" : 2,"MI" : 3,"FA" : 4,"SOL" : 5, "LA" : 6, "SI" : 7,"Z": 8}
    notes = aString.rsplit(' ')
    for i in range(len(notes)) : 
        if notes[i][-1] == '\n':
            notes[i] = notes[i][:-1]
        notes[i] = notes[i][:-1]
    for key,note in enumerate(notes):
        if note in daNotes:
            pass
        else:
            notes.pop(key)
    for note in notes : 
        val = mapNote[note]
        codedNotes.append(val)
    return codedNotes

def Inverse(b, numnote):
    l=b+1
    inv=[]
    for i in numnote:
        s=(l-i)%l
        inv.append(s)
    return inv

def Transpose(b,k,alist):
    l=b+1
    trans=[]
    for i in alist:
        s=(i+k)%l
        trans.append(s)
    return trans

from dating import *
import os
#initialisation du fishier 
rePath = 'partitions.txt'
try:
    part, numpart = read_txt_file(rePath)
    global dadict 
    dadict = makeDict(numpart, part)
except FileNotFoundError :
    print("Fishier partions.txt introuvable, trouvez le et relancez"
            )


def main():
    while True:
        print("""
        1.Voir toutes les partitions
        2.Jouer une partition
        3.Jouer toutes les partitions
        4.Transformation (markov/inversion/transposition)
        5.Ajouter une nouvelle partition
        6.Quitter
        """)
        menu1=input("Choisir le numéro de l'option ")
        if menu1=="1":
                list_partitions(dadict,printEm=True)
        elif menu1=="2":
            print("\n Jouer une partition")
            list_of_partitions = list_partitions(dadict, printEm=True)
            indexx = int(input("Jouer partition numéro ?  :"))
            playMyJam(dadict, index=indexx, play_all=False) 
        elif menu1=="3":
            print("Jouer toutes vos partitions")
            playMyJam(dadict, play_all=True)
        elif menu1=="4":
            Transformation(dadict)
        elif menu1=="5":
            print("\n Ajouter une partition dans une liste")                        
            user_input =input("Enter the path of your file: ")
            assert os.path.exists(user_input), "I did not find the file at, "+str(user_input)
            part , numpart = read_txt_file(user_input)
            dict2 = makeDict(par,numpart) 
            append_text_file(rePath,dic2)
        elif menu1=="6":
            print("\n Goodbye") 
            break
        else:
            print("\n Not Valid Choice Try again")


if __name__ == "__main__":
    main()

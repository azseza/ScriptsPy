import sys
'''doin this for fun pls '''

f = open(sys.argv[1])
howM = int(sys.argv[2])

with open("output.txt", "w+") as output:
    lines = f.readline()
    while lines:
        words = lines.split()
        for word in words:
            for i in word:
                output.write(chr(ord(i)+howM))
            output.write(' ')
        lines = f.readline()
        if lines == "":
            break
output.close()
f.close()

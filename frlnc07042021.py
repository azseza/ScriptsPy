"""Python script for automating tasks
@uthor : azseza
"""
import csv
import subprocess
from typing import List
import os
import time

def praseall(projects : list) -> list:
    lscmd = '/c/Devops/oc/oc.exe get ns   grep -v "openshift" '
    #lsout = subprocess.check_output(lscmd, shell=True)
    lsout = os.system(lscmd)
    p1 = subprocess.Popen(['/c/Devops/oc/oc.exe', 'get', 'ns'], stdout=subprocess.PIPE)
    p2 = subprocess.Popen(["grep", "openshift"], stdin=p1.stdout, stdout=subprocess.PIPE)
    p1.stdout.close()  
    lsout = p2.communicate()[0]
    print(lsout)
    for row in lsout.split('\n') : 
        projects.append(row)    
    print(projects)
    projects.remove(projects[0])
    for project in projects:
        a = project.split(' ')
        project = a[0]
    print(projects)
    return projects


def getProject(projectName):
    #projectName = input("enter project name:")
    fullCmd = "/c/DevOps/oc/oc.exe -n "+ projectName + " get rolebindings.authorization"
    try : 
        projectOutput = subprocess.check_output(fullCmd, shell=True)
        print("prased projet attributes")
        return projectOutput, name 
    except Exception:
        print("See if the project name exists ! ")

def parseProject(output, name):    
    keys = ["Project Name","Role","User","Group","Services Account"]
    ffile = name+'.csv'
    with open(ffile,"w") as csvfile : 
        writer = csv.writer(csvfile)
        writer.writerow(keys)
        print("intializing for "+projects)
        for row in output.split('\n'): 
            print("2 ")
            roww = row.split(' ')
            writer.writerow(roww) 
            csvfile.flush()  

if __name__ == '__main__':
    tic = time.time()
    projects = []
    praseall(projects)
    print("getting ready ..")
    for project in projects:
        out, name = getProject(project)
        parseProject(out, name)
        print("created "+ projects+"description")
    toc = time.time()
    print("finshed in "+ str(tic-toc))
##################################################
## Highlighting arXiv Papers on terminal screen ##
## Author: Arnab Laha                           ##
## Email : laha.arnab@students.iiserpune.ac.in  ##
##################################################

import subprocess
import os,sys
import time

start_time=time.time()

### Install libraries if not present in the system
try:
    import bs4
    import tabulate
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'bs4'])
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'tabulate'])
finally:
    from urllib.request import urlopen
    from bs4 import BeautifulSoup
    from tabulate import tabulate


################# USER INPUT ######################

url = "https://arxiv.org/list/hep-ex/pastweek?show=500"    ## arXiv Link for pastweek| show max 500 papers if available
#url  ="https://arxiv.org/list/hep-ex/2203?show=1000"      ## Paper in a month

#####################################################


html = urlopen(url).read()
soup = BeautifulSoup(html, features="html.parser")
# kill all script and style elements
for script in soup(["script", "style"]):
    script.extract()    #rip it out  
    
# get text
text = soup.get_text()
# break into lines and remove leading and trailing space on each
#lines = (line.strip() for line in text.splitlines())
# break multi-headlines into a line each
#chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
# drop blank lines
#text = '\n'.join(chunk for chunk in chunks if chunk)                                                                                    

#Define a function to show today's paper
info =[]

def htmlpage(paperinfo):
    style="<head>\n<style>\ntable {\nfont-family: arial, sans-serif;\nborder-collapse: collapse;\nwidth: 100%;\n    }\ntd, th {\nborder: 1px solid #757575;\ntext-align: center;\npadding: 12px;\n}\ntr:nth-child(even) {\nbackground-color: #D1FBC1;\n}\n</style>\n</head>\n"
    w3style='<meta name="viewport" content="width=device-width, initial-scale=1">\n<link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">\n'
    heading= '<div class="w3-container w3-center">\n <h2>This week arXiv Papers</h2>\n</div>'
    
    file=open("index.html","w")    
    file.writelines(["<!DOCTYPE html>\n","<html>\n"])
    file.write(style)
    file.write(w3style)
    file.write("<body>\n")
    file.write(heading)
    file.write(" <table>\n")
    file.write("  <tr>\n")
    file.write("   <th>Index</th>\n")
    file.write("   <th>arXivLink</th>\n")
    file.write("   <th>Paper</th>\n</tr>\n")
    
    for item in paperinfo:
        file.write(" <tr>\n")
        file.write("  <td>"+item[0]+"</td>\n")
        file.write("  <td><a href=\""+item[1]+"\">"+item[1]+"</a></td>\n")
        file.write("  <td>"+item[2]+"</td>\n")
        file.write("</tr>\n")
        
    file.write("</table\n>")
    file.write("</body>\n")
    file.write("</html>\n")
    
def CheckPaper():
    list_ByarXivLink=text.split("Title: ")
    ## Quick Debug
    #print(list_ByarXivLink[1].split("\n\n\nAuthors:")[0].split("  "))
    #print(list_ByarXivLink[0].split("arXiv:")[1][:10])
    for i in range(1,len(list_ByarXivLink),1):
        arxivlink=list_ByarXivLink[i-1].split("arXiv:")[1][:10]
        papername= '\n'.join(list_ByarXivLink[i].split("\n\n\nAuthors:")[0].split("  "))
        info.append([str(i),'https://arxiv.org/abs/'+str(arxivlink),papername])
    colname = ['Index','arXiv Link','Paper']
    print(tabulate(info,headers=colname,tablefmt='fancy_grid',numalign='center'))
    htmlpage(info)
    os.system("firefox index.html")
    info.clear()

print("\n")
print("                   *******************************************************              ")
print("                   **        Hi! Your arXiv papers of the past week     **              ")
print("                   **                                                   **              ")
print("                   **                                                   **              ")
print("                   *******************************************************              ")
CheckPaper()
end_time=time.time()    
print("                                  Time taken: %.2f" %(end_time-start_time) +" sec       ")
print("                                    Have a good day!                                  \n")
text=''



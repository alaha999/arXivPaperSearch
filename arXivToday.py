import subprocess
import sys
import time

start_time=time.time()

### Install Libraries if not present in the system
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
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Create a text file out of the html page
url = "https://arxiv.org/list/hep-ex/pastweek?show=500"  ## arXiv Link for pastweek| show max 500 papers if available
html = urlopen(url).read()
soup = BeautifulSoup(html, features="html.parser")

# kill all script and style elements
for script in soup(["script", "style"]):
    script.extract()    # rip it out

# get text
text = soup.get_text()
# break into lines and remove leading and trailing space on each
lines = (line.strip() for line in text.splitlines())
# break multi-headlines into a line each
chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
# drop blank lines
text = '\n'.join(chunk for chunk in chunks if chunk)



#Define a function to show today's paper
info =[]
def CheckPaper():
    list_ByarXivLink=text.split("Title: ")

    ## Quick Debug
    #print(list_ByarXivLink[1].split("Authors:")[0])
    #print(list_ByarXivLink[0].split("arXiv:")[1][:10])
    for i in range(1,len(list_ByarXivLink),1):
        arxivlink=list_ByarXivLink[i-1].split("arXiv:")[1][:10]
        papername=list_ByarXivLink[i].split("Authors:")[0]
        info.append([str(i),'https://arxiv.org/abs/'+str(arxivlink),papername])
    colname = ['Index','arXiv Link','Paper']
    print(tabulate(info,headers=colname,tablefmt='fancy_grid',numalign='center'))

end_time=time.time()    
print("\n")
print("                   *******************************************************              ")
print("                   **        Hi! Your arXiv papers of the past week     **              ")
print("                   **                                                   **              ")
print("                   **               Time taken: %.2f" %(end_time-start_time) +" sec                ** ")
print("                   **                                                   **              ")
print("                   **               Author: Arnab Laha                  **              ")
print("                   **         laha.arnab@students.iiserpune.ac.in       **              ")
print("                   *******************************************************              ")
CheckPaper()
print("\n")
print("                                    Have a good day!                                  \n")
info.clear()

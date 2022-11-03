##################################################
## Highlighting arXiv Papers on terminal screen ##
## Author: Arnab Laha                           ##
## Email : laha.arnab@students.iiserpune.ac.in  ##
##################################################

import subprocess
import os,sys
import time,datetime
import argparse

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


################# PARSING #########################
parser = argparse.ArgumentParser()
parser.add_argument('--collab',type=str,required=False,help='mention collaboration such as --collab CMS')
parser.add_argument('--time',type=str,required=False,help='mention time period such as --time monthly')
parser.add_argument('--year',type=str,required=False,help='mention year such as --year 2022')
args = parser.parse_args()


################# USER INPUT ######################
CName=args.collab
TimePeriod=args.time
InputYear= args.year


################# MonthDatabase ###################
year=datetime.datetime.now().strftime("%y")           #current year 
Month=datetime.datetime.now().strftime("%B")          #current month

if(InputYear==None):
    year=datetime.datetime.now().strftime("%Y"); InputYear=year                           #default year
elif(int(InputYear)>2022):
    sys.exit("\n Hangover, pal? :) We are still at 20"+year+"! and Month is "+Month+"\n") #future year error
else: 
    year=InputYear[2:]                                                                    #customized year

#Dictionary to help the url setup    
monthdict={"Jan":year+"01","Feb":year+"02","Mar":year+"03","Apr":year+"04","May":year+"05","Jun":year+"06",
           "Jul":year+"07","Aug":year+"08","Sep":year+"09","Oct":year+"10","Nov":year+"11","Dec":year+"12" }

#################  SET URL ##########################
hepex="https://arxiv.org/list/hep-ex/"
if(TimePeriod==None):url=hepex+"pastweek?show=500"; monthStr=Month                         #pastweek #default
elif(TimePeriod=="weekly"):url=hepex+"pastweek?show=500"; monthStr=Month                   #pastweek
elif(TimePeriod=="monthly"):url=hepex+datetime.datetime.now().strftime("%y%m")+"?show=1000"; monthStr=Month #monthly
else:url=hepex+monthdict[TimePeriod]+"?show=1000"; monthStr=TimePeriod                     #customized month and year

#print(url)

################## SCRAP HTML #######################
html = urlopen(url).read()
soup = BeautifulSoup(html, features="html.parser")
# kill all script and style elements
for script in soup(["script", "style"]):
    script.extract()    #rip it out  
    
# get text
text = soup.get_text()

#date
dateString=datetime.datetime.now().strftime("%d"+" "+"%b"+" "+"%Y")

#Define a function to show today's paper
info =[]
def htmlpage(paperinfo):
    style="<head>\n<style>\ntable {\nfont-family: arial, sans-serif;\nborder-collapse: collapse;\nwidth: 100%;\n    }\ntd, th {\nborder: 1px solid #757575;\ntext-align: center;\npadding: 12px;\n}\ntr:nth-child(even) {\nbackground-color: #FFFDE7;\n}\n</style>\n</head>\n"
    
    file=open("index.html","w")    
    file.writelines(["<!DOCTYPE html>\n","<html>\n"])
    file.write(style)
    file.write("<body>\n")
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
    #print(list_ByarXivLink[29].split("\n\n\nAuthors:")[1].split("\n\n\nComments")[0].lstrip(" \n"))#.split("  "))
    #print(list_ByarXivLink[0].split("arXiv:")[1][:10])
    if(CName != None):
        print("\nYou've selected to show only "+CName+" papers for the month "+monthStr+" "+InputYear+" and Today is "+dateString+"\n")
    else:
        print("\nYou've selected to show all papers for the month "+monthStr+" "+year+" and Today is "+dateString+"\n")
        
    for i in range(1,len(list_ByarXivLink),1):
        arxivlink=list_ByarXivLink[i-1].split("arXiv:")[1][:10]
        papername= '\n'.join(list_ByarXivLink[i].split("\n\n\nAuthors:")[0].split("  "))
        if(CName!=None):
            collabName=list_ByarXivLink[i].split("\n\n\nAuthors:")[1].split("\n\n\nComments")[0].lstrip(" \n")
            if(collabName.endswith("Collaboration") or collabName.endswith("collaboration") ):
                if(collabName[collabName.find(CName):(collabName.find(CName)+len(CName))].startswith(CName)):
                    info.append([str(i),'https://arxiv.org/abs/'+str(arxivlink),papername])
        else:
            info.append([str(i),'https://arxiv.org/abs/'+str(arxivlink),papername])
            
    #print        
    colname = ['Index','arXiv Link','Paper']
    print(tabulate(info,headers=colname,tablefmt='fancy_grid',numalign='center'))
    htmlpage(info)
    os.system("firefox index.html")
    info.clear()

#title
if(TimePeriod==None or TimePeriod=='weekly'):title="Hi! Your arXiv papers this week "
elif(TimePeriod=='monthly'):title="Hi! Your arXiv papers this month"
else: title = "Hi! Your arXiv papers list"

print("\n")
print("                   *******************************************************              ")
print("                                      "+title+"                                         ")
print("                                                                                        ")
print("                   *******************************************************              ")
CheckPaper()
end_time=time.time()    
print("                                  Time taken: %.2f" %(end_time-start_time) +" sec       ")
print("                                    Have a good day!                                  \n")
text=''


print("How to use this code\n===================")
print("Current week,  Current year, ALL papers ====> $python3 arXivAdvanced.py")
print("Current week,  Current year, CMS papers ====> $python3 arXivAdvanced.py --collab CMS")
print("Current month, Current year, CMS papers ====> $python3 arXivAdvanced.py --collab CMS --time monthly")
print("Custom  month, Custom  year, CMS papers ====> $python3 arXivAdvanced.py --collab CMS --time May --year 2020")
print("\nArgument Options\n===================")
print("--collab: CMS/ATLAS/Belle, --time weekly/monthly/First Three Letters of Month(e.g. Dec), --year XXXX \n")

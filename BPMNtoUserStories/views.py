from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import xml.etree.ElementTree as ET
import os


def masterpages(request):
     return render(request,'masterpage.html')

def home(request):
     return render(request,'home.html')
     
def uploadpage(request):
     return render(request,'uploadfile.html')

def parsing(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['xml']
        fs = FileSystemStorage()
        fs.save(uploaded_file.name, uploaded_file)
        dir = ('.\media')
        file_name = str(uploaded_file.name)
        full_path = os.path.join(dir,file_name)
        file_output = "clean" +file_name
        full_path_new = os.path.join(dir,file_output)
        with open(full_path, 'r') as infile, open(full_path_new, "w") as outfile:
            data = infile.read()
            data = data.replace('xmlns="http://www.wfmc.org/2009/XPDL2.2"', '')
            outfile.write(data)

        context = {}
        with open(full_path_new, 'r') as filexml :
            tree = ET.parse(filexml)
            root = tree.getroot()
            list_actor = []
            list_activity = []
            for i in tree.findall('.//Lane'):
                name = i.get('Name')
                list_actor.append(name)
            for i in tree.findall('.//Activity'):
                activity = i.get('Name')
                if (activity != "Start" and activity != "End" and activity != None):
                    list_activity.append(activity)
            total_actor = len(list_actor)
            
            

            # mengecek apakah total aktor lebih dari satu dan mengambil nilai koordinat dari setiap lane didalam array
            if (total_actor > 1): 
                Lane_Coordinates = [] #koordinat sumbu y dari setiap swimlane
                for act in tree.findall('.//Lanes'):
                    for sub_child in act.findall('.//Coordinates'):
                        Y_Coordinates = sub_child.get('YCoordinate')
                        Y_Coordinates_cnvrt = int(Y_Coordinates)
                        Lane_Coordinates.append(Y_Coordinates_cnvrt)
                uniques=[]
                dups=[]

                Y_ordinate=[] #Y_Ordinate merupakan variable koordinate y dari setiap aktivitas/activity
                for check in tree.findall('.//Activity'):
                    for sub_ordinate in check.findall('.//Coordinates'):
                        ordinate_y = sub_ordinate.get('YCoordinate')
                        ordinate_y_cnvrt = int(ordinate_y)
                        Y_ordinate.append(ordinate_y_cnvrt)
                
                last_actor=[]
                actor_before_last=[]
                for j in range (0,len(Lane_Coordinates)):
                    for i in range (0,len(Y_ordinate)):
                        # if (Y_ordinate[i] > Lane_Coordinates[j] and Y_ordinate[i] < Lane_Coordinates[j+1]):
                        #     actor_before_last.append(Y_ordinate[i])
                        if (Y_ordinate[i] > Lane_Coordinates[len(Lane_Coordinates)-1]):
                            last_actor.append(Y_ordinate[i])

                print("===LAST ACTOR ACTIVITY===")
                print(last_actor)
                # print("===ACTOR BEFORE LAST===")
                # print(actor_before_last)

                # for each in Coordinates:
                #     if each not in uniques:
                #         uniques.append(each)
                #     else:
                #         dups.append(each)
                # print(dups)
                # for i in range (0,len(Coordinates)):
                #     for j in range (i+1,len(Coordinates)):
                #         if (Coordinates[i] == Coordinates[j]):
                #             final_coordinate.append(Coordinates[i])
                
                            
                        # for check in sub_child:
                        #     check = check.get('YCoordinate')
                        #     if (Y_Coordinates == check):

            else : 
                print("less than 2")

        context = {'list_actor':list_actor, 'list_activity':list_activity,'total_actor':total_actor}
    return render(request,'userstoriesresult.html',context)

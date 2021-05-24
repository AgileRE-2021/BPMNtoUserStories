from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import xml.etree.ElementTree as ET
import os


def masterpages(request):
     return render(request,'masterpage.html')

def home(request):
     return render(request,'home.html')
     
def about(request):
     return render(request,'about.html')

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
        with open(full_path, 'r') as infile, open(full_path_new, "w") as outfile: #MEMBERSIHKAN FORMAT XPDL AGAR TAG PADA XML TERDEFINISI
            data = infile.read()
            data = data.replace('xmlns="http://www.wfmc.org/2009/XPDL2.2"', '')
            outfile.write(data)

        context = {}
        with open(full_path_new, 'r') as filexml :
            tree = ET.parse(filexml)
            root = tree.getroot()
            list_actor = []
            list_activity = []
            for i in tree.findall('.//Lane'):       #PASSING UNTUK NILAI KOMPONEN USER STORIES
                name = i.get('Name')
                list_actor.append(name)
            for i in tree.findall('.//Activity'):
                activity = i.get('Name')
                if (activity != "Start" and activity != "End" and "?" not in activity and activity != None):
                    list_activity.append(activity)
            total_actor = len(list_actor)
            

            # mengecek apakah total aktor lebih dari satu dan mengambil nilai koordinat dari setiap lane didalam array
            if (total_actor > 1): 
                Lane_Coordinates = [] #koordinat sumbu y dari setiap swimlane
                for act in tree.findall('.//Lanes'):
                    for sub_child in act.findall('.//Coordinates'):
                        Y_Coordinates = sub_child.get('YCoordinate')
                        Y_Coordinates_cnvrt = float(Y_Coordinates)
                        Lane_Coordinates.append(Y_Coordinates_cnvrt)
                
                Y_ordinate=[] #Y_Ordinate merupakan variable koordinate y dari setiap aktivitas/activity
                for check in tree.findall('.//Activity'):
                    for sub_ordinate in check.findall('.//Coordinates'):
                        ordinate_y = sub_ordinate.get('YCoordinate')
                        print(type(ordinate_y))
                        ordinate_y_cnvrt = float(ordinate_y)
                        Y_ordinate.append(ordinate_y_cnvrt)
                
                Array = []
                ACT = []
                for i in tree.findall('.//Lane'):  
                    name = i.get('Name')
                    ACT.append(name)

                for i in range (0,len(ACT)):
                    ACT[i] = []
                    Array.append(ACT[i])

                if (len(list_actor)>2):
                    for j in range (1,(len(Lane_Coordinates)-1)):
                        for i in range (0,len(Y_ordinate)):
                            if (Y_ordinate[i] < Lane_Coordinates[len(Lane_Coordinates)-(len(Lane_Coordinates)-1)]): #Mendefinisikan Aktor Pertama dan Koordinat Y
                                ACT[0].append(Y_ordinate[i])
                                ACT[0] = list(set(ACT[0]))
                            elif (Y_ordinate[i] > Lane_Coordinates[len(Lane_Coordinates)-1]):
                                ACT[(len(Lane_Coordinates)-1)].append(Y_ordinate[i])
                                ACT[(len(Lane_Coordinates)-1)] = list(set(ACT[(len(Lane_Coordinates)-1)]))
                            elif (Y_ordinate[i]>Lane_Coordinates[j] and Y_ordinate[i]<Lane_Coordinates[j+1]):
                                ACT[j].append(Y_ordinate[i])
                                ACT[j] = list(set(ACT[j]))
                else:
                    for i in range (0,len(Y_ordinate)):
                        for j in range (0,len(Y_ordinate)):
                            if (Y_ordinate[i] < Lane_Coordinates[len(Lane_Coordinates)-(len(Lane_Coordinates)-1)]): #Mendefinisikan Aktor Pertama dan Koordinat Y
                                ACT[0].append(Y_ordinate[i])
                                ACT[0] = list(set(ACT[0]))
                            elif (Y_ordinate[i] > Lane_Coordinates[len(Lane_Coordinates)-1]):
                                ACT[(len(Lane_Coordinates)-1)].append(Y_ordinate[i])
                                ACT[(len(Lane_Coordinates)-1)] = list(set(ACT[(len(Lane_Coordinates)-1)]))
                                    
                for j in range (0,(len(ACT))):
                    for i in range (0,(len(ACT[j]))):
                        checking = ACT[j][i]
                        for elem in tree.findall('.//Activity/NodeGraphicsInfos/NodeGraphicsInfo/Coordinates[@YCoordinate="%s"]......' %checking):
                            activity_multiple = elem.get('Name')
                            ACT[j].append(activity_multiple)
                      
                for i in tree.findall('.//Lane'):       #MENAMBAHKAN AKTOR KEDALAM ARRAY
                    name = i.get('Name')
                    ACT.append(name)

                # for i in range (0,len(ACT)):
                #     print(ACT[i])

            else : 
                print("less than 2")

        context = {'list_actor':list_actor, 'list_activity':list_activity,'total_actor':total_actor}
    return render(request,'userstoriesresult.html',context)

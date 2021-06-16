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
            for i in tree.findall('.//Activity/Implementation/Task/.....'):
                activity = i.get('Name')
                print(activity)
                if (activity != "Start" and activity != "End" and "?" not in activity and activity):
                    list_activity.append(activity)
            total_actor = len(list_actor)
            

            Artifacts = []
            for i in tree.findall('.//Artifact'):
                annotation = i.get('ArtifactType')
                print(annotation)
                if (annotation == "Annotation"):
                    Artifacts.append(annotation)
            
            # mengecek apakah total aktor lebih dari satu dan mengambil nilai koordinat dari setiap lane didalam array
            if (total_actor > 1): 
                koordinatX = [] #koordinat sumbu x dari setiap swimlane
                koordinatY = [] #koordinat sumbu y dari setiap swimlane
                for act in tree.findall('.//Lanes'):
                    for sub_child in act.findall('.//Coordinates'):
                        Y_Coordinates = sub_child.get('YCoordinate')
                        X_Coordinates = sub_child.get('XCoordinate')
                        koordinatY.append(Y_Coordinates)
                        koordinatX.append(X_Coordinates)

                if (koordinatX[0]==koordinatX[1]): #CHECKING KOORDINAT Y 
                    Y_ordinate=[] #Y_Ordinate merupakan variable koordinate y dari setiap aktivitas/activity
                    for check in tree.findall('.//Activity/Implementation/Task/.....'):
                        for sub_ordinate in check.findall('.//Coordinates'):
                            ordinate_y = sub_ordinate.get('YCoordinate')
                            Y_ordinate.append(ordinate_y)   #SUMBU Y DARI SETIAP ACTIVITY
                    
                    Array = []
                    ACT = []
                    for i in tree.findall('.//Lane'):  
                        name = i.get('Name')
                        ACT.append(name)

                    for i in range (0,len(ACT)):
                        ACT[i] = []
                        Array.append(ACT[i])

                    print(koordinatY)
                    if (len(list_actor)>2):
                        for j in range (1,(len(koordinatY)-1)):
                            for i in range (0,len(Y_ordinate)):
                                if (Y_ordinate[i] < koordinatY[len(koordinatY)-(len(koordinatY)-1)]): #Mendefinisikan Aktor Pertama dan Koordinat Y
                                    ACT[0].append(Y_ordinate[i])
                                    ACT[0] = list(set(ACT[0]))
                                elif (Y_ordinate[i] > koordinatY[len(koordinatY)-1]):
                                    ACT[(len(koordinatY)-1)].append(Y_ordinate[i])
                                    ACT[(len(koordinatY)-1)] = list(set(ACT[(len(koordinatY)-1)]))
                                elif (Y_ordinate[i] > koordinatY[j] and Y_ordinate[i] < koordinatY[j+1]):
                                    ACT[j].append(Y_ordinate[i])
                                    ACT[j] = list(set(ACT[j]))
                    else:
                        for i in range (0,len(Y_ordinate)):
                            for j in range (0,len(Y_ordinate)):
                                if (Y_ordinate[i] < koordinatY[len(koordinatY)-(len(koordinatY)-1)]): #Mendefinisikan Aktor Pertama dan Koordinat Y
                                    ACT[0].append(Y_ordinate[i])
                                    ACT[0] = list(set(ACT[0]))
                                elif (Y_ordinate[i] > koordinatY[len(koordinatY)-1]):
                                    ACT[(len(koordinatY)-1)].append(Y_ordinate[i])
                                    ACT[(len(koordinatY)-1)] = list(set(ACT[(len(koordinatY)-1)]))
                    
                    print(Array)
                    print(ACT)

                    # print(Array)
                    # print(ACT)

                    deleted_index = []
                    for i in range (0,len(ACT)):
                        deleted = len(ACT[i])
                        deleted_index.append(deleted)
                    
                    arr_Y = []
                    arr_Name = []
                    for j in range (0,(len(ACT))):
                        for i in range (0,(len(ACT[j]))):
                            checking = ACT[j][i]
                            for elem in tree.findall('.//Activity/NodeGraphicsInfos/NodeGraphicsInfo/Coordinates[@YCoordinate="%s"]......' %checking):
                                id = elem.get('Id') #coba
                                activity_multiple = elem.get('Name')
                                # if (activity_multiple != "Start" and activity_multiple != "End" and "?" not in activity_multiple and activity_multiple):
                                ACT[j].append(activity_multiple) #coba
                                    # arr_Name.append(activity_multiple)
                                    # arr_Name.append(activity_multiple) #coba
                                    # ACT[j].append(activity_multiple)
                   
                    
                    #ASPECT OF WHY PROCESSING
                    # if (len(Artifacts)>0):
                    #     Arr_Pair = []  #Pasangan Activity dengan Association
                    #     why = []
                    #     for i in range (0,len(Artifacts)):
                    #         why.append("X")
                    #     for i in range (0,len(why)):
                    #         why[i] = []
                    #         Arr_Pair.append(why[i])

                    #     source_array = []                           #inserted source to array
                    #     for j in tree.findall('.//Association'):
                    #         Source = j.get('Source')
                    #         for elem in tree.findall('.//Activity[@Id="%s"]' %Source):
                    #             id_act = elem.get('Id')
                    #             source_array.append(id_act)
                        
                    #     target_array = []                           #inserted source to array
                    #     for j in tree.findall('.//Association'):
                    #         Target = j.get('Target')
                    #         for elem in tree.findall('.//Artifact[@Id="%s"]' %Target):
                    #             Text_annotation = elem.get('TextAnnotation')
                    #             target_array.append(Text_annotation)
                        
                    #     for i in range (0,len(why)):
                    #         why[i].append(source_array[i])
                    #         why[i].append(target_array[i])
                    #     print(why)          
                        

                    for i in range (0,len(ACT)):                #MENDELETE HANYA KOORDINAT Y SAJA
                        for j in range (0,deleted_index[i]):
                            ACT[i].pop(0)
                    
                    # for i in range (0,len(ACT)):                
                    #     for j in range (0,len(ACT[i])):         
                    #         appendix = ACT[i][j]
                    #         ACT[i][j] = []
                    #         ACT[i][j].append(appendix)
                    #         ACT[i][j].append(list_actor[i])
                    #         for elem in tree.findall('.//Activity[@Id="%s"]' %appendix):
                    #             activities = elem.get('Name')
                    #             ACT[i][j].append(activities)
                    
                    # for i in range (0,len(ACT)):                
                    #     for j in range (0,len(ACT[i])):   
                    #         for z in range (0,len(why)):
                    #             if (ACT[i][j][0]==why[z][0]):
                    #                 ACT[i][j].append(why[z][1])
                    
                    # for i in range (0,len(ACT)):
                    #     for j in range (0,len(ACT[i])):                  #MENDELETE HANYA KOORDINAT Y SAJA
                    #         for z in range (0,1):
                    #             ACT[i][j].pop(0)

                    # print("") #coba
                    # print("") #coba
                    # print("==HASIL ID BERDASARKAN KOORDINAT==") #coba
                    # for i in range (0,len(ACT)):
                    #     for j in range (0,len(ACT[i])): 
                    #         if (len(ACT[i][j])==3):
                    #             print ("I as " + ACT[i][j][0] + ", i can " + ACT[i][j][1] + ", so that " + why[z][1] )
                    #         else :
                    #             print ("I as " + ACT[i][j][0] + ", i can " + ACT[i][j][1])

                    for i in range (0,len(ACT)):
                        ACT[i].append(list_actor[i])
                    
                    # for i in range (0,len(ACT)):
                    #     for z in range (0,len(why)):
                    #         for j in range (0,len(ACT[i])-1):
                    #             if (why[z][0]==ACT[i][j]):
                    #                 print ("I as " + ACT[i][len(ACT[i])-1] + ", i can " + ACT[i][j] + ", so that " + why[z][1] )
                    #             else :
                    #                 print ("I as " + ACT[i][len(ACT[i])-1] + ", i can " + ACT[i][j] )
                            

                context = {'list_actor':list_actor, 'list_activity':list_activity,'total_actor':total_actor,'ACT':ACT}
                return render(request,'userstoriesresult.html',context)
            else : 
                print("less than 2")
                context = {'list_actor':list_actor, 'list_activity':list_activity,'total_actor':total_actor}
                return render(request,'userstoriesresult.html',context)


def history(request):
    return render(request,'history.html')


# def generate_pdf(request):
#     html_string = render_to_string('pdf.html')
#     html = HTML(string=html_string)
#     result = html.write_pdf()

# class PDFUserDetailView(PDFTemplateResponseMixin, DetailView):
#     model = get_user_model()
#     template_name = 'user_detail.html'

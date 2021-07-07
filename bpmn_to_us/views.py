from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import xml.etree.ElementTree as ET
import os
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from .models import BPMN, TextUserStory, UserStories
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

from .render import Render
from django.views.generic import View

class Pdf(View):

    def getpdf(request,id):
        text_user_story = TextUserStory.objects.filter(id_us=id)
        params = {
            'data': text_user_story,
        }
        return Render.render('result_pdf.html', params)

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

            if(len(list_actor) < 1):
                list_actor.append("User")
                
            for i in tree.findall('.//Activity/Implementation/Task/.....'):         
                activity = i.get('Name')
                subject = "i"
                space = " "
                adverb = "can"
                space2 = " "
                raw_percobaan = subject + space + adverb + space2 + activity
                raw_percobaan = raw_percobaan.casefold()
                text = nltk.word_tokenize(raw_percobaan)
                print(text[1])

                POS = nltk.pos_tag(text)
                print("POS")
                print(POS)

                print("===VERBS===")
                print(POS[2][0])
                if (POS[2][1]=='VBP' or POS[2][1]=='VB' or POS[2][1]=='VBD' or POS[2][1]=='VBZ' or POS[2][1]=='VBN' or POS[2][1]=='VBG'):
                    for i in range(3,len(POS)):
                        if (POS[i][1]=='NN'):
                            if (activity != "Start" and activity != "End" and "?" not in activity and activity):
                                list_activity.append(activity.casefold())
                                break

            Artifacts = []
            TextAnnotation = []
            for i in tree.findall('.//Artifact'):
                annotation = i.get('ArtifactType')
                text = i.get('TextAnnotation')
                TextAnnotation.append(text)
                print(annotation)
                if (annotation == "Annotation"):
                    Artifacts.append(annotation)
            
            total_actor = len(list_actor)


            if (total_actor > 1): 
                koordinatX = []
                koordinatY = []
                for act in tree.findall('.//Lanes'):
                    for sub_child in act.findall('.//Coordinates'):
                        Y_Coordinates = sub_child.get('YCoordinate')
                        X_Coordinates = sub_child.get('XCoordinate')
                        koordinatY.append(Y_Coordinates)
                        koordinatX.append(X_Coordinates)

                if (koordinatX[0]==koordinatX[1]):
                    Y_ordinate=[] 
                    for check in tree.findall('.//Activity/Implementation/Task/.....'):
                        for sub_ordinate in check.findall('.//Coordinates'):
                            ordinate_y = sub_ordinate.get('YCoordinate')
                            Y_ordinate.append(ordinate_y)   
                    
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
                                if (Y_ordinate[i] < koordinatY[len(koordinatY)-(len(koordinatY)-1)]):
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
                                if (Y_ordinate[i] < koordinatY[len(koordinatY)-(len(koordinatY)-1)]):
                                    ACT[0].append(Y_ordinate[i])
                                    ACT[0] = list(set(ACT[0]))
                                elif (Y_ordinate[i] > koordinatY[len(koordinatY)-1]):
                                    ACT[(len(koordinatY)-1)].append(Y_ordinate[i])
                                    ACT[(len(koordinatY)-1)] = list(set(ACT[(len(koordinatY)-1)]))
                    
                    print(Array)
                    print(ACT)


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
                                id = elem.get('Id')
                                activity_multiple = elem.get('Name')
                                subject = "i"
                                space = " "
                                adverb = "can"
                                space2 = " "
                                raw_percobaan = subject + space + adverb + space2 + activity_multiple
                                raw_percobaan = raw_percobaan.casefold()
                                text = nltk.word_tokenize(raw_percobaan)
                                print(text[1])

                                POS = nltk.pos_tag(text)
                                print("POS")
                                print(POS)


                                print("===VERBS===")
                                print(POS[2][0])
                                if (POS[2][1]=='VBP' or POS[2][1]=='VB' or POS[2][1]=='VBD' or POS[2][1]=='VBZ' or POS[2][1]=='VBN' or POS[2][1]=='VBG'):
                                    for x in range(3,len(POS)):
                                        if (POS[x][1]=='NN'):
                                            ACT[j].append(id)
                                            break
                        

                    if (len(Artifacts)>0):
                        Arr_Pair = []  
                        why = []
                        for i in range (0,len(Artifacts)):
                            why.append("X")
                        for i in range (0,len(why)):
                            why[i] = []
                            Arr_Pair.append(why[i])

                        source_array = []                         
                        for j in tree.findall('.//Association'):
                            Source = j.get('Source')
                            for elem in tree.findall('.//Activity[@Id="%s"]' %Source):
                                id_act = elem.get('Id')
                                source_array.append(id_act)
                        
                        target_array = []                          
                        for j in tree.findall('.//Association'):
                            Target = j.get('Target')
                            for elem in tree.findall('.//Artifact[@Id="%s"]' %Target):
                                Text_annotation = elem.get('TextAnnotation')
                                target_array.append(Text_annotation)
                        
                        for i in range (0,len(why)):
                            why[i].append(source_array[i])
                            why[i].append(target_array[i])
                        print(why)          
                        

                        for i in range (0,len(ACT)):               
                            for j in range (0,deleted_index[i]):
                                ACT[i].pop(0)
                        
                        for i in range (0,len(ACT)):                
                            for j in range (0,len(ACT[i])):         
                                appendix = ACT[i][j]
                                ACT[i][j] = []
                                ACT[i][j].append(appendix)
                                ACT[i][j].append(list_actor[i])
                                for elem in tree.findall('.//Activity[@Id="%s"]' %appendix):
                                    activities = elem.get('Name')
                                    ACT[i][j].append(activities)
                        
                        for i in range (0,len(ACT)):                
                            for j in range (0,len(ACT[i])):   
                                for z in range (0,len(why)):
                                    if (ACT[i][j][0]==why[z][0]):
                                        ACT[i][j].append(why[z][1])
                    else:
                        for i in range (0,len(ACT)):               
                            for j in range (0,deleted_index[i]):
                                ACT[i].pop(0)
                                
                        for i in range (0,len(ACT)):                
                            for j in range (0,len(ACT[i])):         
                                appendix = ACT[i][j]
                                ACT[i][j] = []
                                ACT[i][j].append(appendix)
                                ACT[i][j].append(list_actor[i])
                                for elem in tree.findall('.//Activity[@Id="%s"]' %appendix):
                                    activities = elem.get('Name')
                                    ACT[i][j].append(activities)
                                    
                    for i in range (0,len(ACT)):
                        for j in range (0,len(ACT[i])):                 
                            for z in range (0,1):
                                ACT[i][j].pop(0)

                    print(ACT)
                    print("") 
                    print("")
                    print("==HASIL ID BERDASARKAN KOORDINAT==") 
                    for i in range (0,len(ACT)):
                        for j in range (0,len(ACT[i])): 
                            if (len(ACT[i][j])==3):
                                print ("I as " + ACT[i][j][0] + ", i can " + ACT[i][j][1] + ", so that " + why[z][1] )
                            else :
                                print ("I as " + ACT[i][j][0] + ", i can " + ACT[i][j][1])

                    
                    
                print("FILE NAME")
                print(file_name)
                
                newBPMN = BPMN(
                    nama_bpmn=file_name,
                )

                newBPMN.save()
                bpmn_target_data = BPMN.objects.latest('id_bpmn')
                bpmn_target = bpmn_target_data.id_bpmn

                usNameSize = len(file_name)
                usName = file_name[:usNameSize - 5]
                print(usName + '_us')

                newUS = UserStories(
                    nama_us = usName,
                    id_bpmn = bpmn_target,
                )

                newUS.save()

                us_target_data = UserStories.objects.latest('id_us')
                us_target = us_target_data.id_us

                for i in range (0,len(ACT)):
                        for j in range (0,len(ACT[i])): 
                            if (len(ACT[i][j])==3):
                                print ("I as " + ACT[i][j][0] + ", i can " + ACT[i][j][1] + ", so that " + why[z][1] )
                                newTUS = TextUserStory(
                                    id_us = us_target,
                                    text_who = ACT[i][j][0],
                                    text_what = ACT[i][j][1],
                                    text_why = why[z][1],
                                )

                                newTUS.save()
                            else :
                                print ("I as " + ACT[i][j][0] + ", i can " + ACT[i][j][1])
                                newTUS = TextUserStory(
                                    id_us = us_target,
                                    text_who = ACT[i][j][0],
                                    text_what = ACT[i][j][1],
                                )

                                newTUS.save()


                context = {'list_actor':list_actor, 'list_activity':list_activity,'total_actor':total_actor,'ACT':ACT, 'TextAnnotation':TextAnnotation}
                return render(request,'userstoriesresult.html',context)
            else : 
                print("less than 2")
                print("FILE NAME")
                print(file_name)

                newBPMN = BPMN(
                    nama_bpmn=file_name,
                )

                newBPMN.save()

                bpmn_target_data = BPMN.objects.latest('id_bpmn')
                bpmn_target = bpmn_target_data.id_bpmn

                usNameSize = len(file_name)
                usName = file_name[:usNameSize - 5]
                print(usName + '_us')

                newUS = UserStories(
                    nama_us = usName,
                    id_bpmn = bpmn_target,
                )

                newUS.save()
                us_target_data = UserStories.objects.latest('id_us')
                us_target = us_target_data.id_us
                
                for i in range (0,len(list_activity)):
                    for j in range (0,len(list_actor)):
                        print ("I as " + list_actor[j] + ", i can " + list_activity[i])
                        newTUS = TextUserStory(
                            id_us = us_target,
                            text_who = list_actor[j],
                            text_what = list_activity[i],
                        )
                        newTUS.save()

                context = {'list_actor':list_actor, 'list_activity':list_activity,'total_actor':total_actor, 'TextAnnotation':TextAnnotation}
                return render(request,'userstoriesresult.html',context)

def documentation(request):
    return render(request, 'documentation.html')

def history(request):
    bpmn_target_data = UserStories.objects.all
    return render(request,"history.html",{'data':bpmn_target_data})
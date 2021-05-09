from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import xml.etree.ElementTree as ET


def masterpages(request):
     return render(request,'masterpage.html')
     
def uploadpage(request):
     return render(request,'uploadfile.html')

def parsing(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['xml']
        fs = FileSystemStorage()
        fs.save(uploaded_file.name, uploaded_file)
        file_name = uploaded_file.name
        with open('.\media\Review_Order1.xpdl', 'r') as infile, open('.\media\Fileclean.xpdl', "w") as outfile:
            data = infile.read()
            data = data.replace('xmlns="http://www.wfmc.org/2009/XPDL2.2"', '')
            outfile.write(data)

        context = {}
        with open('.\media\FileClean.xpdl', 'r') as filexml :
            tree = ET.parse(filexml)
            root = tree.getroot()
            list_actor = []
            list_activity = []
            for i in tree.findall('.//Lane'):
                name = i.get('Name')
                list_actor.append(name)
            for i in tree.findall('.//Activity'):
                activity = i.get('Name')
                list_activity.append(activity)
        # context['list_activity'] = list_activity
        context = {'list_actor':list_actor, 'list_activity':list_activity}
    return render(request,'userstoriesresult.html',context)

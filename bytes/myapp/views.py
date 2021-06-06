from django.shortcuts import render  
from django.http import HttpResponse  
from myapp.functions import handle_uploaded_file  
from myapp.forms import StudentForm  
import sys
import glob
from subprocess import run,PIPE
def index(request):  
    if request.method == 'POST':  
        student = StudentForm(request.POST, request.FILES)  
        if student.is_valid():  
            handle_uploaded_file(request.FILES['file'])  
            out=run([sys.executable,'../Riskcovry-Hackathon-Bytes-/scripts/testmodel.py'],shell=False,stdout=PIPE)
            #print(out)
            return render(request,"app/home.html",{'data':out.stdout.decode('utf-8')})
    else:  
        student = StudentForm()  
        return render(request,"app/index.html",{'form':student}) 


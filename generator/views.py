from django.shortcuts import render, redirect
from django.http import FileResponse
from django.conf import settings
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.views import View
from .models import File
from .forms import UploadFileForm, LoginForm
from . import handle, cimke
import os



class Login_page(View):
    def get(self, request):
         return render(request, 'generator/login.html')
    
    def post(self, request):
        form = LoginForm(request.POST)

        if form.is_valid():
            user = authenticate(
                username = form.cleaned_data['username'],
                password = form.cleaned_data['password']
            )

            if user is not None:
                login(request, user)
                return redirect('index')


        return render(request, 'generator/login.html')



class Logout_page(View):
    def get(self,request):
        logout(request)
        return redirect('login_page')



class Register_page(View):  
    def get(self,request):
        return render(request,'generator/registration.html')
    
    def post(self,request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if len(password) < 8 :
            return render(request,'generator/registration.html', {'error': 'Túl rövid jelszó'})
        
        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()

        user = authenticate(
                username = username,
                password = password
            )
        login(request, user)

        return redirect('index')



class Index(View):
    def get(self,request):
        if request.user.is_authenticated:

            files = File.objects.filter(owner=request.user)
            return render(request, "generator/index.html", {'files': files})
        
        return redirect('/login')


    def post(self,request):
        if request.user.is_authenticated:

            form = UploadFileForm(request.POST, request.FILES)
            files = File.objects.filter(owner=request.user)

            if (form.is_valid()) and str(request.FILES.get('file'))[-4:] == ".pdf":
                
                print(str(request.FILES.get('file')))
                file_path = os.path.join(settings.BASE_DIR, "generator\\Static\\inputFiles", str(request.FILES.get('file')))
                    
                # Fájl mentése
                handle.uploaded_file(request.FILES.get('file'), file_path)
                
                # Fájl átalakitása
                images = cimke.pdf_to_images(file_path)
                pages = cimke.merge(images, int(request.POST.get('cols')),int(request.POST.get('rows')))     
                file_name = cimke.export(pages, str(request.user.username))
                
                f = File(owner=request.user, filename=file_name)
                f.save()

                os.remove(file_path)

                return render(request,"generator/index.html", {"file" : file_name, 'files' : files})
            
            return render(request, "generator/index.html", {'files': files})
        
        return redirect('/login')



# link a fájl letöltéséhez
class Download(View):
    def get(self,request, fileName):
        username = fileName.split('_')[0]

        if str(request.user.username) == username:

            file = os.path.join(settings.BASE_DIR, f"output/{fileName}")

            fileOpened = open(file, 'rb')
    
            return FileResponse(fileOpened)
    
        return redirect('/')





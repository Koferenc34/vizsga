from django.shortcuts import render, redirect
from django.http import FileResponse
from django.conf import settings
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.views import View
from .models import File
from .forms import UploadCimkeFileForm, UploadVizjelFileForm, LoginForm
from .converters import cimke, vizjel
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

        # Leszedi a szóközöket a stringekről és megnézi hogy üresek-e vagy nem
        if(username.strip() and email.strip() and password.strip()):

            # Foglalt-e a felhasználónév
            if(User.objects.filter(username = username)):
                return render(request,'generator/registration.html', {'error': 'Már létezik ilyen felhasználó'})
            # Jelszó hossz
            if len(password) < 8 :
                return render(request,'generator/registration.html', {'error': 'Túl rövid jelszó. Min 8 karakter'})

            # Új felhasználó mentése
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()

            # Bejelentkeztetés
            user = authenticate(
                    username = username,
                    password = password
                )
            login(request, user)

        else: return render(request,'generator/registration.html', {'error': 'Hiányos adatok'})

        return redirect('index')



class Index(View):
    def get(self,request):
        if request.user.is_authenticated:

            files = File.objects.filter(owner=request.user)
            return render(request, "generator/index.html", {'files': files, 'spaceId': 1})
        
        return redirect('login_page')


    def post(self,request):
        if request.user.is_authenticated:

            formCimke = UploadCimkeFileForm(request.POST, request.FILES)
            formVizjel = UploadVizjelFileForm(request.POST, request.FILES)
            files = File.objects.filter(owner=request.user)

            # PDF Cimke Egyesítő
            # PDF végződés és konverter ellenőrzése
            if (formCimke.is_valid()) and str(request.FILES.get('file'))[-4:] == ".pdf" and str(request.POST.get("converter")) == "cimke":

                os.makedirs(os.path.join(settings.BASE_DIR, "generator\\Static\\tempFiles", str(request.user.username)), exist_ok=True)
                
                file_path = os.path.join(settings.BASE_DIR, "generator\\Static\\tempFiles", str(request.FILES.get('file')))
                file = request.FILES.get('file')
                cols = int(request.POST.get('cols'))
                rows = int(request.POST.get('rows'))
                username = str(request.user.username)
                os.makedirs(os.path.join(settings.BASE_DIR, "output", username), exist_ok=True)
                    
                # Fájl mentése
                with open(file_path, "wb+") as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)
                
                # Fájl átalakitása         
                file_name, alreadyExists = cimke.convert(file_path,cols,rows,username)
                
                if(not alreadyExists):
                    f = File(owner=request.user, filename=file_name)
                    f.save()

                os.remove(file_path)

                return render(request,"generator/index.html", {"file" : file_name, 'files' : files, 'spaceId' : 1})
            
            # Kép Vízjelezés
            # képformátum ('.png','.jpg','.jpeg','.webp','.svg') és konverter ellenőrzése
            fourChar = str(request.FILES.get('file'))[-4:]
            fiveChar = str(request.FILES.get('file'))[-5:]
            print(fourChar)
            print(fiveChar)
            if (formVizjel.is_valid() and str(request.POST.get("converter")) == "vizjel" and (
                (fourChar == '.png' or '.jpg' or '.svg') or
                (fiveChar == '.jpeg' or '.webp')
            )):
                os.makedirs(os.path.join(settings.BASE_DIR, "generator\\Static\\tempFiles", str(request.user.username)), exist_ok=True)

                file_path = os.path.join(settings.BASE_DIR, "generator\\Static\\tempFiles", str(request.FILES.get('file')))
                file = request.FILES.get('file')
                watermark = request.POST.get('watermark')
                username = str(request.user.username)
                os.makedirs(os.path.join(settings.BASE_DIR, "output", username), exist_ok=True)
                
                # Fájl mentése
                with open(file_path, "wb+") as destination:
                    for chunk in file.chunks():
                        destination.write(chunk)

                # Fájl átalakitása         
                file_name, alreadyExists = vizjel.convert(file_path,watermark,username,str(file))
                
                if(not alreadyExists):
                    f = File(owner=request.user, filename=file_name)
                    f.save()

                os.remove(file_path)

                return render(request,"generator/index.html", {"file" : file_name, 'files' : files, 'spaceId' : 2})

            return render(request, "generator/index.html", {'files': files, 'spaceId' : 1})
        
        return redirect('login_page')



# link a fájl letöltéséhez
class Download(View):
    def get(self,request,userName, fileName):
        if str(request.user.username) == userName:
            file = os.path.join(settings.BASE_DIR, f"output/{userName}/{fileName}")
            fileOpened = open(file, 'rb')
        
            return FileResponse(fileOpened)    
            
        return redirect('index')
    
# link a fájl törléséhez
class Delete(View):
    def get(self,request,userName,id,fileName):
        if str(request.user.username) == userName:
            f_path = os.path.join(settings.BASE_DIR, "output", userName, fileName)
            if os.path.exists(f_path):
                os.remove(f_path)

            f = File(id=id,owner=request.user, filename=fileName)
            f.delete()

            dir = os.path.join(settings.BASE_DIR, "output", userName)
            if not os.listdir(dir): os.rmdir(dir)

        return redirect('index')





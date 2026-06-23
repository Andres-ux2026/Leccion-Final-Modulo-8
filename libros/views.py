from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Libro
from .forms import LibroForms

# Create your views here.
def crear_libro(request):
    #si el usuario envio el formulario 
    if request.method == "POST":
        form = LibroForms(request.POST, request.FILES) #request.POST (SON TODOS LOS DATOS DEL FORMULARIO)

        if form.is_valid():
            form.save()
            messages.success(request, "producto guardado correctamente")
            return redirect("lista_libros")
    else:
        form = LibroForms()

    return render(request, "crear_libro.html",{"form":form})
#crud
# r (lectura de datos)   

def lista_libros(request):
    libros = Libro.objects.all()
    return render(request, "libros.html",{"libros":libros})



#crud 
# u (update)
def actualizar_libros(request, id):
    libros = Libro.objects.get(id=id)

    if request.method == "POST":
        form = LibroForms(request.POST,request.FILES, instance=libros)
        if form.is_valid():
            form.save()
            messages.success(request,"producto actualizado correctamente")
            return redirect("lista_libros")
    else:
        form = LibroForms(instance=libros)

    return render(request, "actualizar_libros.html",{"form":form})



def Eliminar_libros(request, id):
    libros = Libro.objects.get(id=id)
    libros.delete()
    messages.success(request,"mensaje desde la view!!!!!")
    return redirect("lista_libros")

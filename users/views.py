from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import UserCreationForm


def logout_view(request):
    """Faz o Logout"""
    logout(request)
    return HttpResponseRedirect(reverse('home'))

def register(request):
    """Faz o cadastro de novo ususario"""
    #verfifiva se o User já está autenticado e  e redireciona caso sim
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))
    
    if request.method != 'POST':
        #exibe o form em branco
        form = UserCreationForm()
    else:
        #processa o form preeschido
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            #Faz o login do User e redireciona para index
            authenticat_user = authenticate(username=new_user.username, password = request.POST['password1'])
            login(request, authenticat_user)
            return HttpResponseRedirect(reverse('home'))
    context = {'form': form}
    return render(request, 'users/register.html',context)


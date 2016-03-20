from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate
from django.shortcuts import redirect, render
from django.template import loader
from .forms import UserForm
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User

@login_required
def index(request):
    template = loader.get_template('index.html')
    context = {
    }
    return HttpResponse(template.render(context, request))

def logout_view(request):
    logout(request)
    return redirect('/code_cloud/accounts/login')


def adduser(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password'],
                                    )
            login(request, new_user)
            # redirect, or however you want to get to the main view
            return HttpResponseRedirect('/code_cloud')
    else:
        form = UserForm()

    return render(request, 'registration/adduser.html', {'form': form})

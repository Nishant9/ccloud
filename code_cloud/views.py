from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect



@login_required
def index(request):
        return HttpResponse("Hello, world. You're at the polls index.")



def logout_view(request):
    logout(request)
    return redirect('/code_cloud/accounts/login')

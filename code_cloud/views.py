from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate
from django.shortcuts import redirect, render
from django.template import loader, Context, Template
from .forms import UserForm
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.views.generic.base import TemplateView
from .models import Problem
from django.template import TemplateDoesNotExist
from django.http import Http404
from django.views.generic.edit import UpdateView, DeleteView
from .forms import ProblemForm

@login_required
def index(request):
    template = loader.get_template('index.html')
    context = {
    }
    return HttpResponse(template.render(context, request))

@login_required
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

@login_required
def allproblemsview(request):

    template = loader.get_template('index_all_problems.html')
    context = Context({
        'problem_list' : Problem.objects.filter(user = request.user)
    })
    return HttpResponse(template.render(context))

@login_required
def query(request):
    oj = request.GET.get('oj',None)
    tag = request.GET.get('tag',None)
    problem_list = Problem.objects.filter(user = request.user)
    if oj != None :
        problem_list = problem_list.filter(online_judge = oj)
    if tag != None :
        problem_list = Tags.objects.filter(problem__in = problem_list).values_list('problem', flat=True)

    template = loader.get_template('index_query.html')
    context = Context({
        'problem_list' : problem_list,
    })
    return HttpResponse(template.render(context))

@login_required
def view_problem(request):

    template = loader.get_template('index_view_problem.html')
    context = Context({
        'problem' : Problem.objects.filter(id = request.GET.get('pid'))[0]
    })
    return HttpResponse(template.render(context))


class StaticView(TemplateView):
    def get(self, request, page, *args, **kwargs):
        self.template_name = page
        response = super(StaticView, self).get(request, *args, **kwargs)
        try:
            return response.render()
        except TemplateDoesNotExist:
            raise Http404()



class ProblemUpdate(UpdateView):
    model = Problem
    success_url = '/code_cloud'
    fields = ['name', 'online_judge', 'difficulty', 'access']
    template_name='update_problem.html'



class ProblemDelete(DeleteView):
    model = Problem
    success_url = '/code_cloud'
    template_name='problem_confirm_delete.html'

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate
from django.shortcuts import redirect, render
from django.template import loader, Context, Template
from .forms import UserForm, TagForm, ShareForm
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.views.generic.base import TemplateView
from .models import Problem, Tags, Share
from django.template import TemplateDoesNotExist
from django.http import Http404
from django.views.generic.edit import UpdateView, DeleteView
from .forms import ProblemForm, TagForm
from uuid import uuid4
from pygments.lexers import get_lexer_for_filename
from pygments.formatters import HtmlFormatter
from pygments import highlight
from django.views.decorators.csrf import csrf_exempt
import datetime
from itertools import groupby
from django.views.static import serve
import os


@login_required
def index(request):
    template = loader.get_template('index.html')
    problem_list = Problem.objects.filter(user = request.user)
    date = [b.date_created.date() for b in problem_list]
    lst = [[str(key), len(list(group))] for key, group in groupby(date)]
    context = {
        'graph_data' : lst
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
    problem_list = Problem.objects.filter(user = request.user)
    zip_list = [([str(t) for t in Tags.objects.filter(problem = p)],p) for p in problem_list]
    context = Context({
        'problem_list' : zip_list
    })
    return HttpResponse(template.render(context))



@login_required
def sharedproblemsview(request):

    template = loader.get_template('index_shared_problems.html')
    problem_list = Share.objects.filter(share_user = request.user).values_list('problem', flat=True)
    problem_list = [Problem.objects.get(id = p) for p in problem_list]
    print(problem_list)
    zip_list = [([str(t) for t in Tags.objects.filter(problem = p)],p) for p in problem_list]
    context = Context({
        'problem_list' : zip_list
    })
    return HttpResponse(template.render(context))



@login_required
def tagsview(request):

    template = loader.get_template('index_tags.html')
    problem_list = Problem.objects.filter(user = request.user)
    zip_list = [([str(t) for t in Tags.objects.filter(problem = p)],p) for p in problem_list]
    tag_list = Tags.objects.filter(problem__in = problem_list).values_list('tag', flat=True)
    print(tag_list)
    context = Context({
        'problem_list' : zip_list
    })
    return HttpResponse(template.render(context))


@login_required
def query(request):
    oj = request.GET.get('oj',None)
    tag = request.GET.get('tag',None)
    search = request.GET.get('search',None)
    problem_list = Problem.objects.filter(user = request.user)
    if oj != None :
        problem_list = problem_list.filter(online_judge = oj)
    if tag != None :
        problem_list = Tags.objects.filter(tag = tag).filter(problem__in = problem_list).values_list('problem_id', flat=True)
        problem_list = [Problem.objects.get(id = p) for p in problem_list]
    if search != None :
        shared_list =  Share.objects.filter(share_user = request.user).values_list('problem', flat=True)
        # shared_list = [Problem.objects.get(id = p) for p in shared_list]
        shared_list = Problem.objects.filter(id__in = shared_list)
        problem_list = shared_list | problem_list
        problem_list = problem_list.filter(name__icontains = search)
    zip_list = [([str(t) for t in Tags.objects.filter(problem = p)],p) for p in problem_list]
    template = loader.get_template('index_query.html')
    context = Context({
        'problem_list' : zip_list,
    })
    return HttpResponse(template.render(context))

@login_required
def view_problem(request):

    problem = Problem.objects.get(id = request.GET.get('pid'))
    if problem.user != request.user :
        problem_list = Share.objects.filter(share_user = request.user).values_list('problem', flat=True)
        if problem.id in problem_list :
            pass
        else :
            raise Http404()
    f = open(str(problem.docfile), 'r')
    code = f.read()
    f.close()
    formatter = HtmlFormatter()
    formatter.noclasses = True
    lexer = get_lexer_for_filename(str(problem.docfile))
    context = Context({
        'problem' : problem,
        'highlighted_code' : highlight(code, lexer, formatter)
    })
    return render(request, 'index_view_problem.html', context)




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
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
#        self.check_permission(request.user, self.object)
        if request.user != self.object.user :
            raise Http404()
        return super(ProblemUpdate, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
#        self.check_permission(request.user, self.object)
        if request.user != self.object.user :
            raise Http404()
        return super(ProblemUpdate, self).post(request, *args, **kwargs)




class ProblemDelete(DeleteView):
    model = Problem
    success_url = '/code_cloud'
    template_name='problem_confirm_delete.html'
    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(ProblemDelete, self).get_object()
        if not obj.user == self.request.user:
            raise Http404
        return obj


@csrf_exempt
def edit_tag(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/code_cloud')
    if request.method == 'POST':
        form = TagForm(request.POST)
        form.save()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])




def share_problem(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/code_cloud')
    if request.method == 'POST':
        pid = request.POST.get('problem', None)
        user_name = request.POST.get('share_user', None)
        sh = Share(problem = Problem.objects.get(id = pid), share_user = User.objects.get(username = user_name))
        print(sh)
        sh.save()
        return HttpResponseRedirect(request.META['HTTP_REFERER'])

@csrf_exempt
def download_problem(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/code_cloud')
    if request.method == 'POST':
        pid = request.POST.get('problem', None)
        problem = Problem.objects.get(id = pid)
        filepath = str(problem.docfile)
        return serve(request, os.path.basename(filepath), os.path.dirname(filepath))

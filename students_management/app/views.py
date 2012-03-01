# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.db.models import Max

from app.models import *
from app.forms import *


def main_page(request):
    """ Main page: list of groups """
    groups = Group.objects.order_by('id')
    for group in groups:
        group.studentsNum = Student.objects.select_related('groupId').filter(groupId=group.id).count()

    variables = RequestContext(request, {'groups': groups})

    return render_to_response('main_page.html', variables)


def group_page(request, groupId):
    try:
        group = Group.objects.get(id=groupId)
    except:
        raise Http404('Requested group is not found')

    students = Student.objects.filter(groupId=group.id)
    paginator = Paginator(students, 5)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        students = paginator.page(page)
    except (EmptyPage, InvalidPage):
        students = paginator.page(paginator.num_pages)

    variables = RequestContext(request, {'students': students, 'group': group, "pages": paginator.page_range})

    return render_to_response('group_page.html', variables)


def _group_save(request, form):
    group, created = Group.objects.get_or_create(name)

def group_form_page(request):
    if request.method == 'POST':
        group, created = Group.objects.get_or_create(id=request.POST.get('id'))
        form = GroupForm(request.POST, instance=group)
        if not created:
            form.fields['seniorId'].queryset = Student.objects.filter(groupId=group.id)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    elif request.GET.has_key('id'):
        groupId = int(request.GET.get('id'))
        group = Group.objects.get(id=groupId)
        form = GroupForm(instance=group)
        form.fields['seniorId'].queryset = Student.objects.filter(groupId=groupId)
    else:
        form = GroupForm()
        newId = int(Group.objects.all().aggregate(Max('id'))['id__max'])+1
        form.fields['id'].initial = newId

    variables = RequestContext(request, {'form': form})
    
    return render_to_response('group_form.html', variables, context_instance=RequestContext(request))


def student_page(request, studentId):
    return HttpResponse("Here will be the list the student's portfolio") 
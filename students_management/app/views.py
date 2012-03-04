# Create your views here.
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.db.models import Max

from re import search

from app.models import *
from app.forms import *
from settings import MEDIA_ROOT


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


def group_form_page(request):
    if request.method == 'POST':
        try:
            group = Group.objects.get(id=request.POST.get('id'))
        except Group.DoesNotExist:
            seniorId = request.POST.get(u'seniorId') or None
            group = Group(id=request.POST.get(u'id'), name=request.POST.get(u'name'), seniorId=seniorId)
        form = GroupForm(request.POST, instance=group)
        form.fields['seniorId'].queryset = Student.objects.filter(groupId=group.id)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/group/{0}'.format(group.id))
    elif request.GET.has_key('id'):
        groupId = int(request.GET.get('id'))
        group = Group.objects.get(id=groupId)
        form = GroupForm(instance=group)
        form.fields['seniorId'].queryset = Student.objects.filter(groupId=groupId)
    else:
        form = GroupForm()
        newId = int(Group.objects.all().aggregate(Max('id'))['id__max'])+1
        form.fields['id'].initial = newId
        form.fields['seniorId'].queryset = Student.objects.filter(groupId=newId)

    variables = RequestContext(request, {'form': form})
    
    return render_to_response('group_form.html', variables, context_instance=RequestContext(request))


def group_delete_page(request):
    groupId = request.GET.get('id')
    group = Group.objects.get(id=groupId)
    try:
        group.delete()
    except:
        pass

    return main_page(request)



def student_page(request, studentId):
    try:
        student = Student.objects.get(id=studentId)
    except:
        raise Http404('Requested student is not found')

    variables = RequestContext(request, {'student': student})

    return render_to_response('student_page.html', variables)

def student_form_page(request):
    if request.method == 'POST':
        if request.POST.get('id') not in ['', None]:
            student = Student.objects.get(id=request.POST.get('id'))
        else:
            student = None
        #if 'file' in request.FILES:
            #photo = request.FILES['file']
            #photoName = photo['filename']
            #with file("{0}{1}".format(MEDIA_ROOT, photoName), 'wb') as f:
                #f.write(photo['content'])
        form = StudentForm(request.POST, request.FILES, instance=student)
        form.fields['groupId'].queryset = Group.objects.all()
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/group/{0}'.format(form.instance.groupId.id))
        variables = {'form': form, 'add': True}
    elif request.GET.has_key('id'):
        studentId = int(request.GET.get('id'))
        student = Student.objects.get(id=studentId)
        form = StudentForm(instance=student)
        form.fields['groupId'].queryset = Group.objects.all()
        variables = {'form': form, 'edit': True}
    else:
        form = StudentForm()
        form.fields['groupId'].queryset = Group.objects.all()
        try:
            groupId = search('/group/(\d)+', request.META['HTTP_REFERER']).group(1)
        except:
            groupId = None
        form.fields['groupId'].initial = groupId
        form.fields['groupId'].widget.attrs['readonly'] = True
        variables = {'form': form, 'add': True}

    variables = RequestContext(request, variables)

    return render_to_response('student_form.html', variables, context_instance=RequestContext(request))


def student_delete_page(request):
    studentId = request.GET.get('id')
    student = Student.objects.get(id=studentId)
    groupId = student.groupId.id
    try:
        student.delete()
    except:
        pass

    return group_page(request, groupId)


from django.forms import ModelForm
from django.forms.models import BaseFormSet
from django.forms import HiddenInput
from django.forms import ModelChoiceField, CharField, ChoiceField, IntegerField
from app.models import *


class MyModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return u"{0} {1} {2}".format(obj.lastName, obj.firstName, obj.middleName)


class GroupForm(ModelForm):
    seniorId = MyModelChoiceField(None, "(nobody)", label='Senior')
    #id = IntegerField()

    #def __init__(self, *args, **kwags):
        #groupId = kwags.pop('groupId', None)
        #super(forms.ModelForm, self).__init__(*args, **kwags)

        #if groupId:
            #self.fields['id'] = IntegerField(groupId)
            #self.fields['seniorId'].queryset = Student.objects.filter(groupId=groupId)
            #self.fields['id'].queryset = Group.objects.get(id=groupId)

    class Meta:
        model = Group
        #fields = ('id', 'name', 'seniorId')
        widgets = {
            'id': HiddenInput()
        }


#class GroupFormSet(BaseFormSet):
#    def __init__(self, *args, **kwags):
#        super(BaseFormSet, self).__init__(*args, **kwags)
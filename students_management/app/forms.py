from django.forms import ModelForm
from django.forms.models import BaseFormSet
from django.forms import HiddenInput
from django.forms import ModelChoiceField, CharField, ChoiceField, IntegerField, ValidationError
from app.models import *


class StudentChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return u"{0} {1} {2}".format(obj.lastName, obj.firstName, obj.middleName)


class GroupForm(ModelForm):
    seniorId = StudentChoiceField(None, "(nobody)", label='Senior', required=False)

    class Meta:
        model = Group
        widgets = {
            'id': HiddenInput()
        }


class StudentForm(ModelForm):
    class Meta:
        model = Student
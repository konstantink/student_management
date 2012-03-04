from django.forms import ModelForm
from django.forms.models import BaseFormSet
from django.forms import HiddenInput, TextInput
from django.forms import ModelChoiceField, CharField, ChoiceField, IntegerField, ValidationError
from app.models import *


class StudentChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return u"{0} {1} {2}".format(obj.last_name, obj.first_name, obj.middle_name)


class GroupForm(ModelForm):
    seniorId = StudentChoiceField(None, "(nobody)", label='Senior', required=False)

    def clean_name(self):
        from re import match, UNICODE
        name = self.cleaned_data['name']
        if match('^[\w\-]+$', name, UNICODE):
            return name
        raise ValidationError("Incorrect name '{0}' for group. Name can contain only alphanumeric, underscore and dash".format(name))

    class Meta:
        model = Group
        widgets = {
            'id': HiddenInput()
        }


class GroupChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return u"{0}".format(obj.name)


class StudentForm(ModelForm):
    id = IntegerField(widget=HiddenInput, required=False)
    groupId = GroupChoiceField(None, "(none)", label='Group')

    class Meta:
        model = Student

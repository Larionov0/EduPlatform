from .models import *
from django import forms


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'description']

    def save(self, company_id, commit=True):
        print('saving')
        self.instance.company_id = company_id
        super().save(commit)

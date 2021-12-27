from django.urls import path
from .views import *


app_name = 'main'

urlpatterns = [
    path('my_companies', my_companies, name='my_companies'),
    path('company_admin/<int:comp_user_id>', lambda: None),
    path('company_teacher/<int:comp_user_id>', lambda: None),
    path('company_student/<int:comp_user_id>', lambda: None),
    path('enter_company/<int:id>', enter_company, name='enter_company'),
    path('enter_company/<int:id>', enter_company, name='enter_company'),
    path('company/<int:id>/subjects', subjects, name='subjects'),

    path('company/<int:id>/edit_subject/<int:subject_id>', edit_subject, name='edit_subject'),
    path('company/<int:id>/create_subject', create_subject, name='create_subject'),
    path('company/<int:id>/delete_subject/<int:subject_id>', delete_subject, name='delete_subject'),

    path('company/<int:id>/groups', groups, name='groups')
]

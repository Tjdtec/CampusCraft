from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login, name='login'),

    path('get_student_by_id/<str:id>'
         ,views.student_load_infos, name='student_load_infos'),

    path('get_counselor_by_id/<str:id>'
         ,views.counselor_load_infos, name='counselor_load_infos'),

    path('get_employer_by_id/<str:id>'
         ,views.employer_load_infos, name='employer_load_infos'),

    path('get_student_affair_by_id/<str:id>'
         ,views.student_affair_load_infos, name='student_affair_load_infos'),

    path('get_work_study_admin_by_id/<str:id>'
         ,views.work_study_admin_load_infos, name='work_study_admin_load_infos'),
]

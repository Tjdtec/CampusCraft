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

    path('student_load_related_jobs/<str:student_id>'
         ,views.student_load_related_jobs, name='student_load_related_jobs'),

    path('student_load_unrelated_jobs/<str:student_id>'
         ,views.student_load_unrelated_jobs, name='student_load_unrelated_jobs'),

    path('student_apply_for_job/<str:job_id>/<str:student_id>'
         ,views.student_apply_for_job, name='student_apply_for_job'),
]

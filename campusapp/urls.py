from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login, name='login'),

    path('get_student_by_id/<str:id>'
         , views.student_load_infos, name='student_load_infos'),

    path('get_counselor_by_id/<str:id>'
         , views.counselor_load_infos, name='counselor_load_infos'),

    path('get_employer_by_id/<str:id>'
         , views.employer_load_infos, name='employer_load_infos'),

    path('get_student_affair_by_id/<str:id>'
         , views.student_affair_load_infos, name='student_affair_load_infos'),

    path('get_work_study_admin_by_id/<str:id>'
         , views.work_study_admin_load_infos, name='work_study_admin_load_infos'),

    path('student_load_related_jobs/<str:student_id>'
         , views.student_load_related_jobs, name='student_load_related_jobs'),

    path('student_load_unrelated_jobs/<str:student_id>'
         , views.student_load_unrelated_jobs, name='student_load_unrelated_jobs'),

    path('student_apply_for_job/<str:job_id>/<str:student_id>'
         , views.student_apply_for_job, name='student_apply_for_job'),

    path('stu_admin_create_student/<str:stu_admin_id>'
         , views.stu_admin_create_student, name='stu_admin_create_student'),

    path('stu_admin_modify_student/<str:stu_admin_id>'
         , views.stu_admin_modify_student, name='stu_admin_modify_student'),

    path('make_new_job/<str:employer_id>', views.make_new_job, name='make_new_job'),

    path('job_manager_approve_job/<str:job_manager_id>/<str:job_number>'
         , views.job_manager_approve_job, name='job_manager_approve_job'),

    path('submit_job_feedback/<str:employer_id>/<str:job_number>/<str:job_feedback>',
         views.submit_job_feedback, name='submit_job_feedback'),

    path('stu_admin_get_all_students/'
         , views.stu_admin_get_all_students, name='stu_admin_get_all_students'),

    path('assists_get_brief/<str:major_name>'
         , views.assists_get_brief, name='assists_get_brief'),

    path('assists_admin_get_brief/'
         , views.assists_admin_get_brief, name='assists_admin_get_brief')
]

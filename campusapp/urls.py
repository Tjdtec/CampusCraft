from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('get_student_by_id/<str:student_id>',views.student_load_infos, name='student_load_infos')
]

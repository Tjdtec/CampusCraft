from django.http import JsonResponse

from django.http import HttpResponse
from django.conf import settings
import os
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Login
from django.http import JsonResponse

def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        try:
            login_record = Login.objects.get(user_name=username, user_password=password)
            response_data = {
                'user_identifier': login_record.get_user_type_display()
            }
            return JsonResponse(response_data)
        except Login.DoesNotExist:
            return JsonResponse({'error': 'Invalid username or password'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405) 



"""
APIs for students
"""

def student_load_related_jobs(request, student_id):

    # find the student obj according to this student_id
    student = Student.objects.get(student_id=student_id)

    # B: find all jobs objs that are related to this student

    return student.view_applied_jobs()

def student_load_unrelated_jobs(request, student_id):

    # find the student obj according to this student_id
    student = Student.objects.get(student_id=student_id)

    # A: find all jobs objs
    A = Job.objects.all()

    # B: find all jobs objs that are related to this student
    B = student.view_applied_jobs()

    # return A-B
    return A.difference(B)

def student_update_infos(request, student_id, student_json):

    # find student objs according to student_id

    # call update self_infos
    pass

def student_apply_for_job(request, job_id, student_id):

    # find student obj according to student_id

    # find job obj according to job_id

    # call job's insert_student function
    pass 
    
"""
APIs for 'Counselor' or 'Assists' or 'fu_dao_yuan'
"""

def assists_get_brief(request, major_name):

    # gathering informations of a given major(name).

    # return a string like 

    """
    {
    "total_populations": "本专业总共有12人",       
    "applied_populations": "共有8人参加勤工俭学工作",        
    "max_wage": "收入最高的1203$每月",
    "min_wage": "收入最低45$每月。"
    "no_jobs_populations": 12,
    "one_or_two_jobs_populations": 10,
    "three_or_more_jobs_populations": 34
    }
    """

    pass


def assists_get_students(request, major_name):
    
    # filter all students of a given major

    # return student list

    pass


"""
APIs for StuAdmins or StudentAffair
"""

# def stu_admin_update_student_info():
#  Okay.... just reuse the Student's student_update_infos() function



def stu_admin_create_student(request, student_json):

    # just like it's name says....

    pass



def stu_admin_get_all_students(request):

    # return all students (we don't care majors here)

    pass

def assists_admin_get_brief(request):

    # gathering informations of all students.

    # return a string like 

    """
    {
    "total_populations": "本专业总共有12人",       
    "applied_populations": "共有8人参加勤工俭学工作",        
    "max_wage": "收入最高的1203$每月",
    "min_wage": "收入最低45$每月。"
    "no_jobs_populations": 12,
    "one_or_two_jobs_populations": 10,
    "three_or_more_jobs_populations": 34
    }
    """

    pass



"""
APIs for JobManagers or WorkStudyAdmin
"""

def job_manager_approve_job(request, job_manager_id, job_number):

    # find job manager's obj according to job_manager_id

    # call job manager's approve_job(cls, job_number)

    pass


def job_manager_load_jobs(request,job_manager_id):

    # find all jobs

    pass



"""
APIs for job card
"""


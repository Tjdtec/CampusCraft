from django.http import JsonResponse

from django.http import HttpResponse
from django.conf import settings
import os
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Login, StudentAffair, WorkStudyAdmin, Employer, Student, Counselor, Job
from django.http import JsonResponse

@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        try:
            student = Student.login(username, password)
            counselor = Counselor.login(username, password)
            employer = Employer.login(username, password)
            student_affair = StudentAffair.login(username, password)
            work_study_admin = WorkStudyAdmin.login(username, password)
            if student:
                student_info = student.view_student_info()
                student_info["role"] = "student"
                return JsonResponse(student_info)
            if counselor:
                counselor_info = counselor.view_counselor_info()
                counselor_info["role"] = "counselor"
                return JsonResponse(counselor_info)
            if student_affair:
                student_affair_info = student_affair.view_student_affair_info()
                student_affair_info["role"] = "student_affair"
                return JsonResponse(student_affair_info)
            if employer:
                employer_info = employer.view_employer_info()
                employer_info["role"] = "employer"
                return JsonResponse(employer_info)
            if work_study_admin:
                work_study_admin_info = work_study_admin.view_work_study_admin_info()
                work_study_admin_info["role"] = "work_study_admin"
                return JsonResponse(work_study_admin_info)
            
            return JsonResponse({'error': 'no match'}, status=400)
            
        except Login.DoesNotExist:
            return JsonResponse({'error': 'Invalid shits'}, status=400)
    else:
        return JsonResponse({'error': 'WTF?'}, status=405) 

"""
General APIs
"""

# Pass-in IDs into these motherfuckers 
# next, according to that, return the information of that shit

def student_load_infos(request, id):

    student = Student.objects.get(student_id=id)
    return JsonResponse(student.view_student_info())

def counselor_load_infos(request, id):

    counselor = Counselor.objects.get(employee_id=id)
    return JsonResponse(counselor.view_counselor_info())

def employer_load_infos(request, id):

    employer = Employer.objects.get(employer_id=id)
    return JsonResponse(employer.view_employer_info())

def student_affair_load_infos(request, id):

    student_affair = StudentAffair.objects.get(stu_admin_id=id)
    return JsonResponse(student_affair.view_student_affair_info())

def work_study_admin_load_infos(request, id):

    work_study_admin = WorkStudyAdmin.objects.get(work_admin_id=id)
    return JsonResponse(work_study_admin.view_work_study_admin_info())

def job_flow(stu = None):

    if stu is None:
        job_objects = Job.objects.all()
    else:
        job_objects = stu.view_applied_jobs()

    job_list = []
    for job in job_objects:
        job_dict = {
            'job_id': job.id,
            'job_number': job.job_number,
            'is_approved': job.is_approved,
            'job_title': job.job_title,
            'job_content': job.job_content,
            'salary': job.salary,
            'feedback': job.feedback
            # Add other fields as needed
        }
        job_list.append(job_dict)
    return job_list


"""
APIs for students
"""
def student_load_related_jobs(request, student_id):
    if request.method == 'GET':
        # find the student obj according to this student_id
        try:
            # B: find all jobs objs that are related to this student
            stu = Student.objects.get(student_id=student_id)
            return JsonResponse(job_flow(stu=stu), safe=False)
        except Student.DoesNotExist:
            return JsonResponse({'error': 'Invalid student_id'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405) 


def student_load_unrelated_jobs(request, student_id):
    if request.method == 'GET':
        try:
            # find the student obj according to this student_id
            stu = Student.objects.get(student_id=student_id)

            # A: find all jobs objs
            job_all = job_flow()
            # B: find all jobs objs that are related to this student
            job_rel = job_flow(stu)
            # return A-B
            job_unrel = [item for item in job_all if item not in job_rel]
            return JsonResponse(job_unrel, safe=False)
        except Student.DoesNotExist:
            return JsonResponse({'error': 'Invalid student_id'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405) 


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

#VIP
def assists_get_students(request, major_name):
    
    # filter all students of a given major

    # return student list

    pass


"""
APIs for StuAdmins or StudentAffair
"""

# def stu_admin_update_student_info():
#  Okay.... just reuse the Student's student_update_infos() function


#VIP
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

#VIP
def job_manager_load_jobs(request,job_manager_id):

    # find all jobs

    pass



"""
APIs for company or Employer
"""

#VIP
def make_new_job(request,job_json):

    pass





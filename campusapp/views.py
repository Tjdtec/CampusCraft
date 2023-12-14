from django.http import JsonResponse

from django.http import HttpResponse
from django.conf import settings
import os
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Login, StudentAffair, WorkStudyAdmin, Employer, Student, Counselor, Job
from django.http import JsonResponse
from django.db.models import Count, Max, Min


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


def job_flow(stu=None):
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


def stu_flow():
    stu_objects = Student.objects.all()

    stu_list = []
    for stu in stu_objects:
        stu_dict = {
            'student_id': stu.student_id,
            'name': stu.name,
            'contact_number': stu.contact_number,
            'introduction': stu.introduction,
            'class_name': stu.class_name,
            'major': stu.major
            # Add other fields as needed
        }
        stu_list.append(stu_dict)
    return stu_list


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
    stu = Student.objects.get(student_id=student_id)
    # find job obj according to job_id
    job = Job.objects.get(job_number=job_id)
    # call job's insert_student function
    stu.apply_for_job(job)
    return JsonResponse({'success': 'happy~'})


"""
APIs for 'Counselor' or 'Assists' or 'fu_dao_yuan'
"""


def assists_get_brief(request, major_name):
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
    if request.method == 'GET':
        try:
            total_populations = Student.objects.filter(major=major_name).count()
            applied_populations = Student.objects.filter(major=major_name, jobs__isnull=False).distinct().count()
            max_wage_obj = Job.objects.filter(student_job_fk__major=major_name).aggregate(Max('salary'))
            min_wage_obj = Job.objects.filter(student_job_fk__major=major_name).aggregate(Min('salary'))
            no_jobs_populations = Student.objects.filter(major=major_name, jobs__isnull=True).count()
            one_or_two_jobs_populations = Student.objects.filter(major=major_name, jobs__isnull=False).annotate(
                num_jobs=Count('jobs')).filter(num_jobs__lte=2).count()
            three_or_more_jobs_populations = Student.objects.filter(major=major_name, jobs__isnull=False).annotate(
                num_jobs=Count('jobs')).filter(num_jobs__gte=3).count()

            # Build a dictionary
            data = {
                "total_populations": f"本专业总共有{total_populations}人",
                "applied_populations": f"共有{applied_populations}人参加勤工俭学工作",
                "max_wage": f"收入最高的{max_wage_obj['salary__max']}$每月",
                "min_wage": f"收入最低{min_wage_obj['salary__min']}$每月",
                "no_jobs_populations": no_jobs_populations,
                "one_or_two_jobs_populations": one_or_two_jobs_populations,
                "three_or_more_jobs_populations": three_or_more_jobs_populations
            }

            # return Json
            return JsonResponse(data, safe=False)

        except Exception as e:
            # Print the exception message for debugging
            print(f"Exception: {str(e)}")
            # Reraise the exception to get more details in the console or Django error page
            raise e
    else:
        return JsonResponse({'error': 'WTF?'}, status=405)


# VIP


def assists_get_students(request, major_name):
    """
    Return a list of all students belonging to the given major.
    """
    if request.method == 'GET':
        try:
            # Query all students with the specified major
            students = Student.objects.filter(major=major_name)

            # Extract relevant information for each student
            student_list = [
                {
                    'name': student.name,
                    'contact_number': student.contact_number,
                    'introduction': student.introduction,
                    'major': student.major,
                    'class_name': student.class_name,
                    'student_id': student.student_id,
                }
                for student in students
            ]

            # return Json
            return JsonResponse(student_list, safe=False)
        except Exception as e:
            # Print the exception message for debugging
            print(f"Exception: {str(e)}")
            # Reraise the exception to get more details in the console or Django error page
            raise e
    else:
        return JsonResponse({'error': 'WTF?'}, status=405)


"""
APIs for StuAdmins or StudentAffair
"""


# def stu_admin_update_student_info():
#  Okay.... just reuse the Student's student_update_infos() function


# VIP
def stu_admin_create_student(request, stu_admin_id):
    # just like its name says....
    if request.method == 'POST':
        try:
            student_json = json.loads(request.body)
            stu_name = student_json.get('name')
            stu_contact_number = student_json.get('contact_number')
            stu_major = student_json.get('major')
            stu_class_name = student_json.get('class_name')
            stu_id = student_json.get('student_id')
            stu_admin = StudentAffair.objects.get(stu_admin_id=stu_admin_id)
            stu_admin.add_student(name=stu_name, contact_number=stu_contact_number, major=stu_major,
                                  class_name=stu_class_name, student_id=stu_id)
            response_data = {'message': f'{stu_admin.stu_admin_name}: Student created successfully'}
            return JsonResponse(response_data, status=200)
        except json.JSONDecodeError:
            response_data = {'error': 'Invalid JSON data'}
            return JsonResponse(response_data, status=400)
    else:
        response_data = {'error': 'Invalid JSON data'}
        return JsonResponse(response_data, status=404)


def stu_admin_modify_student(request, stu_admin_id):
    if request.method == 'POST':
        try:
            modify_stu_json = json.loads(request.body)
            stu_name = modify_stu_json.get('name')
            stu_contact_number = modify_stu_json.get('contact_number')
            stu_major = modify_stu_json.get('major')
            stu_class_name = modify_stu_json.get('class_name')
            stu_id = modify_stu_json.get('student_id')
            # Get the stu_admin object by the stu_admin_id
            stu_admin = StudentAffair.objects.get(stu_admin_id=stu_admin_id)
            stu_admin.modify_student_info(name=stu_name, contact_number=stu_contact_number, major=stu_major,
                                          class_name=stu_class_name, student_id=stu_id)
            response_data = {'message': f'{stu_admin.stu_admin_name}: Student created successfully'}

            return JsonResponse(response_data, status=200)
        except json.JSONDecodeError:
            response_data = {'error': 'Invalid JSON data'}
            return JsonResponse(response_data, status=400)
        finally:
            response_data = {'error': 'Invalid  stu_admin_id'}
            return JsonResponse(response_data, status=401)

    else:
        response_data = {'error': 'Invalid JSON data'}
        return JsonResponse(response_data, status=405)


def stu_admin_get_all_students(request):
    # return all students (we don't care majors here)
    if request.method == 'GET':
        # find all the student obj 
        try:
            return JsonResponse(stu_flow(), safe=False)
        except Student.DoesNotExist:
            return JsonResponse({'error': 'Invalid student_id'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)


def assists_admin_get_brief(request):
    """
    {
    "total_populations": "学生总共有12人",       
    "applied_populations": "共有8人参加勤工俭学工作",        
    "max_wage": "收入最高的1203$每月",
    "min_wage": "收入最低45$每月。"
    "no_jobs_populations": 12,
    "one_or_two_jobs_populations": 10,
    "three_or_more_jobs_populations": 34
    }
    """
    if request.method == 'GET':
        try:
            total_populations = Student.objects.count()
            applied_populations = Student.objects.filter(jobs__isnull=False).distinct().count()
            max_wage_obj = Job.objects.aggregate(Max('salary'))
            min_wage_obj = Job.objects.aggregate(Min('salary'))
            no_jobs_populations = Student.objects.filter(jobs__isnull=True).count()
            one_or_two_jobs_populations = Student.objects.annotate(
                num_jobs=Count('jobs')).filter(num_jobs__lte=2).count()
            three_or_more_jobs_populations = Student.objects.annotate(
                num_jobs=Count('jobs')).filter(num_jobs__gte=3).count()

            # Build a dictionary
            data = {
                "total_populations": f"学生总共有{total_populations}人",
                "applied_populations": f"共有{applied_populations}人参加勤工俭学工作",
                "max_wage": f"收入最高的{max_wage_obj['salary__max']}$每月",
                "min_wage": f"收入最低{min_wage_obj['salary__min']}$每月",
                "no_jobs_populations": no_jobs_populations,
                "one_or_two_jobs_populations": one_or_two_jobs_populations,
                "three_or_more_jobs_populations": three_or_more_jobs_populations
            }

            # return Json
            return JsonResponse(data, safe=False)

        except Exception as e:
            # Print the exception message for debugging
            print(f"Exception: {str(e)}")
            # Reraise the exception to get more details in the console or Django error page
            raise e
    else:
        return JsonResponse({'error': 'WTF?'}, status=405)


"""
APIs for JobManagers or WorkStudyAdmin
"""


def job_manager_approve_job(request, job_manager_id, job_number):
    # find job manager's obj according to job_manager_id
    work_admin = WorkStudyAdmin.objects.get(work_admin_id=job_manager_id)
    # call job manager's approve_job(cls, job_number)
    work_admin.approve_job(job_number=job_number)
    response_data = {'message:': f'{work_admin.work_admin_name}: A new job has been approved!'}
    return JsonResponse(response_data, status=200)


# VIP
def job_manager_load_jobs(request, employer_id):
    # find all jobs()
    if request.method == 'GET':
        # find the student obj according to this employer_id
        try:
            # B: find all jobs objs that are related to this manager
            job_man = Employer.objects.get(employer_id = employer_id)
            return JsonResponse(job_man_flow(job_man),safe=False)
        except Employer.DoesNotExist:
            return JsonResponse({'error': 'Invalid job_manager_id'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)



"""
APIs for company or Employer
"""


# VIP
def make_new_job(request, employer_id):
    if request.method == 'POST':
        try:
            job_json = json.loads(request.body)
            job_number = job_json.get('job_number')
            job_title = job_json.get('job_title')
            job_content = job_json.get('job_content')
            job_salary = job_json.get('salary')
            job_dict = {
                'job_number': job_number,
                'job_title': job_title,
                'job_content': job_content,
                'salary': job_salary
            }
            # Create an employer case to make a new job
            employer = Employer.objects.get(employer_id=employer_id)
            employer.create_job(job_dict)
            response_data = {'message': f'{employer.employer_name}: New job was successfully release!'}

            return JsonResponse(response_data, status=200)
        except json.JSONDecodeError:
            response_data = {'error': 'Invalid JSON data'}
            return JsonResponse(response_data, status=400)
    else:
        response_data = {'error': 'Invalid JSON data'}
        return JsonResponse(response_data, status=405)


def submit_job_feedback(request, employer_id, job_number, job_feedback):
    employer = Employer.objects.get(employer_id=employer_id)
    employer.provide_feedback(feedback_text=job_feedback, job_number=job_number)
    response_data = {'message:': f'{employer.employer_name}: Feedback has been submitted'}

    return JsonResponse(response_data, status=200)

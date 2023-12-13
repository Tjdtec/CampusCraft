from django.db import models

# Create your models here.
from django.db import models


class Student(models.Model):
    name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    introduction = models.TextField()
    major = models.CharField(max_length=50)
    class_name = models.CharField(max_length=20)
    student_id = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Counselor(models.Model):
    employee_id = models.CharField(max_length=10)
    major = models.CharField(max_length=50)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_students(self):
        # 获取与该辅导员专业相同的学生
        return Student.objects.filter(major=self.major)


class Job(models.Model):
    student_job_fk = models.ManyToManyField(Student, blank=True)
    job_number = models.CharField(max_length=10, unique=True)
    is_approved = models.BooleanField(default=False)
    job_title = models.CharField(max_length=100)
    job_content = models.TextField()
    salary = models.IntegerField()
    feedback = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Job {self.job_number}: {self.job_title}"


class Employer(models.Model):
    jobs_em_fk_2 = models.ManyToManyField(Job, blank=True)
    employer_id = models.CharField(max_length=10, unique=True)
    employer_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.employer_name} ({self.employer_id})"


class WorkStudyAdmin(models.Model):
    work_admin_id = models.CharField(max_length=10, unique=True)
    work_admin_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.work_admin_name} ({self.work_admin_id})"


class StudentAffair(models.Model):
    stu_admin_id = models.CharField(max_length=10, unique=True)
    stu_admin_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.stu_admin_name} ({self.stu_admin_id})"


class Login(models.Model):
    STUDENT = 0
    COUNSELOR = 1
    EMPLOYER = 2
    WORK_STUDY_ADMIN = 3
    STUDENT_AFFAIRS = 4

    USER_TYPES = [
        (STUDENT, 'Student'),
        (COUNSELOR, 'Counselor'),
        (EMPLOYER, 'Employer'),
        (WORK_STUDY_ADMIN, 'Work Study Admin'),
        (STUDENT_AFFAIRS, 'Student Affairs'),
    ]
    user_names = models.CharField(max_length=30, unique=True)
    user_passwords = models.CharField(max_length=100)
    user_type = models.CharField(max_length=20, choices=USER_TYPES)

    def __str__(self):
        return f"{self.user_names} ({self.get_user_type_display()})"

from django.contrib import admin

# Register your models here.

from django.contrib import admin

from .models import WorkStudyAdmin, Student, Counselor, Employer, Job, StudentAffair, Login

admin.site.register(WorkStudyAdmin)
admin.site.register(Student)
admin.site.register(Counselor)
admin.site.register(Employer)
admin.site.register(Job)
admin.site.register(StudentAffair)
admin.site.register(Login)

from django.db import models

# Create your models here.
from django.db import models
from django.db.models import Max, Min


class Student(models.Model):
    """
       学生类模型

       属性:
       - name (CharField): 学生姓名，最大长度为100个字符。
       - contact_number (CharField): 联系方式，最大长度为15个字符，可选字段。
       - introduction (TextField): 简介信息。
       - major (CharField): 专业，最大长度为50个字符。
       - class_name (CharField): 班级，最大长度为20个字符。
       - student_id (CharField): 学号，最大长度为10个字符。

       方法:
       - login(cls, username, password): 学生登录方法，通过用户名和密码验证登录。
       - apply_for_job(self, job): 学生申请工作的方法，将自己关联到特定的工作。
       - view_student_info(self): 查看学生基本信息的方法，返回一个包含学生信息的字典。
       - view_applied_jobs(self): 查看所投递的工作的方法，返回学生所投递的所有工作。
       - view_approved_jobs(self): 查看所有通过审核的工作的方法，返回所有通过审核的工作。
       - modify_introduction(self, new_introduction): 学生修改自己简介信息的方法，更新简介信息。
       - __str__(self): 返回学生对象的字符串表示形式。

       使用样例:
       student = Student.login(username='example_username', password='example_password')
       if student:
           student.apply_for_job(job)
           student_info = student.view_student_info()
           applied_jobs = student.view_applied_jobs()
           approved_jobs = student.view_approved_jobs()
           student.modify_introduction(new_introduction='New introduction text.')
           student.modify_contact_number(new_number='New number.')
           print(student)
       """
    name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15, blank=True)
    introduction = models.TextField()
    major = models.CharField(max_length=50)
    class_name = models.CharField(max_length=20)
    student_id = models.CharField(max_length=10)

    @classmethod
    def login(cls, username, password):
        """
            @classmethod 是一个装饰器，用于定义类方法。类方法是在类级别而不是实例级别调用的方法。
            类方法的第一个参数通常是类本身，通常命名为 cls。在这个示例中，@classmethod 被用于修
            饰 login 方法，使其成为 Counselor 类的类方法。这样定义的类方法可以通过类本身调用，
            而不需要先创建类的实例。

            使用样例:
            student = Student.login(username='example_username', password='example_password')
            if student:
                print(f"登录成功，欢迎 {student.name}!")
            else:
                print("登录失败，请检查用户名和密码。")
            """
        try:
            # 尝试通过用户名和密码查找辅导员
            login_record = Login.objects.get(user_name=username, user_password=password, user_type=Login.STUDENT)
            student = cls.objects.get(student_id=login_record.user_id)
            return student
        except (Login.DoesNotExist, cls.DoesNotExist):
            # 如果未找到匹配的记录，返回 None 表示登录失败
            return None

    def apply_for_job(self, job):
        """
        这个案例描述了学生对感兴趣的工作进行投递:
        self.job_set 是由 Django 自动生成的一个反向关系。在 Django 的模型中，如果一个模型有多对多关系，Django 会为该模型自动创建一个反向
        关系，名称格式为 related_name_set，其中 related_name 是我们在关联字段上定义的名字。在Job 模型中，我们使用了
        models.ManyToManyField(Student, blank=True)，其中 Student 是多对多关系的目标模型。由于你没有显式地为这个关系
        定义 related_name，Django 将使用默认的 related_name，即模型名小写后加上 _set。因此，self.job_set 实际上是指向与当前学生关联的
        所有工作的集合。当调用 self.job_set.add(job) 时，你向这个集合中添加了一个工作对象 job，表示当前学生对这份工作感兴趣或申请。

        个人注解: 也就是说，在对应的job实例的 student_job_fk 中你是能够查看的到与这个实例相关联的所有学生的基本信息

        使用样例:
        job = Job.objects.get(job_number='example_job_number')
        student.apply_for_job(job)
        """
        self.job_set.add(job)

    def view_student_info(self):
        """
        查看学生信息的方法: 该方法会直接返回一个dict字典用以返回存储的学生信息
        使用样例:
        student_info = student.view_student_info()
        print(student_info)
        """
        return {
            'name': self.name,
            'contact_number': self.contact_number,
            'introduction': self.introduction,
            'major': self.major,
            'class_name': self.class_name,
            'student_id': self.student_id,
        }

    def view_applied_jobs(self):
        """
        查看所投递的工作对象的方法
        使用样例:
        applied_jobs = student.view_applied_jobs()
        for job in applied_jobs:
            print(job.job_title)
        """
        return self.job_set.all()

    def view_approved_jobs(self):
        """
        查看所有通过审核的工作对象的方法
        使用样例:
        approved_jobs = student.view_approved_jobs()
        for job in approved_jobs:
            print(job.job_title)
        """
        return Job.objects.filter(is_approved=True)

    def modify_introduction(self, new_introduction):
        """
        学生修改自己简介信息的方法
        使用样例:
        student.modify_introduction(new_introduction='New introduction text.')
        """
        self.introduction = new_introduction
        self.save()

    def __str__(self):
        return self.name

    def modify_contact_number(self, new_number):
        """
        学生修改自己的联系方式
        student.modify_contact_number(new_number = 'Your new number which type is charfeild.')
        """
        self.contact_number = new_number
        self.save()


class Counselor(models.Model):
    """
    辅导员类模型
    属性:
    - employee_id (CharField): 辅导员工号，最大长度为10个字符。
    - major (CharField): 专业，最大长度为50个字符。
    - name (CharField): 辅导员姓名，最大长度为100个字符。

    方法:
    - login(cls, username, password): 辅导员登录方法，通过用户名和密码验证登录。
    - get_students(self): 获取与该辅导员专业相同的所有学生。

    使用样例:
    counselor = Counselor.login(username='example_username', password='example_password')
    if counselor:
        students = counselor.get_students()
        print(counselor)
    """
    employee_id = models.CharField(max_length=10)
    major = models.CharField(max_length=50)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    @classmethod
    def login(cls, username, password):
        """
        @classmethod 是一个装饰器，用于定义类方法。类方法是在类级别而不是实例级别调用的方法。
        类方法的第一个参数通常是类本身，通常命名为 cls。在这个示例中，@classmethod 被用于修
        饰 login 方法，使其成为 Counselor 类的类方法。这样定义的类方法可以通过类本身调用，
        而不需要先创建类的实例。
        """
        try:
            # 尝试通过用户名和密码查找辅导员
            login_record = Login.objects.get(user_name=username, user_password=password, user_type=Login.COUNSELOR)
            counselor = cls.objects.get(employee_id=login_record.user_id)
            return counselor
        except (Login.DoesNotExist, cls.DoesNotExist):
            # 如果未找到匹配的记录，返回 None 表示登录失败
            return None

    def get_students(self):
        # 获取与该辅导员专业相同的学生
        return Student.objects.filter(major=self.major)
    
    def view_counselor_info(self):
        return{
            "employee_id": self.employee_id,
            "major": self.major,
            "name": self.name
        }


class Job(models.Model):
    """
    工作类模型

    属性:
    - student_job_fk (ManyToManyField): 学生外键，与该工作相关的学生集合。
    - job_number (CharField): 工作号，最大长度为10个字符，必须唯一。
    - is_approved (BooleanField): 审核状态，表示该工作是否通过审核，默认为 False。
    - job_title (CharField): 工作标题，最大长度为100个字符。
    - job_content (TextField): 工作内容描述。
    - salary (IntegerField): 薪资。
    - feedback (TextField, 可选): 反馈信息，可以为空。

    方法:
    - __str__(self): 返回工作对象的字符串表示形式。

    使用样例:
    job = Job(student_job_fk=student_instance, job_number='123456', is_approved=False,
               job_title='Part-time Job', job_content='Job description', salary=1000)
    job.save()
    print(job)
    """
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
    """
    用人单位类模型

    属性:
    - jobs_em_fk_2 (ManyToManyField): 工作外键，与该用人单位发布的工作相关联的工作集合。
    - employer_id (CharField): 用人单位ID，最大长度为10个字符，必须唯一。
    - employer_name (CharField): 用人单位名称，最大长度为100个字符。
     - contact_number (CharField): 联系电话，最大长度为15个字符。

    方法:
    - __str__(self): 返回用人单位对象的字符串表示形式。
    - login(cls, username, password): 用于用人单位登录的类方法。
    - create_job(self, job_data): 用于用人单位发布工作的方法。
    - view_all_students(self): 用于用人单位查看所有学生信息的方法。
    - view_applied_students(self): 用于用人单位查看投递了自己发布的所有工作岗位的学生的方法。
    - view_all_jobs(self): 用于用人单位查看所有自己发布的工作的方法。
    - provide_feedback(self, job_number, feedback_text): 用于用人单位填写某个工作岗位的反馈信息的方法。

    使用样例:
    employer = Employer(employer_id='123456', employer_name='ABC Company', contact_number='123-456-7890')
    employer.save()

    # 登录用人单位
    logged_in_employer = Employer.login(username='abc_company', password='secure_password')

    # 发布工作
    job_data = {'job_number': '789012', 'is_approved': False, 'job_title': 'Intern', 'job_content': 'Job description', 'salary': 1500}
    new_job = logged_in_employer.create_job(job_data)

    # 查看所有学生信息
    all_students = logged_in_employer.view_all_students()

    # 查看投递了自己发布的所有工作岗位的学生
    applied_students = logged_in_employer.view_applied_students()

    # 查看所有自己发布的工作
    all_jobs = logged_in_employer.view_all_jobs()

    # 提供反馈信息
    job_number = '789012'
    feedback_text = 'Great candidate!'
    success = logged_in_employer.provide_feedback(job_number, feedback_text)
    """
    jobs_em_fk_2 = models.ManyToManyField(Job, blank=True)
    employer_id = models.CharField(max_length=10, unique=True)
    employer_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)

    @classmethod
    def login(cls, username, password):
        """
           @classmethod 是一个装饰器，用于定义类方法。类方法是在类级别而不是实例级别调用的方法。
           类方法的第一个参数通常是类本身，通常命名为 cls。在这个示例中，@classmethod 被用于修
           饰 login 方法，使其成为 Counselor 类的类方法。这样定义的类方法可以通过类本身调用，
           而不需要先创建类的实例。
           """
        try:
            # 尝试通过用户名和密码查找辅导员
            login_record = Login.objects.get(user_name=username, user_password=password, user_type=Login.EMPLOYER)
            employer = cls.objects.get(employer_id=login_record.user_id)
            return employer
        except (Login.DoesNotExist, cls.DoesNotExist):
            # 如果未找到匹配的记录，返回 None 表示登录失败
            return None

    def create_job(self, job_data):
        """
        用人单位发布工作的方法
        用人单位根据前端传入的数据，创建一个新的用户实例
        """
        job = Job.objects.create(**job_data)
        self.jobs_em_fk_2.add(job)
        return job

    def view_all_students(self):
        """
        用人单位查看所有学生信息的方法
        """
        return Student.objects.all()

    def view_applied_students(self):
        """
        用人单位可以查看投递了自己发布的所有工作岗位的学生
        参数 job__in 是 Django ORM 的查询语法之一，用于查询与某个关联模型的外键关系中包含
        在给定列表或查询集中的对象。在这里，job__in 用于查询与 Job 模型的外键关联中包含在
        jobs 列表中的对象。
        """
        jobs = self.jobs_em_fk_2.all()
        students = Student.objects.filter(job__in=jobs)
        return students

    def view_all_jobs(self):
        """
        用人单位可以查看所有自己发布的工作
        """
        return self.jobs_em_fk_2.all()

    def provide_feedback(self, job_number, feedback_text):
        """
        用人单位填写某个工作岗位的反馈信息的方法
        """
        try:
            job = self.jobs_em_fk_2.get(job_number=job_number)
            job.feedback = feedback_text
            job.save()
            return True
        except Job.DoesNotExist:
            return False

    def __str__(self):
        return f"{self.employer_name} ({self.employer_id})"
    

    def view_employer_info(self):
        return{
            "employer_id": self.employer_id,
            "employer_name": self.employer_name,
            "contact_number": self.contact_number
        }


class WorkStudyAdmin(models.Model):
    """
    勤工俭学管理员类模型

    属性:
    - work_admin_id (CharField): 勤工俭学管理员ID，最大长度为10个字符，必须唯一。
    - work_admin_name (CharField): 勤工俭学管理员名称，最大长度为100个字符。

    方法:
    - __str__(self): 返回勤工俭学管理员对象的字符串表示形式。
    - login(cls, username, password): 用于勤工俭学管理员登录的类方法。
    - view_all_students_info(self): 勤工俭学管理员查看所有学生的信息及其所投递的岗位的方法。
    - approve_job(cls, job_number): 勤工俭学管理员通过审核工作的方法。

    使用样例:
    work_study_admin = WorkStudyAdmin(work_admin_id='admin123', work_admin_name='Admin User')
    work_study_admin.save()

    # 登录勤工俭学管理员
    logged_in_admin = WorkStudyAdmin.login(username='admin_user', password='secure_password')

    # 查看所有学生信息及其所投递的岗位
    all_students_info = logged_in_admin.view_all_students_info()

    # 通过审核工作
    job_number = '789012'
    logged_in_admin.approve_job(job_number)
    """

    work_admin_id = models.CharField(max_length=10, unique=True)
    work_admin_name = models.CharField(max_length=100)

    @classmethod
    def login(cls, username, password):
        """
           @classmethod 是一个装饰器，用于定义类方法。类方法是在类级别而不是实例级别调用的方法。
           类方法的第一个参数通常是类本身，通常命名为 cls。在这个示例中，@classmethod 被用于修
           饰 login 方法，使其成为 Counselor 类的类方法。这样定义的类方法可以通过类本身调用，
           而不需要先创建类的实例。
           """
        try:
            # 尝试通过用户名和密码查找辅导员
            login_record = Login.objects.get(user_name=username, user_password=password, user_type=Login.WORK_STUDY_ADMIN)
            work_study_admin = cls.objects.get(work_admin_id=login_record.user_id)
            return work_study_admin
        except (Login.DoesNotExist, cls.DoesNotExist):
            # 如果未找到匹配的记录，返回 None 表示登录失败
            return None

    def view_all_students_info(self):
        """
        勤工俭学管理员查看所有学生的信息及其所投递的岗位的方法
        """
        students_info = []
        for student in Student.objects.all():
            student_info = {
                'student': student,
                'applied_jobs': student.job_set.all(),
            }
            students_info.append(student_info)
        return students_info

    @classmethod
    def approve_job(cls, job_number):
        """
        勤工俭学管理员通过审核工作的方法
        """
        job = Job.objects.get(job_number=job_number)
        job.is_approved = True
        job.save()

    def __str__(self):
        return f"{self.work_admin_name} ({self.work_admin_id})"
    
    def view_work_study_admin_info(self):
        return{
            "work_admin_id": self.work_admin_id,
            "work_admin_name": self.work_admin_name
        }


class StudentAffair(models.Model):
    """
    学生处类模型

    属性:
    - stu_admin_id (CharField): 学生处管理员ID，最大长度为10个字符，必须唯一。
    - stu_admin_name (CharField): 学生处管理员名称，最大长度为100个字符。

    方法:
    - __str__(self): 返回学生处管理员对象的字符串表示形式。
    - login(cls, username, password): 用于学生处管理员登录的类方法。
    - view_all_students_info(self): 学生处管理员查看所有学生信息的方法。
    - get_students_statistics(self): 学生处管理员获取全体学生的统计信息的方法。
    - get_income_statistics(self): 学生处管理员获取参加勤工俭学学生的收入统计信息的方法。
    - add_student(self, name, gender, student_id): 学生处管理员添加学生的基本信息的方法。
    - modify_student_info(self, student_id, new_name, new_gender): 学生处管理员修改学生基本信息的方法。
    - delete_student(self, student_id): 学生处管理员删除学生基本信息的方法。

    使用样例:
    student_affair = StudentAffair(stu_admin_id='admin123', stu_admin_name='Student Affairs Admin')
    student_affair.save()

    # 登录学生处管理员
    logged_in_admin = StudentAffair.login(username='admin_user', password='secure_password')

    # 查看所有学生信息
    all_students_info = logged_in_admin.view_all_students_info()

    # 获取学生统计信息
    students_statistics = logged_in_admin.get_students_statistics()

    # 获取收入统计信息
    income_statistics = logged_in_admin.get_income_statistics()

    # 添加学生信息
    new_student = logged_in_admin.add_student(name='New Student', gender='Male', student_id='123456')

    # 修改学生信息
    modified_student = logged_in_admin.modify_student_info(student_id='123456', new_name='Modified Student', new_gender='Female')

    # 删除学生信息
    deleted_student = logged_in_admin.delete_student(student_id='123456')
    """

    stu_admin_id = models.CharField(max_length=10, unique=True)
    stu_admin_name = models.CharField(max_length=100)

    @classmethod
    def login(cls, username, password):
        """
           @classmethod 是一个装饰器，用于定义类方法。类方法是在类级别而不是实例级别调用的方法。
           类方法的第一个参数通常是类本身，通常命名为 cls。在这个示例中，@classmethod 被用于修
           饰 login 方法，使其成为 Counselor 类的类方法。这样定义的类方法可以通过类本身调用，
           而不需要先创建类的实例。
           """
        try:
            # 尝试通过用户名和密码查找辅导员
            login_record = Login.objects.get(user_name=username, user_password=password, user_type=Login.STUDENT_AFFAIRS)
            stu_affair = cls.objects.get(stu_admin_id=login_record.user_id)
            return stu_affair
        except (Login.DoesNotExist, cls.DoesNotExist):
            # 如果未找到匹配的记录，返回 None 表示登录失败
            return None

    def view_all_students_info(self):
        """
        学生处查看所有学生信息的方法
        """
        return Student.objects.all()

    def get_students_statistics(self):
        """
        学生处获取全体学生的统计信息的方法
        """
        total_students = Student.objects.count()
        students_with_jobs = Student.objects.filter(job__isnull=False).count()

        return {
            'total_students': total_students,
            'students_with_jobs': students_with_jobs,
        }

    def get_income_statistics(self):
        """
        学生处获取参加勤工俭学学生的收入统计信息的方法
        """
        students_with_jobs = Student.objects.filter(job__isnull=False)
        if students_with_jobs.exists():
            max_income = students_with_jobs.aggregate(Max('job__salary'))['job__salary__max']
            min_income = students_with_jobs.aggregate(Min('job__salary'))['job__salary__min']
        else:
            max_income = min_income = 0

        return {
            'max_income': max_income,
            'min_income': min_income,
        }

    def add_student(self, name, gender, student_id):
        """
        学生处添加学生的基本信息的方法
        """
        student = Student.objects.create(name=name, gender=gender, student_id=student_id)
        return student

    def modify_student_info(self, student_id, new_name, new_gender):
        """
        学生处修改学生基本信息的方法
        """
        try:
            student = Student.objects.get(student_id=student_id)
            student.name = new_name
            student.gender = new_gender
            student.save()
            return True
        except Student.DoesNotExist:
            return False

    def delete_student(self, student_id):
        """
        学生处删除学生基本信息的方法
        """
        try:
            student = Student.objects.get(student_id=student_id)
            student.delete()
            return True
        except Student.DoesNotExist:
            return False

    def view_student_affair_info(self):
        return{
            'stu_admin_id': self.stu_admin_id,
            'stu_admin_name': self.stu_admin_name
        }

    def __str__(self):
        return f"{self.stu_admin_name} ({self.stu_admin_id})"


class Login(models.Model):
    """
    登录信息类模型

    属性:
    - user_name (CharField): 用户名，最大长度为30个字符，必须唯一。
    - user_password (CharField): 用户密码，最大长度为100个字符。
    - user_type (CharField): 用户类型，使用 choices 参数限制为预定义的用户类型，包括学生、辅导员、用人单位、
            勤工俭学管理员和学生处管理员。
    - user_id (CharField): 用户id，存储对应的用户在相关的表中所属的id，默认值为0000，最大长度为10个字符

    方法:
    - __str__(self): 返回登录信息对象的字符串表示形式。

    使用样例:
    login_record = Login(user_name='john_doe', user_password='secure_password', user_type=Login.STUDENT)
    login_record.save()

    # 获取用户类型的显示名称
    user_type_display = login_record.get_user_type_display()
    """
    STUDENT = 'Student'
    COUNSELOR = 'Counselor'
    EMPLOYER = 'Employer'
    WORK_STUDY_ADMIN = 'Work Study Admin'
    STUDENT_AFFAIRS = 'Student Affairs'

    USER_TYPES = [
        (STUDENT, 'Student'),
        (COUNSELOR, 'Counselor'),
        (EMPLOYER, 'Employer'),
        (WORK_STUDY_ADMIN, 'Work Study Admin'),
        (STUDENT_AFFAIRS, 'Student Affairs'),
    ]
    user_name = models.CharField(max_length=30, unique=True)
    user_password = models.CharField(max_length=100)
    user_type = models.CharField(max_length=20, choices=USER_TYPES)
    user_id = models.CharField(max_length=10, default='0000')

    def __str__(self):
        return f"{self.user_name} ({self.get_user_type_display()})"
# Generated by Django 4.2.8 on 2023-12-13 03:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("campusapp", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Login",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("user_names", models.CharField(max_length=30, unique=True)),
                ("user_passwords", models.CharField(max_length=100)),
                (
                    "user_type",
                    models.CharField(
                        choices=[
                            (0, "Student"),
                            (1, "Counselor"),
                            (2, "Employer"),
                            (3, "Work Study Admin"),
                            (4, "Student Affairs"),
                        ],
                        max_length=20,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="StudentAffairs",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("stu_admin_id", models.CharField(max_length=10, unique=True)),
                ("stuadmin_name", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="WorkStudyAdmin",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("work_admin_id", models.CharField(max_length=10, unique=True)),
                ("work_admin_name", models.CharField(max_length=100)),
            ],
        ),
        migrations.DeleteModel(
            name="Admin",
        ),
        migrations.AlterField(
            model_name="employer",
            name="jobs_em_fk_2",
            field=models.ManyToManyField(blank=True, to="campusapp.job"),
        ),
        migrations.AlterField(
            model_name="job",
            name="student_job_fk",
            field=models.ManyToManyField(blank=True, to="campusapp.student"),
        ),
    ]
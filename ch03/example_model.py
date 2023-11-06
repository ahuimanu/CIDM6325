from django.db import models


class Program(models.Model):
    pass


class Course(models.Model):
    pass


class Catalog(models.Model):
    courses = models.ForeignKey(Course, on_delete=models.CASCADE)


class ProgramCourses(models.Model):
    # many to many can go here too
    pass


class ProgramCourse(models.Model):
    """Serves as the degree requirement course specification"""

    program_id = models.ForeignKey(Program, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    is_core = models.BooleanField()
    is_degree = models.BooleanField()
    is_major = models.BooleanField()
    guide_semester = models.IntegerField()

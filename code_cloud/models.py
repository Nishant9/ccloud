from django.db import models
from django.conf import settings

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')
class Problem(models.Model):
    DIFFICULT = 'DF'
    MEDIUM = 'MD'
    EASY = 'ES'
    PUBLIC = 'PB'
    PRIVATE = 'PV'
    CODECHEF = 'CC'
    CODEFORCES = 'CF'
    UVA = 'UV'
    TOPCODER = 'TC'
    SPOJ = 'SP'
    NONE = 'NA'
    OJ_CHOICES = (
        (CODECHEF, 'Codechef'),
        (UVA, 'UVa'),
        (CODEFORCES, 'Codeforces'),
        (TOPCODER, 'Topcoder'),
        (SPOJ, 'Sphere Online Judge'),
        (NONE, 'Not Applicable')
    )
    ACCESS_CHOICES = (
        (PUBLIC, 'Public'),
        (PRIVATE, 'Private'),
    )
    DIFFICULTY_CHOICES = (
        (DIFFICULT, 'Difficult'),
        (MEDIUM, 'Medium'),
        (EASY, 'Easy'),
        (NONE, 'Not Applicable')
    )
    name = models.CharField(max_length = 200)
    date_created = models.DateTimeField(auto_now_add = True)
    online_judge = models.CharField(max_length = 200, choices = OJ_CHOICES)
    difficulty = models.CharField(max_length = 2, choices = DIFFICULTY_CHOICES, default = EASY)
    access = models.CharField(max_length = 2, choices = ACCESS_CHOICES, default = PRIVATE)
    docfile = models.FileField(upload_to = 'documents/%Y/%m/%d')

class Notifications(models.Model):
    userid = models.ForeignKey(AUTH_USER_MODEL)
    notification = models.CharField(max_length = 400)

class Tags(models.Model):
    problem = models.ForeignKey(Problem, on_delete = models.CASCADE)
    tag = models.CharField(max_length = 50)

class Share(models.Model):
    problem = models.ForeignKey(Problem, on_delete = models.CASCADE)
    share_user = models.ForeignKey(AUTH_USER_MODEL)

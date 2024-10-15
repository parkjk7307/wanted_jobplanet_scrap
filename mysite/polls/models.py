# **공고제목 - title**
# **회사이름 - company_name**
# **디테일 페이지로 가는 주소 - detail_url **
# **마감일 - end_date**
# ** 참고한 플랫폼 이름 - platform_name**

from django.db import models

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
# **공고제목 - title**
# **회사이름 - company_name**
# **디테일 페이지로 가는 주소 - detail_url **
# **마감일 - end_date**
# ** 참고한 플랫폼 이름 - platform_name**

from django.db import models
from django.utils import timezone
import datetime
from django.contrib import admin

class Question(models.Model):
    question_text = models.CharField(max_length=200, verbose_name='질문')
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='생성일') # auto_now_add 퀘스찬이 처음 생길때 시간을 add한다.
#    owner = models.ForeignKey('auth.User', related_name='questions', on_delete=models.CASCADE, null=True)

    @admin.display(boolean=True, description='최근생성(하루기준)')
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    
    def __str__(self):
        if self.was_published_recently():
            new_badge = 'NEW!!!'
        else:
            new_badge = ''
        return f'{new_badge} 제목: {self.question_text}, 날짜: {self.pub_date}'

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    # 모델 생성 완료
    # question이 Choice 여러개를 포함하고 있다.

    def __str__(self):
        return f'[{self.question.question_text}] / {self.choice_text}'

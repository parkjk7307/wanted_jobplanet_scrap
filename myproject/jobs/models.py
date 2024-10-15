from django.db import models

class Job(models.Model):
    title = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200)
    skills = models.TextField(null=True, blank=True)
    detail_url = models.URLField(unique=True)  # detail_url이 고유하도록 설정
    end_date = models.CharField(max_length=100, default='상시 채용')
    platform_name = models.CharField(max_length=100, default='Jobplanet')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
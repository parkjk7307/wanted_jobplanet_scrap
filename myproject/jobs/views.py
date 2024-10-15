from django.shortcuts import render
from .models import Job
from .scraping import scrape_jobs  # 스크래핑 함수 임포트

def job_list(request):
    # 스크래핑된 데이터를 가져오기
    jobs_data = scrape_jobs()

    # 데이터베이스에 저장
    for job_data in jobs_data:
        Job.objects.get_or_create(
            detail_url=job_data['detail_url'],  # 중복 방지 기준
            defaults={
                'title': job_data['title'],
                'company_name': job_data['company_name'],
                'skills': job_data['skills'],
                'end_date': job_data['end_date'],
                'platform_name': job_data['platform_name'],
            }
        )

    # 데이터베이스에서 모든 공고 가져오기
    jobs = Job.objects.all()

    # 템플릿으로 데이터 전달
    return render(request, 'jobs/job_list.html', {'jobs': jobs})
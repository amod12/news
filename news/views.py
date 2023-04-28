import json

from csp.decorators import csp_exempt
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.db.models.query import QuerySet


from news.models import News
# from placess.trip_calculator import get_iterinary, process_iterinary
# from places.matcher import match_recommendation
from news.matcher import Matcher


def get_matched_news(description: str) -> QuerySet[News]:
    # matched_place_ids = match_recommendation(description)
    matcher = Matcher()
    matched_new_ids = matcher.matcher(description)
    print(matched_new_ids)
    news = []
    if matched_new_ids:
        for news_id in matched_new_ids:
            print('@@')
            if news_id:
                new = News.objects.get(id=news_id)
                news.append(new)
    return news[:3]

@csp_exempt
def get_recommendation(request):
    user_description = request.POST.get('user_description',)
    
    news=''
    query=user_description
    if len(user_description) > 2:
        
        news = get_matched_news(user_description)
    else:
        query="none"
    return render(request, 'result.html', context={"newss": news,"query":query})


@csp_exempt 
def get_input_form_page(request):
    news=News.objects.all()
    # print(news)
    return render(request, 'input_form.html', {
        'foo': 'bar',
        'news': news,
    })
def detail_page(request,id=None):
    news=get_object_or_404(News,id=id)
    recommended= get_matched_news(news.title)
    context={
        'news':news,
        'recommended_news':recommended
    }
    return render(request,'details.html',context)
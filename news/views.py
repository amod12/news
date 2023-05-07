import json

from csp.decorators import csp_exempt
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.db.models.query import QuerySet


from news.models import News
from news.matcher import Matcher


def get_matched_news(description: str,rem_id=None) -> QuerySet[News]:
    # matched_place_ids = match_recommendation(description)
    matcher = Matcher()
    matched_new_ids = matcher.matcher(description)
    
    news = []
    if matched_new_ids:
        for news_id in matched_new_ids:
            if news_id and news_id != rem_id:
                news_item = News.objects.get(id=news_id)
                news.append(news_item)
    return news[:4]


@csp_exempt
def get_recommendation(request):
    user_description = request.POST.get('user_description',)
    
    news=''
    query=user_description
    if len(user_description) > 1:
        news = get_matched_news(user_description)
        print(len(news))

    else:
        query="none"
    return render(request, 'result.html', context={"newss": news,"query":query})


@csp_exempt 
def get_input_form_page(request):
    news=News.objects.all().order_by('-add_time',)
    print(type(news))
    # print(news)
    return render(request, 'input_form.html', {
        'foo': 'bar',
        'news': news,
    })
    
    

@csp_exempt 
def detail_page(request,id=None):
    news=get_object_or_404(News,id=id)
    recommended= get_matched_news(news.title,rem_id=id)
    context={
        'news':news,
        'recommended_news':recommended
    }
    return render(request,'details.html',context)

@csp_exempt 
def base(request):
    return render(request,'abc.html')


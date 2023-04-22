import json

from csp.decorators import csp_exempt
from django.shortcuts import render
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
    news = []
    if matched_new_ids:
        for news_id in matched_new_ids:
            print('@@')
            print(news_id)
            new = News.objects.get(id=news_id)
            news.append(new)
    return news[:3]

@csp_exempt
def get_recommendation(request):
    user_description = request.POST.get('user_description')
    news = get_matched_news(user_description)
    print(news)
    return render(request, 'result.html', context={"newss": news})


@csp_exempt 
def get_input_form_page(request):
    return render(request, 'input_form.html', {
        'foo': 'bar',
    })

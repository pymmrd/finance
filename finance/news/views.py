# Create your views here.

#Django Core imports
from django.utils import simplejson
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

#Project imports
from news.models import NewsItem

@csrf_exempt
def delete_news(request):
    success = False
    pk = int(request.POST.get('pk'))
    ni = NewsItem.objects.get(pk=pk).delete()
    success = True
    response = simplejson.dumps({'success': success})
    return HttpResponse(response, content_type='application/javascript; charset=utf-8')



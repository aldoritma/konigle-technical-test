import json
from multiprocessing import context
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ValidationError

from django.core.validators import validate_email
from django.views.decorators.csrf import csrf_exempt
from unity.models import Subscriber
from datetime import datetime, timezone
from django.core.paginator import Paginator

def index(request):
    model = Subscriber()
    total_emails = model.total_emails()
    total_unsubscribers = model.total_unsubscribers()
    total_emails_this_month = model.total_emails_this_month()
    subscribers = Subscriber.objects.all().order_by('-timestamp')
    subscribers = Paginator(subscribers, 5)
    subscribers = subscribers.get_page(request.GET.get('page', 1))
    context = {
        'subscribers': subscribers,
        'total_emails': total_emails,
        'total_unsubscribers': total_unsubscribers,
        'total_emails_this_month': total_emails_this_month,
        'current_date': datetime.now(timezone.utc).strftime('%B %Y')
        
    }
    return render(request, 'subscribers/index.html', context)



# API /subscribe
@csrf_exempt
@require_http_methods(["POST"])
def subscribe(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        email = data.get('email')
        validate_email(email)
        subscriber = Subscriber.objects.filter(email=email).first()
        # Check subscriber exists
        if not subscriber:
            subscriber = Subscriber(email=email)
            subscriber.save()
        else:
            subscriber.status = 'SUBSCRIBED'
            subscriber.save()
        return HttpResponse(json.dumps({'message': 'Subscribed successfully'}), status=200, content_type='application/json')
    except ValidationError as e:
        return HttpResponse(json.dumps({'status': 'error'}), status=422, content_type='application/json')

@csrf_exempt
@require_http_methods(["POST"])
def unsubscribe(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        email = data.get('email')
        validate_email(email)
        subscriber = Subscriber.objects.filter(email=email).first()
        if not subscriber:
            return HttpResponse(json.dumps({'message': 'Subscriber not found'}), status=404, content_type='application/json')

        subscriber.status = 'UNSUBSCRIBED'
        subscriber.save()

        return HttpResponse(json.dumps({'status': 'ok', 'email': subscriber.email}), content_type='application/json')
    except ValidationError:
        return HttpResponse(json.dumps({'status': 'error'}), status=400)
    except Exception as e:
        print(e)
        return HttpResponse(json.dumps({'status': 'error'}), status=500)

        
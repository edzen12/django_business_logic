from mailchimp3 import MailChimp

from django.http import JsonResponse
from django.conf import settings

from mailings.models import CommonMailingList


def add_to_common_list_view(request):
    """веб-сервис добавляющий email в общий лист рассылки"""

    email = request.GET.get('email')
    if not email:
        return JsonResponse({'success': False, 'message':'Передайте email'})
    
    mailchimp_client = MailChimp(
        mc_api=settings.MAILCHIMP_API_KEY, 
        mc_user=settings.MAILCHIMP_USERNAME)

    mailchimp_client.lists.members.create(settings.MAILCHIMP_COMMON_LIST_ID, {
        'email_address': email,
        'status': 'subscribed', 
    })
    subscriber_hash=mailchimp_client \
        .search_members \
        .get(query=email,
             fields='exact_matches.members.id') \
        .get('exact_matches').get('members')[0].get('id')

    mailchimp_client.lists.members.tags.update(
        list_id=settings.MAILCHIMP_COMMON_LIST_ID,
        subscriber_hash=subscriber_hash,
        data={'tags':[{'name':'COMMON TAG', 'status':'active'}]})

    return JsonResponse({'success':True})
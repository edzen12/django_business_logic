from typing import Optional
from mailchimp3 import MailChimp

from django.http import JsonResponse
from django.conf import settings

from mailings.models import CommonMailingList, CaseMailingList
from cases.models import Case


def add_to_common_list_view(request):
    """веб-сервис добавляющий email в общий лист рассылки"""

    email = request.GET.get('email')
    if not email:
        return JsonResponse({'success': False, 'message':'Передайте email'})
 
    _add_email_to_mailchimp_audience(audience_id=settings.MAILCHIMP_COMMON_LIST_ID, email=email)
    subscriber_hash = _get_mailchimp_subscriber_hash(email)
    _add_mailchimp_tag(settings.MAILCHIMP_COMMON_LIST_ID, subscriber_hash=subscriber_hash, tag='COMMON TAG')  
    
    CommonMailingList.objects.get_or_create(email=email)

    return JsonResponse({'success':True})


def add_to_case_list_view(request):
    """веб-сервис добавляющий email в лист рассылок по конкретному делу"""

    email = request.GET.get('email')
    if not email:
        return JsonResponse({'success': False, 'message':'Передайте email'})
    
    case_id = request.GET.get('email')
    if not case_id:
        return JsonResponse({'success': False, 'message':'Передайте case_id'})
 
    _add_email_to_mailchimp_audience(audience_id=settings.MAILCHIMP_CASE_LIST_ID, email=email)
    subscriber_hash = _get_mailchimp_subscriber_hash(email)

    case = Case.objects.get(pk=case_id)
    case_tag = f'CASE {case.name}'

    _add_mailchimp_tag(settings.MAILCHIMP_CASE_LIST_ID, subscriber_hash=subscriber_hash, tag=case_tag) 
    CaseMailingList.objects.get_or_create(email=email, case=case)

    return JsonResponse({'success':True})

def _get_mailchimp_client() -> MailChimp:
    """Возвращает клиент API для работы с MailChimp"""
    return MailChimp(
        mc_api=settings.MAILCHIMP_API_KEY, 
        mc_user=settings.MAILCHIMP_USERNAME)

def _add_email_to_mailchimp_audience(audience_id:str, email=str) -> None:
    """Добавляет email в MailChimp аудиторию с идентификатором audience_id"""
    _get_mailchimp_client().lists.members.create(audience_id, {
        'email_address': email,
        'status': 'subscribed', 
    })

def _get_mailchimp_subscriber_hash(email:str)->Optional[str]:
    """Возвращает идентификатор email в MailChimp или None, 
    если email там не найдено"""
    members=_get_mailchimp_client() \
        .search_members \
        .get(query=email,
             fields='exact_matches.members.id') \
        .get('exact_matches').get('members')
    if not members:
        return None
    return members[0].get('id')

def _add_mailchimp_tag(audience_id:str, subscriber_hash:str, tag:str)->None:
    """Добавляет тег tag для email'a с идентификатором subscriber_hash в аудитории audience_id"""
    _get_mailchimp_client().lists.members.tags.update(
        list_id=audience_id,
        subscriber_hash=subscriber_hash,
        data={'tags':[{'name':tag, 'status':'active'}]})

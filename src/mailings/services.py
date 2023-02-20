from typing import Union

from mailings.models import CommonMailingList, CaseMailingList
from cases.models import Case
from .mailchimp_services import add_mailchimp_email_with_tag


def add_email_to_common_mailchimp_list(email:str):
    """Добавляет email в общий лист рассылки"""
    add_mailchimp_email_with_tag(audience_name='COMMON',
                                  email=email,
                                  tag='COMMON TAG') 
    CommonMailingList.objects.get_or_create(email=email)


def add_email_to_case_mailchimp_list(email:str, case_id:Union[int, str]):
    """Добавляет email в лист рассылки по делу"""
    case = Case.objects.get(pk=case_id)
    case_tag = f'CASE {case.name}'
    add_mailchimp_email_with_tag(audience_name='CASES',
                                  email=email,
                                  tag=case_tag)  
    CaseMailingList.objects.get_or_create(email=email, case=case)
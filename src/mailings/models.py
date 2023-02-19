from django.db import models


class CommonMailingList(models.Model):
    """Рассылка на общие материалы с сайта"""
    email = models.EmailField('Email подписчика')

    class Meta:
        db_table = 'common_mailing_list'


class CommonMailingList(models.Model):
    """Рассылка на материалы конкретного дела"""
    email = models.EmailField('Email подписчика')
    case = models.ForeignKey(to='cases.Case', verbose_name="Дело", on_delete=models.CASCADE)

    class Meta:
        db_table = 'case_mailing_list'



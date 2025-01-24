from django.db import models


class WhitelistedUser(models.Model):
    """ Модель белого листа """
    telegram_id = models.BigIntegerField(unique=True,
                                         verbose_name='Телеграм ИД')
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Белый лист'
        verbose_name_plural = 'Белый лист'

    def __str__(self):
        return self.telegram_id

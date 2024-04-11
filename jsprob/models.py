from django.db import models


class DataUser(models.Model):
    log = models.CharField('Логин', max_length=90)
    fik = models.CharField('ФИК(-О)', max_length=200, default='0')
    scores = models.IntegerField('Очки Ls', default=0)
    pravil = models.IntegerField('Прав Отв', default=0)
    bezosh = models.IntegerField('Безош отв', default=0)
    scoresl1 = models.IntegerField('Очки L1', default=0)
    scoresl2 = models.IntegerField('Очки L2', default=0)
    scoresl3 = models.IntegerField('Очки L3', default=0)
    scoresl4 = models.IntegerField('Очки L4', default=0)
    scoresl5 = models.IntegerField('Очки L5', default=0)
    scoresl6 = models.IntegerField('Очки L6', default=0)
    scoresl7 = models.IntegerField('Очки L7', default=0)
    pop = models.IntegerField('Попытки', default=1)
    poptd = models.IntegerField('Поп сег', default=0)
    res1 = models.IntegerField('РезЦел1', default=0)
    res2 = models.IntegerField('РезЦел2', default=0)
    res3 = models.IntegerField('РезЦел3', default=0)
    res4 = models.IntegerField('РезЦел4', default=0)
    scorTD = models.IntegerField('Очки TD', default=0)
    quantwin = models.IntegerField('Побед дня', default=0)
    quanttop = models.IntegerField('TOPы7 дня', default=0)
    pole1 = models.CharField('Поле1', max_length=200, default='0')
    pole2 = models.CharField('Поле2', max_length=200, default='0')
    pole3 = models.CharField('Поле3', max_length=200, default='0')
    pole4 = models.CharField('Поле4', max_length=200, default='0')


    def __str__(self):
        return self.log  #return f'Тема: {self.temazad}'

    class Meta:
        verbose_name = 'Данные участника'
        verbose_name_plural = 'Данные участника'
        ordering = ['id']


class Indexs(models.Model):
    log = models.CharField('Указатели', max_length=90)
    ips = models.CharField('IP Users', max_length=800, default='0')
    ipskol = models.CharField('Quantity IP', max_length=200, default='0')
    curdate = models.DateField('Сегодняшняя дата', default='2022-01-01')
    pole1 = models.CharField('Поле1', max_length=200, default='0')
    pole2 = models.CharField('Поле2', max_length=200, default='0')

    def __str__(self):
        return self.log  #return f'Тема: {self.temazad}'

    class Meta:
        verbose_name = 'Индексы и указатели'
        verbose_name_plural = 'Индексы и указатели'
        ordering = ['id']

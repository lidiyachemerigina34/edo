from django.db import models


# Create your models here.
# Create your models here.
class UsersModel(models.Model):
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    ROLE_CHOICES = [
        ('ceo', 'Руководитель организации'),
        ('signer', 'Сотрудники, которые подписывают договора по доверенности'),
        ('contract', 'Сотрудники отдела Контрактной службы'),
        ('buh', 'Сотрудники Бухгалтерии и Планово-финансового управления'),
        ('lawyer', 'Сотрудники Юридической службы'),
        ('manager', 'Руководители подразделений'),
        ('delo', 'Делопроизводитель'),
        ('admin', 'Администратор'),
    ]

    #авторизационные данные
    login = models.CharField(max_length=100, verbose_name='Логин', blank=True)
    password = models.CharField(max_length=100, verbose_name='Пароль', default="")
    token  = models.CharField(max_length=100, verbose_name='Токен', blank=True)

    name = models.CharField(max_length=100, verbose_name='Имя', blank=True)
    lastname = models.CharField(max_length=100, verbose_name='Фамилия', blank=True)
    secondname = models.CharField(max_length=100, verbose_name='Отчество', blank=True)

    role = models.CharField(max_length=100, choices=ROLE_CHOICES , verbose_name='Роль', blank=True)
    email = models.CharField(max_length=100, verbose_name='Почта', blank=True)
    phone = models.CharField(max_length=100, verbose_name='Номер телефона', blank=True)

    position = models.CharField(max_length=100, verbose_name='Должность', blank=True)
    description = models.CharField(max_length=100, verbose_name='Описание', blank=True)

    image = models.FileField(upload_to='images/users/', verbose_name='Фото', blank=True)


   

    def __str__(self):
        return self.name


    def getJson(self):

        roles = []
        for r in self.role.all():
            roles.append(r.code)
        return {
            'id':self.id,
            'image': "http://tasty-catalog.ru"+self.image.url,
            'name' : self.name,
            'position': self.position,
            'isCurrentUser':False,
            'roles':roles,
            'email':self.email
        }



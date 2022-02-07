from django.db import models


# Create your models here.
from users.models import UsersModel


class FileModel(models.Model):
    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'



    fileId = models.CharField(max_length=100, verbose_name='ID файла')
    date = models.DateField(verbose_name="Создан", blank=True, auto_now=True)
    owner = models.ForeignKey(UsersModel,verbose_name='Владелец',  on_delete=models.CASCADE)
    file = models.FileField(upload_to='images/files/', verbose_name='Файл', blank=True)
    encrypted = models.BooleanField(default=False, verbose_name='Зашифрован')


    def __str__(self):
        return self.fileId

    def getJson(self):
        return {
            "id":self.id,
            "title": self.fileId,
            "fileId":self.fileId,
            "date":self.date,
            "encrypted":self.encrypted,
            "link":"https://tasty-catalog.ru"+self.file.url,
            "owner":self.owner.getJson()
        }

class TemplateModel(models.Model):
    class Meta:
        verbose_name = 'Шаблон'
        verbose_name_plural = 'Шаблоны'


    title = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField( verbose_name='Описание', blank=True)
    file = models.ForeignKey(FileModel, on_delete=models.CASCADE)
    date = models.DateField(verbose_name="Создан", auto_now=True)
    owner = models.ForeignKey(UsersModel,verbose_name='Владелец',  on_delete=models.CASCADE)
  
    def __str__(self):
        return self.title

    def getJson(self):
        return {
            "id":self.id,
            "title": self.title,
            "description": self.description,
            "file":self.file.getJson(),
            "date":self.date,
            #"link":self.file.url,
            "owner":self.owner.getJson()
        }



    
# модель отправки
class ReconciliationModel(models.Model):
    class Meta:
        verbose_name = 'Согласование'
        verbose_name_plural = 'Согласование'

    file = models.ForeignKey(FileModel, on_delete=models.CASCADE)

    
    # signFile = models.ForeignKey(FileModel, verbose_name='Подпись' , on_delete=models.CASCADE, null=True)
    # containerFile = models.ForeignKey(FileModel, verbose_name='Контайнер' , on_delete=models.CASCADE, null=True)
    # pdfFile = models.ForeignKey(FileModel, verbose_name='PDF-контейнер' , on_delete=models.CASCADE, null=True)

    description = models.CharField(max_length=100, verbose_name='Описание', blank=True)
   
    startDate = models.DateField(verbose_name="Начало", blank=True, auto_now=True)
    endDate = models.DateField(verbose_name="Конец", blank=True)

    complete = models.BooleanField(verbose_name="Завершено",default=False)
    edited = models.BooleanField(verbose_name="На доработке",default=False)
    title = models.CharField(max_length=100, verbose_name="Название",default="")

    encrypted = models.BooleanField(default=False, verbose_name='Зашифрован')

    signer = models.ForeignKey(UsersModel,default="", verbose_name="Подписывает", on_delete=models.CASCADE)
    owner = models.ForeignKey(UsersModel,default="", related_name='user_owner', verbose_name="Организовал", on_delete=models.CASCADE)




    def __str__(self):
        return self.file.fileId + "("+str(self.startDate)+"-"+str(self.endDate)+")"

    def getJson(self):
        return {
            "id":self.id,
            "title":self.title,
            "startDate":self.startDate,
            "endDate":self.endDate,
            "signer":self.signer.getJson(),
            "owner":self.owner.getJson(),
            "file":self.file.getJson(),
            "description":self.description,
            #"signFile":"" if self.signFile is None else self.signFile.getJson(),
            #"containerFile":"" if self.containerFile is None else self.containerFile.getJson(),
            #"pdfFile":"" if self.pdfFile is None else self.pdfFile.getJson(),
            "encrypted":self.encrypted
        }


class ReconciliationFileModel(models.Model):
    class Meta:
        verbose_name = 'Файл согласования'
        verbose_name_plural = 'Файлы согласования'
    
    reconciliation = models.ForeignKey(ReconciliationModel, verbose_name='Согласование' ,  on_delete=models.CASCADE)
    file = models.ForeignKey(FileModel, verbose_name='Файл' , on_delete=models.CASCADE, null=True)
    type = models.CharField(max_length=100, verbose_name="Тип",default="")



    def __str__(self):
        return self.reconciliation.title + "("+self.type+")"
# модель отправки
class ReconciliationUsersModel(models.Model):
    class Meta:
        verbose_name = 'Пользователи согласования'
        verbose_name_plural = 'Пользователи согласования'

    reconciliation = models.ForeignKey(ReconciliationModel, on_delete=models.CASCADE)
    user = models.ForeignKey(UsersModel, on_delete=models.CASCADE)

    apply = models.BooleanField(default=False, verbose_name='Принят')
    endeed = models.BooleanField(default=False, verbose_name='Завершен')


    def __str__(self):
        return self.user.name

    def getJson(self):
        return {
            'user':self.user.getJson(),
            'apply':self.apply,
            'endeed':self.endeed,
        }

# комментарии
class ReconciliationCommentsModel(models.Model):
    class Meta:
        verbose_name = 'Комментарии'
        verbose_name_plural = 'Комментарии'

    reconciliation = models.ForeignKey(ReconciliationModel, on_delete=models.CASCADE)
    user = models.ForeignKey(UsersModel, on_delete=models.CASCADE)
    text = models.CharField(max_length=100, verbose_name='Комментарий', default=-1)

    def __str__(self):
        return self.reconciliation.title

    def getJson(self):
        return {
            "id":self.id,
            "sourceType":"reconciliation",
            "source":self.reconciliation.id,
            "user":self.user.getJson(),
            "text":self.text
        }


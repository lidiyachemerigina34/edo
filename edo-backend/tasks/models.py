from django.db import models


# Create your models here.
from users.models import UsersModel


# модель отправки
class TaskModel(models.Model):

    TASK_STATUS = [
    ('INCOMING', 'Не прочитано'),
    ('IN_PROGRESS', 'Выполняется'),
    ('COMPLETE', 'Завершена'),
    ('CANCLE', 'Отменена'),
    ('WAIT', 'Ожидает'),
    ('COMPLETE_FULL', 'Завершена поставщиком'),
    ]

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    #file = models.ForeignKey(FileModel, on_delete=models.CASCADE)
    description = models.TextField( verbose_name='Описание', blank=True)

    provider = models.ForeignKey(UsersModel,verbose_name="Поставщик", related_name='provider', on_delete=models.CASCADE)
    executor = models.ForeignKey(UsersModel,verbose_name="Исполнитель",related_name='executor', on_delete=models.CASCADE)
    watcher = models.ForeignKey(UsersModel,verbose_name="Наблюдатель",related_name='watcher', on_delete=models.CASCADE)

    startDate = models.DateField(verbose_name="Начало", blank=True, auto_now_add=True)
    endDate = models.DateField(verbose_name="Конец", blank=True)

    status = models.CharField(max_length=100, verbose_name="Статус", choices=TASK_STATUS, default='INCOMING')
    file_id = models.CharField(max_length=100, verbose_name="Файл", choices=TASK_STATUS, default=False)

    title = models.CharField(max_length=100, verbose_name="Название",default="")


    def __str__(self):
        return self.title

    def getJson(self, id = -1):
        return {
            "id":self.id,
            "title":self.title,
            "startDate":self.startDate,
            "endDate":self.endDate,
            "description":self.description,
            "status":self.status,
            "provider" : self.provider.getJson(),
            "executor" : self.executor.getJson(),
            "watcher" : self.watcher.getJson(),
            "canCancle": self.provider.id == id,
            "canWork": self.executor.id == id
        }



# комментарии
class TaskCommentsModel(models.Model):
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    task = models.ForeignKey(TaskModel, on_delete=models.CASCADE)
    user = models.ForeignKey(UsersModel, on_delete=models.CASCADE)
    text = models.CharField(max_length=100, verbose_name='Комментарий', default=-1)

    def __str__(self):
        return self.text

    def getJson(self):
        return {
            "id":self.id,
            "source":self.task.id,
            "sourceType":"task",
            "user":self.user.getJson(),
            "text":self.text
        }
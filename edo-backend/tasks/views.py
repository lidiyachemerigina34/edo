import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from tasks.models import TaskModel,TaskCommentsModel
from users.views import getUserIdByToken

#получает список задач
def get(request):



    tasks = []
    currentUser = getUserIdByToken(request)
    tasksQS = TaskModel.objects.filter(executor_id = currentUser["id"])
    for task in tasksQS:
        tasks.append(task.getJson(currentUser["id"]))

    tasksQS = TaskModel.objects.filter(watcher_id = currentUser["id"])
    for task in tasksQS:
        tasks.append(task.getJson(currentUser["id"]))


    tasksQS = TaskModel.objects.filter(provider_id = currentUser["id"])
    for task in tasksQS:
        tasks.append(task.getJson(currentUser["id"]))


    return JsonResponse(
        tasks, safe=False
    )




#загрузка комментриев
@csrf_exempt
def getComment(request):
    


    comments = []
    task = TaskModel.objects.filter(id=request.GET["source"])
    if len(task) > 0:
        if task[0].status == "INCOMING":
            TaskModel.objects.filter(id=task[0].id).update(status = "WAIT")

    commentQS = TaskCommentsModel.objects.filter(task_id=request.GET["source"])

    for comment in commentQS:
        comments.append(comment.getJson())


    return JsonResponse(comments, safe=False)


#созадть
@csrf_exempt
def create(request):
    post = json.load(request)
    user_id = getId(request)

    currentUser = getUserIdByToken(request)

    TaskCommentsModelQS = TaskModel.objects.create(
        title=post["title"],
        endDate=post["endDate"],
        executor_id=post["executor"]["id"],
        provider_id=currentUser["id"],
        watcher_id=post["watcher"]["id"],
        description=post["description"]
    )

    return JsonResponse(TaskCommentsModelQS.getJson())

#смена статуса задачи
@csrf_exempt
def setStatus(request):
    post = json.load(request)
    TaskModel.objects.filter(
        id=post["taskId"]
    ).update(status=post["status"])

    return JsonResponse({
        "status":True
    })

#отправка комментария
@csrf_exempt
def sendComment(request):
    post = json.load(request)
    currentUser = getUserIdByToken(request)

    TaskCommentsModelQS = TaskCommentsModel.objects.create(
        task_id=post["source"],
        user_id=currentUser["id"],
        text=post["text"]
    )

    return JsonResponse(TaskCommentsModelQS.getJson())

import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from catalog.models import ReconciliationCommentsModel, ReconciliationModel, ReconciliationUsersModel, FileModel, TemplateModel, ReconciliationFileModel
from users.views import getUserIdByToken
from tasks.models import TaskCommentsModel
from django.core.files.storage import FileSystemStorage

#ПОЛУЧИТЬ СПИСОК СОГЛАСОВАНИЙ
def getReconciliation(request):
    currentUser = getUserIdByToken(request)
    reconciliationQS = ReconciliationModel.objects.all()
    reconciliations = []


    #ПЕРЕБИРАЕМ СОГЛАСОВАНИЯ И НАБИРАЕМ ПОД НЕГО ДАННЫЕ
    #ТИПО ПОДПИСАНО ИЛИ НЕТ , СОГЛАСОВАНО ИЛИ НЕТ , ЕСТЬ ЛИ ПРИЛОЖЕННЫЕ ФАЙЛЫ
    for reconciliation in reconciliationQS:

        needApply = False
        tmp = reconciliation.getJson()
        tmp["users"] = []

        usersQS = ReconciliationUsersModel.objects.filter(
            reconciliation_id=reconciliation.id
        )
        fullApply = True
        for u in usersQS:
            if u.apply == False:
                fullApply = False
            tmp["users"].append(u.getJson())
            if u.apply == False and u.endeed == False and u.user.id == currentUser["id"]:
                needApply = True
            for user in tmp["users"]:
                if user["user"]["id"] == currentUser["id"]:
                    user["user"]["isCurrentUser"] = True
        files = ReconciliationFileModel.objects.filter(reconciliation_id = reconciliation.id)
        tmp["files"] = []
        for f in files:
            tmp["files"].append( f.file.getJson() )
        tmp["fullApply"] = fullApply
        tmp["canSign"]  = currentUser["id"] == tmp["signer"]["id"] and len(tmp["files"]) == 0 and fullApply
        tmp["needApply"]  = needApply
        tmp["currentUser"] = currentUser
        

        tmp["canEdit"]  = currentUser["id"] == tmp["owner"]["id"]

        if not accessToReconciliation(tmp, currentUser):
            continue
        reconciliations.append(tmp)



    return JsonResponse(
        reconciliations, safe=False
        
    )
#ПРОВЕРЯЕТ ДОСТУПНО ЛИ СОГЛАСОВАНИЕ ПОЛЬЗОВАТЕЛЮ
def accessToReconciliation(reconciliation, user):
    if "contracts" in user["roles"]:
        return True

    if reconciliation["owner"]["id"] == user["id"]:
        return True     

    if reconciliation["signer"]["id"] == user["id"]:
            return True   
    for u in reconciliation["users"]:
        if user["id"] == u["user"]["id"]:
            return True
    

    return False

#СОЗДАТЬ СОГЛАСОВАНИЕ
@csrf_exempt
def createReconciliation(request):
    post = json.load(request)
    currentUser = getUserIdByToken(request)
    reconciliation = ReconciliationModel.objects.create(
        file_id=post["file"],
        title=post["title"],
        description=post["description"],
        #startDate=post["startDate"],
        endDate=post["endDate"],
        signer_id=post["signer"]["id"],
        owner_id=currentUser["id"]
    )

    for user in post["users"]:
        ReconciliationUsersModel.objects.create(
            user_id=user["id"],
            reconciliation_id=reconciliation.id
        )


    return JsonResponse(
        reconciliation.getJson()
    )
#УДАЛИТЬ СОГЛАСОВАНИЕ
@csrf_exempt
def deleteReconciliation(request):
    post = json.load(request)

    ReconciliationModel.objects.filter(
                id=post["id"],
             
            ).delete()


    return JsonResponse({
        "status" : True
    })

#УДАЛИТЬ ШАБЛОН
@csrf_exempt
def deleteTemplate(request):
    post = json.load(request)

    TemplateModel.objects.filter(
                id=post["id"],
               
            ).delete()


    return JsonResponse({
        "status" : True
    })

#СОГЛАСОВАТЬ ДОКУМЕНТ 
#КЛИК ПО КНОПКЕ ПРИМЕНИТЬ НА ЭКРАНЕ СОГЛАСУЮЩИХ
@csrf_exempt
def applyReconciliation(request):
    post = json.load(request)
    currentUser = getUserIdByToken(request)
    ReconciliationUsersModel.objects.filter(
                reconciliation_id=post["reconciliationId"],
                user_id=currentUser["id"],
            ).update(
                apply = post["apply"],
                endeed = True
            )


    return JsonResponse({
        "status" : True
    })


#ОБНОВИТЬ ФАЙЛ СОГЛАСОВАНИЯ ЕСЛИ ОТКЛОНИЛИ
@csrf_exempt
def editReconciliation(request):
    post = json.load(request)


    ReconciliationModel.objects.filter(
        id = post["reconciliationId"]
    ).update(
         file_id=post["fileId"],
    )

    ReconciliationFileModel.objects.filter(reconciliation_id =post["reconciliationId"]).delete()
    ReconciliationUsersModel.objects.filter(
                reconciliation_id=post["reconciliationId"],
            ).update(
                apply = False,
                endeed = False
            )


    return JsonResponse({
        "status" : True
    })

#СКАЧАТЬ КОММЕНТАРИИ
@csrf_exempt
def getComments(request):
    post = json.load(request)


    comments = []

    commentQS = ReconciliationCommentsModel.objects.filter(reconciliation_id=post["source"])

    for comment in commentQS:
        comments.append(comment.getJson())


    return JsonResponse(comments, safe=False)

#ПОЛУЧИТЬ СПИСОК СОГЛАСОВАНИЙ
@csrf_exempt
def getTemplates(request):

    templates = []
    currentUser = getUserIdByToken(request)
    templatesQS = TemplateModel.objects.all().order_by("-id")

    for template in templatesQS:
        t = template.getJson()
        t["canEdit"] = currentUser['id'] == t["owner"]["id"]

        templates.append(t)


    return JsonResponse(templates, safe=False)
#ОТПРАВИТЬ КОММЕНТ
@csrf_exempt
def setComment(request):
    post = json.load(request)
    currentUser = getUserIdByToken(request)
    if(post["sourceType"] == "reconciliation"):
        commentQS = ReconciliationCommentsModel.objects.create(
            reconciliation_id=post["source"],
            user_id=currentUser["id"],
            text=post["text"]
        )
    else:
        commentQS = TaskCommentsModel.objects.create(
            task_id=post["source"],
            user_id=currentUser["id"],
            text=post["text"]
        )


    return JsonResponse(commentQS.getJson())


#СОЗДАТЬ ШАБЛОН
@csrf_exempt
def createTemplates(request):
    post = json.load(request)
    # user_id = getId(request)

    currentUser = getUserIdByToken(request)
    TemplateModelQS = TemplateModel.objects.create(
        title=post["title"],
        file_id = post["file"],
        description=post["description"],
        owner_id=currentUser["id"],
    )


    return JsonResponse(TemplateModelQS.getJson())






#ЗАГРУЗКА ФАЙЛОВ
@csrf_exempt
def load(request):

    currentUser = getUserIdByToken(request)
    if (currentUser == -1):
        currentUser = {
            "id" : 7
        }
    file = FileModel.objects.create(
        fileId = request.FILES['file'].name,
        file= request.FILES['file'],
        encrypted = "encripted" in request.GET,
        owner_id = currentUser["id"]
    )

    if "reconciliation" in request.GET:
        ReconciliationFileModel.objects.filter(
            type = request.GET["type"],
            reconciliation_id = request.GET["reconciliation"]
        ).delete()
        ReconciliationFileModel.objects.create(
            type = request.GET["type"],
            file_id = file.id,
            reconciliation_id = request.GET["reconciliation"]
        )

    # myfile = request.FILES['file']
    # fs = FileSystemStorage()
    # filename = fs.save(str(file.id)+"_"+myfile.name, myfile) # saves the file to `media` folder
    # uploaded_file_url = fs.url(filename) # gets the url
    if "file" in request.FILES.keys():
        handle_uploaded_file(request.FILES['file'],str(file.id)+"_"+request.FILES['file'].name)

    return JsonResponse(
       file.getJson()
        
    )


def handle_uploaded_file(f,name):
    with open('/home/c/cc63778/dostup/public_html/uploads/'+name, 'wb') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
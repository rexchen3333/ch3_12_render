from django.http import HttpResponse
from django.utils import timezone
from django.db.models import Sum
from django.shortcuts import render
from django.forms.models import model_to_dict
from myapp.models import *

# Create your views here.
def test(request):
    return HttpResponse("Hello word!!")
def search_list(request):
    if 'cName' in request.GET:
        cName = request.GET['cName']
        print(cName)
        resultObject=students.objects.filter(cName__contains=cName)
    else:
        resultObject=students.objects.all().order_by("-cID")
    # for data in resultObject:
    #     print(model_to_dict(data))
    errormessage=""
    if not resultObject:
        errormessage="無此資料"
    return render(request,"search_list.html",locals())
def search_name(request):
    return render(request,"search_name.html")
from django.db.models import Q
from django.core.paginator import Paginator
def index(request):
    if 'site_search' in request.GET:
        site_search = request.GET["site_search"]
        site_search = site_search.strip() #去除空白
        # print(site_search)
        # 多個關鍵字
        keywords = site_search.split() #切割字元
        print(keywords)
        q_objects = Q()
        for keyword in keywords:
            q_objects.add(Q(cName__contains=keyword),Q.OR)
            q_objects.add(Q(cBirthday__contains=keyword),Q.OR)
            q_objects.add(Q(cEmail__contains=keyword),Q.OR)
            q_objects.add(Q(cPhone__contains=keyword),Q.OR)
            q_objects.add(Q(cAddr__contains=keyword),Q.OR)
        resultList= students.objects.filter(q_objects)

        # 一個關鍵字
    #     resultList = students.objects.filter(
    #         Q(cName__contains=site_search)|
    #         Q(cBirthday__contains=site_search)|
    #         Q(cEmail__contains=site_search)|
    #         Q(cPhone__contains=site_search)|
    #         Q(cAddr__contains=site_search)
    #     )
    else:
        resultList= students.objects.all().order_by('cID')
    status= True
    if not resultList:
        errormessage="無此資料"
        status=False
    data_count = len(resultList)
    # print(data_count)
    # for d in resultList:
    #     print(model_to_dict(d))
    # 分頁設定，每頁顯示3筆
    paginator = Paginator(resultList,3)
    # ?page=1
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    # print(dir(page_obj))
    return render(request,"index.html",locals())

from django.shortcuts import redirect
def post(request):
    if request.method== "POST":
        cName= request.POST["cName"]
        cSex=request.POST["cSex"]
        cBirthday=request.POST["cBirthday"]
        cEmail=request.POST["cEmail"]
        cPhone=request.POST["cPhone"]
        cAddr=request.POST["cAddr"]
        add =students(cName=cName,cSex=cSex,cBirthday=cBirthday,cEmail=cEmail,cPhone=cPhone,cAddr=cAddr)
        add.save()        
        return redirect("/index/")
    else:
        return render(request,"post.html",locals())
    
def edit(request,id):
    if request.method == "POST":
        cName= request.POST["cName"]
        cSex=request.POST["cSex"]
        cBirthday=request.POST["cBirthday"]
        cEmail=request.POST["cEmail"]
        cPhone=request.POST["cPhone"]
        cAddr=request.POST["cAddr"]
        update =students.objects.get(cID=id)
        update.cName=cName
        update.cSex=cSex 
        update.cBirthday=cBirthday 
        update.cEmail=cEmail 
        update.cPhone=cPhone 
        update.cAddr=cAddr     
        update.save()
        return redirect("/index/")
    else:
        obj_data=students.objects.get(cID=id)
        print(model_to_dict(obj_data))
        return render(request,"edit.html",locals())
def delete(request,id):
    if request.method == "POST":
        obj_data = students.objects.get(cID=id)
        obj_data.delete()
        return redirect("/index/")
    else:
        obj_data = students.objects.get(cID=id)
        return render(request,"delete.html",locals())
######################################
from django.http import JsonResponse
def getAllItems(request):
    resultObject = students.objects.all().order_by("-cID")
    # for d in resultObject:
    #     print(model_to_dict(d))
    resultList = list(resultObject.values())
    # print(resultList)
    return JsonResponse(resultList,safe=False)
    # return HttpResponse("hello")
def getItem(request,id):
    try:
        obj = students.objects.get(cID=id)
        resultDict = model_to_dict(obj)
        return JsonResponse(resultDict)
    except:
        return JsonResponse({"erroe":"Item out found"},status=404)
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt # 關閉CSRF驗證
def createItem(request):
    try:
        if request.method == "GET":
            cName = request.GET["cName"]
            cSex = request.GET["cSex"]
            cBrithday = request.GET["cBrithday"]
            cEmail = request.GET["cEmail"]
            cPhone = request.GET["cPhone"]
            cAddr = request.GET["cAddr"]
            print(f"id={id},cName={cName},cSex={cSex},cBrithday={cBrithday},cEmail={cEmail},cPhone={cPhone},cAddr={cAddr}")
            # return JsonResponse({"message":"Item created successfully"})
        elif request.method == "POST":
            cName = request.POST["cName"]
            cSex = request.POST["cSex"]
            cBrithday = request.POST["cBrithday"]
            cEmail = request.POST["cEmail"]
            cPhone = request.POST["cPhone"]
            cAddr = request.POST["cAddr"]
            print(f"id={id},cName={cName},cSex={cSex},cBrithday={cBrithday},cEmail={cEmail},cPhone={cPhone},cAddr={cAddr}")
            # return JsonResponse({"message":"Item created successfully"})
        add = students(cName=cName,cSex=cSex,cBrithday=cBrithday,cEmail=cEmail,cPhone=cPhone,cAddr=cAddr)
        add.save()
        return JsonResponse({"message":"Item created successfully"})
    except:
        return JsonResponse({"error":"Missing parameters"},status=400)
@csrf_exempt 
def updateItem(request,id):
    try:
        if request.method == "GET":
            cName = request.GET["cName"]
            cSex = request.GET["cSex"]
            cBrithday = request.GET["cBrithday"]
            cEmail = request.GET["cEmail"]
            cPhone = request.GET["cPhone"]
            cAddr = request.GET["cAddr"]
            print(f"id={id},cName={cName},cSex={cSex},cBrithday={cBrithday},cEmail={cEmail},cPhone={cPhone},cAddr={cAddr}")
            # return JsonResponse({"message":"Item created successfully"})
        elif request.method == "POST":
            cName = request.POST["cName"]
            cSex = request.POST["cSex"]
            cBrithday = request.POST["cBrithday"]
            cEmail = request.POST["cEmail"]
            cPhone = request.POST["cPhone"]
            cAddr = request.POST["cAddr"]
            print(f"id={id},cName={cName},cSex={cSex},cBrithday={cBrithday},cEmail={cEmail},cPhone={cPhone},cAddr={cAddr}")
            # return JsonResponse({"message":"Item created successfully"})
        update = students.objects.get(cID=id)
        update.cName=cName
        update.cSex=cSex
        update.cBirthday=cBrithday
        update.cEmail=cEmail
        update.cPhone=cPhone
        update.cAddr=cAddr
        return JsonResponse({"message":"Item created successfully"})
    except:
        return JsonResponse({"error":"Missing parameters"},status=400)
def deleteItem(request,id):
    try:
        delete_data = students.objects.get(cID=id)
        delete_data.delete()
        return JsonResponse({"message":"Item deleted successfully"})
    except:
        return JsonResponse({"error":"Missing parameters"},status=400)
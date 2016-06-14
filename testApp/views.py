from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from models import Employee, Record, DBRecord, Person, PersonWrapper
from django.template import loader, RequestContext
from django.core.urlresolvers import reverse
from SignAndSearch import Authenticate
from .forms import UploadFileForm
import csv

def batchSearch(request):
    form = UploadFileForm(request.POST, request.FILES)
    fileContent = csv.reader(request.FILES['linkedFile'])
    sParams = {}
    successReads = 0
    failReads = 0
    linkObj = Authenticate('bigdatafall2015@gmail.com','chandraisgr8')
    for line in fileContent:
        if len(line) != 10:
            failReads = failReads + 1
            continue
        minReq = 3
        if line[0] != '':
            sParams['firstName'] = line[0]
            minReq = minReq - 1
        if line[1] != '':
            sParams['lastName'] = line[1]
            minReq = minReq - 1
        if line[2] != '':
            sParams['email'] = line[2]
            minReq = minReq - 1
        if line[3] != '':
            sParams['school'] = line[3]
            minReq = minReq - 1
        if line[4] != '':
            sParams['company'] = line[4]
            minReq = minReq - 1
        if line[7] != '':
            minReq = minReq - 1
            country = line[7]
            if len(country) == 2:
                sParams['countryCode'] = country
            else :
                sParams['countryCode'] = 'us'
        else:
            sParams['countryCode'] = 'us'
        if line[5] != '':
            sParams['keywords'] = line[5]
            minReq = minReq - 1
        if line[6] != '':
            sParams['title'] = line[6]
            minReq = minReq - 1
        if line[8] != '':
            sParams['postalCode'] = line[8]
            minReq = minReq - 1
            if line[9] != '':
                sParams['distance'] = line[9]
            else :
                sParams['distance'] = '50'
        resp = Authenticate.performSearch(linkObj, sParams, 'localhost', 27017, 'test')
        if resp.startswith('Success'):
            successReads = successReads + 1
        else :
            failReads = failReads + 1
    message = 'The records from the uploaded file have been processed. '
    message = message + 'Success : ' + str(successReads)+' Failed : ' + str(failReads)
    msg = {'type':'I','message':message}
    context = {
        'msg':msg,}
    return render(request,'testApp/message.html', context)
        
def index1(request):
    latest_question_list = [1,2,3,4]
    template = loader.get_template('testApp/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))

def index(request):
    link = Authenticate('bigdatafall2015@gmail.com','chandraisgr8')
    return HttpResponse(Authenticate.djangoTest(link))

def filter(request):
    cVal = request.POST.get('profileId', '')
    try:
        vals = cVal.split('id')
        if len(vals) < 2:
            raise Exception('Error: Something went wrong, please try again later', 'Error')
        email = vals[0]
        profileId = vals[1]
        rec = DBRecord.objects(record__email=email)
        if rec is None:
            raise Exception('Error: Something went wrong, please try again later', 'Error')
        actualRd = None
        rd = rec[0]['record']
        reslts = rd['results']
        for p in reslts:
            print p['person']['personId']
            if p['person']['personId'] == int(profileId):
                actualRd = p
                break;
        if actualRd is None:
            raise Exception('Error: Something went wrong, please try again later', 'Error')
        DBRecord.objects(record__email=vals[0]).update(record__resultCount=1, set__record__results=[actualRd])
        msg = {'type':'I','message':'Record has been updated Successfully'}
        context = {
            'msg':msg,}
        return render(request,'testApp/message.html', context)
    except:
        msg = {'type':'E','message':'Something went wrong in updating a record, Please try again later'}
        context = {
            'msg':msg,}
        return render(request,'testApp/message.html', context)
    
def formSearch(request):
    firstName = request.POST.get('fname', 'Empty')
    lastName = request.POST.get('lname', 'Empty')
    email = request.POST.get('email', 'Empty')
    school = request.POST.get('school', 'Empty')
    title = request.POST.get('title', 'Empty')
    company = request.POST.get('company', 'Empty')
    postalCode = request.POST.get('postalCode', 'Empty')
    distance = request.POST.get('distance', 'Empty')
    countryCode = request.POST.get('country',  'Empty')
    keywords = request.POST.get('keywords', 'Empty')
    params = {'email':email, 'firstName':firstName,'lastName':lastName, 'school':school, 'countryCode':countryCode, 'keywords':keywords}
    if postalCode != '':
        params['postalCode'] = postalCode
        params['distance'] = distance
    if company != '':
        params['company'] = company
    print params
    linkObj = Authenticate('bigdatafall2015@gmail.com','chandraisgr8')
    resp = Authenticate.performSearch(linkObj, params, 'localhost', 27017, 'test')
    if resp.startswith('Success'):
        print request
        return results(request)
    else:
        if resp.startswith('Error'):
            type = 'E'
        else:
            type = 'I'
        message = resp
        msg = {'type':type, 'message':message}
        context = {
                   'msg':msg}
        return render(request, 'testApp/message.html', context)
    
def remove(request):
    email_id = request.POST.get('email', 'EMPTY')
    if email_id == 'EMPTY':
        msg = {'type':'E','message':'Please enter valid email address'}
        context = {
            'msg':msg,}
        return render(request,'testApp/message.html', context)
    res = DBRecord.objects(record__email=email_id)
    res.delete()
    msg = {'type':'I','message':'If there was a record with the entered email address, It has been removed from the database'}
    context = {
        'msg':msg,}
    return render(request,'testApp/message.html', context)
        
def retrive(request):
    employList = Employee.objects(email=request.POST['email'])
    context = {
               'employList':employList
               }
    return render(request, 'testApp/employ.html', context)
	
def employ(request):
    #link = Authenticate('bigdatafall2015@gmail.com','chandraisgr8')
    return HttpResponse('FName:{0} last Name : {1}, school : {2}'.format(request.POST.get('fname', 'EMPTY'), request.POST.get('lname', 'EMPTY'), request.POST.get('school','EMPTY')))

	
def detail(request, question_id):
    return render(request, 'testApp/readForm.html')

def results(request):
    #res = DBRecord.objects.all()
    res = DBRecord.objects.order_by('record.results.person.firstName', '-record.results.person.connectionCount')
    if res is None:
        msg = {'type':'E','message':'Currently, there are no records. Please perform Search or add few records'}
        context = {
            'msg':msg,}
        return render(request,'testApp/message.html', context)
    persons = []
    for r in res:
        res1 = r['record']
        count = res1['resultCount']
        email = res1['email']
        isMultiple = False
        if count > 1:
            isMultiple = True
        x = res1['results'][0]
        person = {'email':email, 'isMultiple':isMultiple, 'personData':x['person']}
        persons.append(person)
    context = {
               'records':persons}
    return render(request, 'testApp/results.html', context)

def update(request, email_id):
    res = DBRecord.objects(record__email=email_id)
    if res is None:
        msg = {'type':'E','message':'There seems to be some problem fetching records for the entered URL, Please try again later'}
        context = {
            'msg':msg,}
        return render(request,'testApp/message.html', context)
    persons = []
    r = res[0]
    res1 = r['record']
    count = res1['resultCount']
    email = res1['email']
    isMultiple = False
    if count > 1:
        isMultiple = True
    reslts = res1['results']
    for x in reslts:
        person = {'email':email, 'isMultiple':isMultiple, 'personData':x['person']}
        persons.append(person)
    context = {
               'records':persons}
    return render(request, 'testApp/multiple.html', context)
    
def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)

def search(request):
    return render(request, 'testApp/search.html')

def upload(request):
    return render(request, 'testApp/upload.html')

def delete(request):
    return render(request, 'testApp/delete.html')

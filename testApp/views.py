from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from models import Employee, Record, CSPerson, DBRecord, Person, PersonWrapper
from django.template import loader, RequestContext
from django.core.urlresolvers import reverse
from SignAndSearch import Authenticate
from django import forms
from pymongo import MongoClient
from .forms import UploadFileForm
import csv
import json
import logging
from bson import Binary, Code
from bson.json_util import dumps

logging.basicConfig(filename='log_file.txt',level=logging.INFO)

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
    print "Inside form search ... "
    firstName = request.POST.get('fname', 'Empty')
    lastName = request.POST.get('lname', 'Empty')
    email = request.POST.get('email', 'Empty')
    school = request.POST.get('school', 'Empty')
    distance = request.POST.get('distance', 'Empty')
    countryCode = request.POST.get('country',  'Empty')
    keywords = request.POST.get('keywords', 'Empty')
    params = {'email':email, 'firstName':firstName,'lastName':lastName, 'school':school, 'countryCode':countryCode, 'keywords':keywords}
    
    print "Searching : "+params.__str__() 
    # Authenticating a linkedin profile to start with.
    linkObj = Authenticate('bigdatafall2015@gmail.com','chandraisgr8')
    print "Linkedin Object :: "+linkObj.__str__()
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
    

def searchUnderGrad(request): ## Added By, Bikramjit edu.bmandal@gmail.com
    print "Inside grad search ... "
    myclient = MongoClient()
    db = myclient.test
    firstName = request.POST.get('fname', 'Empty')
    lastName = request.POST.get('lname', 'Empty')
    personemail = request.POST.get('email','Empty')
    #print "Values received from request : "+firstName.__str__()+", "+lastName.__str__()+", "+email.__str__()
    #resp = Authenticate.performSearch(linkObj, params, 'localhost', 27017, 'test')
    #resp = Authenticate.filterResult(linkObj, filterParams, 'localhost', 27017, 'test')
    # results = Lesson.objects(__raw__={'subject.subject_name': 'Math'})
    #entries = db.d_b_record.find({'record.email':{'$eq':personemail}})#(__raw__={'person.fmt_location':'Taiwan'})
    '''
    Below we match the email in the records and fetch the 
    person IDs that are related to the given email.

    We need to filter the output further to 
    see if it has the college name present.

    Also other keywords to search for.

    '''
    entries = db.d_b_record.aggregate(
        [
            {
                "$match": {   "record.email": personemail }# Text Search for College Name and Country Name}
            },
            {
                "$group": {   "_id": "$record.results.person.personId"  }
            }
        ])
    entries_list = [] # list, will store all details.
    ent_list = list(entries)


    """
    Helps to convert the Cursor function output to
    JSON readable output using BSON.JSON_UTIL library.
    """
    parsed_bson = dumps(ent_list[0]) 

    '''
    Helps to read the json from the output of the 
    above statement.

    Will now use this method to read the details from the outputs 
    that can be presented in the output.
    '''
    parsed_json = json.loads(parsed_bson.__str__())
    print "\n Length of parsed_bson : "+len(parsed_json).__str__()
    #print "\n\n IDs : "+parsed_json['_id'][0].__str__()+", "+parsed_json['_id'][1].__str__()

    print "\n PARSED_JSON : "+parsed_json.__str__()+" \n"
    for e in parsed_json['_id']: # for each of the entries in parsed_json we send add the values to list.

        #print "value : "+e.__str__()
    
        persons_filter = DBRecord.objects(record__results__person__personId=e.__str__())
        #print "Persons are ... \n"
        '''
        Also complete objects can be sent.
        '''
        for p in persons_filter:
            #print " "+p.record.results.__str__()
            #print " The IDs are :\n"
            for p1 in p.record.results:
                print p1.person.personId.__str__()+", "+p1.person.firstName.__str__()+", "+p1.person.lastName.__str__()+", "+p1.person.fmt_industry.__str__()
                nperson = { 'personId':p1.person.personId, 'personPhoto':p1.person.profilePhoto.profilePhoto.media_picture_link_100,'firstName':p1.person.firstName, 'lastName':p1.person.lastName, 'fmt_industry':p1.person.fmt_industry, 'fmt_location':p1.person.fmt_location, 'workinfo':p1.person.fmt_headline }
            entries_list.append(nperson) # appending the details of one person to the list.    
    
    # each JSON can be 
    print "Entries _ list ::"+entries_list.__str__()

    ctx = { 'fname':firstName, 'lname':lastName, 'personemail':personemail, 'entries':entries_list, 'recordInstances':persons_filter }
    context=ctx
    print "\n Entries appended to list and rendered to searchGrad.html "
    return render(request,'testApp/searchGrad.html',context)
    
def mergedUpdate(request):
    context = RequestContext(request)
    print "<<<<< INSIDE mergeUpdate >>>>> \n"
    myclient = MongoClient()
    db = myclient.test
    print "\n\n\n Inside mergedUpdate \n\n"
    entries_list = []
    return_list = []
    #return_list = []
    if request.method=='GET':
        
        entries_list = request.GET['selectedIDs[]']
        
    if entries_list:
        # fill the return list with merged results.
        # also, merge the data in the database.
        print "\n\n\n\nmergedUpdate returns \n"
        print "list we got : "

        '''
        We use json.loads(string) method to convert the GET request list 
        to a parseable JSON. Now, we can iterate over them using for loop.
        (bikramjit, edu.bmandal@gmail.com)
        '''
        parsed_list = json.loads(entries_list.__str__())
        #print "parsed_list : "+parsed_list.__str__()
        new_parsed_list = json.dumps(parsed_list)
        #print "new parsed_list :"+json.loads(new_parsed_list).__str__()
        final_parsed_list = json.loads(new_parsed_list)
        #print "final_parsed_list : "+final_parsed_list.__str__()
        merge_list = []

        person_filter = DBRecord.objects(record__results__person__personId=final_parsed_list[0].__str__())
        nperson = { 'personId':final_parsed_list[0], 
                    'personPhoto':person_filter[0].record.results[0].person.profilePhoto.profilePhoto.media_picture_link_100,
                    'firstName':person_filter[0].record.results[0].person.firstName, 
                    'lastName':person_filter[0].record.results[0].person.lastName, 
                    'fmt_industry':[], 
                    'fmt_location':[], 
                    'workinfo':[] 
                    }

        print "Intial nperson JSOn : "+nperson.__str__()
        
        
        nperson_bson = json.dumps(nperson)
        print "nperson_bson : "+nperson_bson
        nperson_json = json.loads(nperson_bson)
        print "nperson_json : "+nperson_json.__str__()


        for e in final_parsed_list: # printing to check if values received are right.
            print e.__str__()
            
            final_list = db.d_b_record.aggregate([{"$unwind": "$record.results"},{"$group": { '_id': "$record.results.person.personId", 'headline':{"$addToSet":"$record.results.person.fmt_headline"}, 'location':{"$addToSet":"$record.results.person.fmt_location"}, 'industry':{"$addToSet":"$record.results.person.fmt_industry"}}},{'$match': {'_id': {'$eq':int(e)}}}])
            
            print "final_list : "+str(final_list)
            filter_list = list(final_list)
            print "filter_list : "+str(filter_list)
            parsed_bson = dumps(filter_list[0])
            print "parsed_bson : "+str(parsed_bson)
            parsed_json = json.loads(parsed_bson, encoding='ascii')
            #print "Merge Update JSON : \n"+parsed_json.__str__()
            print "final_list > industry :"+parsed_json['industry'][0]
            for i in parsed_json['industry']:
                print ";;"+i
            nperson['fmt_industry'].append(parsed_json['industry'])
            nperson['fmt_location'].append(parsed_json['location'])
            nperson['workinfo'].append(parsed_json['headline'])

        print "Final nperson JSON : "+nperson.__str__()

            
            
        return_list.append(nperson) #this list will be returned to website.    
        print "RETURN LIST : "+str(return_list)
        ctx = { 'entries':return_list }
        context=ctx
        print "\n Entries appended to list and rendered to searchGrad.html "
        
    else:
        print "\n\n\n\nmergedupdate not working \n"

        #render page with new results.
    #return HttpResponse(context)
    return render(request,'testApp/searchGrad.html',context)



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

def results(request): #Accessing mongoengine to get data.
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

def searchgrad(request):
    return render(request, 'testApp/grad-search.html')

def upload(request):
    return render(request, 'testApp/upload.html')

def delete(request):
    return render(request, 'testApp/delete.html')

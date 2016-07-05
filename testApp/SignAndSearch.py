import cookielib
import os
import urllib
import urllib2
import re
import sys
import json
import pymongo
import datetime
from models import Employee, Record, DBRecord, Person, PersonWrapper
from bs4 import BeautifulSoup
from bs4 import Comment
import logging

logging.basicConfig(filename='log_file.txt',level=logging.INFO)
username = "bigdatafall2015@gmail.com"
password = "chandraisgr8"
dbHost = 'localhost' #found from the hostname() command in mongo.
dbPort = 27017
dbName = 'test'
dbCollection = 'd_b_record'
url1 = 'https://www.linkedin.com/'
linkHome = 'http://www.linkedin.com/nhome'
lSrchTitle = 'Search | LinkedIn'
contentKey = 'content'
gReqParamsKey = 'global_requestParams'
pageKey = 'page'
unifiedSearchKey = 'voltron_unified_search_json'
searchKey = 'search'
advSearchFormKey = 'advancedSearchForm'
searchFieldsKey = 'searchFields'
baseDataKey = 'baseData' #for result count
resultCountKey = 'resultCount'
resultPaginationKey = 'resultPagination'
resultsKey = 'results'
recordKey = 'record'
emailKey ='email'
searchParamsKey = 'searchParams'
userUpdateKey = 'isUserUpdated'
rsltCountKey = 'resultCount'
dateCreateKey = 'dateCreated'
dateUpdateKey = 'dateUpdated'
createByKey = 'createdBy'
updateByKey = 'updatedBy'
emailSentKey = 'isEmailSent'
emailSentCountKey = 'emailCount'
personKey = 'person'
systemVal = 'System'
searchURL = "https://www.linkedin.com/vsearch/p?firstName=Bala&lastName=Yadav&openAdvancedForm=true&locationType=Y&rsid=4764583901457977599432&orig=MDYS"

#person related keys
authTokenKey = 'authToken'
authTypeKey = 'authType'
connecCountKey = 'connectionCount'
localeKey = 'displayLocale'
encryptedIdKey = 'encryptedId'
encryptResltKey = 'encryptedResultId'
firstNameKey = 'firstName'
headlineKey = 'fmt_headline'
curIndustryKey = 'fmt_industry'
curLocKey = 'fmt_location'
prflNameKey = 'fmt_name'
personIdKey = 'personId'
bookmarkKey = 'isBookmarked'
connectEnableKey = 'isConnectedEnabled'
contactKey = 'isContact'
headlessKey = 'isHeadless'
nameMatchKey = 'isNameMatch'
lastNameKey = 'lastName'
searchLink1Key = 'linkAuto_voltron_people_search_1'
searchLink2Key = 'link_voltron_people_search_5'
profileLink1Key = 'link_nprofile_view_3'
profileLink2Key = 'link_nprofile_view_4'
resultIndexKey = 'resultIndex'
logoBaseKey = 'logo_result_base'
isProfilePic = 'isProfilePic'
profilePhoto = 'profilePhoto'
genericGhostImageKey = 'genericGhostImage'
mediaPicDefKey = 'media_picture_link'
mediaPic100Key = 'media_picture_link_100'
mediaPic200Key = 'media_picture_link_200'
mediaPic400Key = 'media_picture_link_400'
personListKey = 'personList'
emptyString = 'EMPTY'
#general strings
equalTo = '='
amper = '&'
spaceV = '%20'
amperV = '%26'
#URL forming constants
searchBaseURL = 'https://www.linkedin.com/vsearch/p?{0}openAdvancedForm=true&locationType=Y&rsid=4764583901459185729672&orig=ADVS'
paramBaseURL = 'https://www.linkedin.com/vsearch/p?{0}openAdvancedForm=true&{1}{2}{3}rsid=4764583901459312896588&orig=MDYS'
titleScopeParam = 'titleScope=CP&'
companyScopeParam = 'companyScope=CP&'
locationNoSelectParam = 'locationType=Y&'
locationSelectParam = 'locationType=I&'

cookie_filename = "parser.cookies.txt"

class Authenticate(object):
    trialCount = 0;
    def __init__(self, login, password):
        """ Start up... """
        self.login = login
        self.password = password
        # Simulate browser with cookies enabled
        self.cj = cookielib.MozillaCookieJar(cookie_filename)
        if os.access(cookie_filename, os.F_OK):
            self.cj.load()
        self.opener = urllib2.build_opener(
            urllib2.HTTPRedirectHandler(),
            urllib2.HTTPHandler(debuglevel=0),
            urllib2.HTTPSHandler(debuglevel=0),
            urllib2.HTTPCookieProcessor(self.cj)
        )
        self.opener.addheaders = [
            ('User-agent', ('Mozilla/4.0 (compatible; MSIE 6.0; '
                           'Windows NT 5.2; .NET CLR 1.1.4322)'))
        ]
        
    
    def performCSSearch(self, searchParams, dbHost, dbPort, dbName):
        """ Performs search and Saves the information gathered into DB. This method almost performs everything this class is created for """
        try:
            #self.login = login
            #self.password = password
            # Simulate browser with cookies enabled
            self.cj = cookielib.MozillaCookieJar(cookie_filename)
            if os.access(cookie_filename, os.F_OK):
                self.cj.load()
            self.opener = urllib2.build_opener(
                urllib2.HTTPRedirectHandler(),
                urllib2.HTTPHandler(debuglevel=0),
                urllib2.HTTPSHandler(debuglevel=0),
                urllib2.HTTPCookieProcessor(self.cj)
            )
            self.opener.addheaders = [
                ('User-agent', ('Mozilla/4.0 (compatible; MSIE 6.0; '
                               'Windows NT 5.2; .NET CLR 1.1.4322)'))
            ]
            self.checkLogin(url1)
            fName = searchParams['firstName']
            mailId = searchParams['email']
            if fName == 'EMPTY' or mailId == 'EMPTY':
                raise Exception('Info: Search has to be performed from Search page only, Please try again', 'Info')
            fSrchURL = self.formSearchURL(searchParams)
            linkedJSON = self.loadSearch(fSrchURL, fName)
            self.formCSRecord(linkedJSON, dbHost, dbPort, dbName)
            return 'Success'
        except Exception as e:
            x,y = e.args
            return x
        
    def performSearch(self, searchParams, dbHost, dbPort, dbName):
        """ Performs search and Saves the information gathered into DB. This method almost performs everything this class is created for """
        print "inside Perform Search ... "
        try:
            #self.login = login
            #self.password = password
            # Simulate browser with cookies enabled
            self.cj = cookielib.MozillaCookieJar(cookie_filename)
            if os.access(cookie_filename, os.F_OK):
                self.cj.load()
            self.opener = urllib2.build_opener(
                urllib2.HTTPRedirectHandler(),
                urllib2.HTTPHandler(debuglevel=0),
                urllib2.HTTPSHandler(debuglevel=0),
                urllib2.HTTPCookieProcessor(self.cj)
            )
            self.opener.addheaders = [
                ('User-agent', ('Mozilla/4.0 (compatible; MSIE 6.0; '
                               'Windows NT 5.2; .NET CLR 1.1.4322)'))
            ]
            self.checkLogin(url1)
            fName = searchParams['firstName']
            mailId = searchParams['email']
            if fName == 'EMPTY' or mailId == 'EMPTY':
                raise Exception('Info: Search has to be performed from Search page only, Please try again', 'Info')
            fSrchURL = self.formSearchURL(searchParams)
            linkedJSON = self.loadSearch(fSrchURL, fName)
            recordJSON = self.formTrimmedJSON(linkedJSON)
            dbRecord = self.formDBRecord(recordJSON, mailId)
            client = self.connect2DB(dbHost, dbPort)
            print "Client details : "+client.__str__()
            self.store2DB(dbRecord, mailId, client)
            return 'Success'
        except Exception as e:
            x,y = e.args
            return x
     
    def filterResult(self, filterParams, dbHost, dbPort, dbName):
        """Performs a filter based on the filter parameters """
        print "Inside Filter Result view ..."
        try:
            self.cj = cookielib.MozillaCookieJar(cookie_filename)
            if os.access(cookie_filename, os.F_OK):
                self.cj.load()
            self.opener = urllib2.build_opener(
                urllib2.HTTPRedirectHandler(),
                urllib2.HTTPHandler(debuglevel=0),
                urllib2.HTTPSHandler(debuglevel=0),
                urllib2.HTTPCookieProcessor(self.cj)
            )
            self.opener.addheaders = [
                ('User-agent', ('Mozilla/4.0 (compatible; MSIE 6.0; '
                               'Windows NT 5.2; .NET CLR 1.1.4322)'))
            ]
            self.checkLogin(url1)

            ## start here ##
            print " Data So Far : \n"+Person.objects.all()
            return 'Success'

        except Exception as e:
            x,y = e.args
            return x       
        
    def connect2DB(self, dbHost, dbPort):
        """ This definition connects to db using the details provided and returns the client"""
        print "inside connect2DB .. "
        try:
            client = pymongo.MongoClient(dbHost, dbPort)
            return client
        except pymongo.errors.ServerSelectionTimeoutError as err:
            raise Exception('Error: There is some problem connecting to Database, Please check connection and retry again, Note: data is not cached', 'Error')
        
    def saveToDB(self, client, json):
        """ Persists the JSON to the db using the client """
        db = client.linkedinTest
        db.users.save(json)
        
    def findEntryInDB(self, db, email):
        """ Returns true if it finds an entry with the email provided """
        entries = db.d_b_record.find({'record.email':{'$eq':email}})
        if entries.count() is 0:
            return False
        return True
    
    def djangoTest(self):
        try:
            val = 24;
            c = val/0
            return 'bala'
        except:
            return 'SUCCESS'
        
    def store2DB(self, json2Store, email, dbClient):
        """ Persists the document to the DB using the dbClient, if the record is already present, it simply replaces the document """
        #db = dbClient.linkedinTest
        print "Inside store2DB ... "
        db = dbClient.test
        print "DB client is : "+db.__str__()

        if self.findEntryInDB(db, email):
            db.d_b_record.replace_one({'record.email':email},json2Store)
        else:
            self.insertRecord(json2Store, db)
    
    def storeCSRecord(self, json2Store, pId, dbClient):
        db = dbClient.test
        entries = db.c_s_person.find({'person.personId':{'$eq':pId}})
        if entries.count is 0:
            db.c_s_person.save(json2Store)
        else:
            db.c_s_person.replace_one({'person.personId':pId}, json2Store)
        
    
    def insertRecord(self, record, db):
        """ Simple Insert into DB """
        print "saving record : "+record.__str__()
        db.d_b_record.save(record)
        
        
    def readSearchParams(self):
        """ Incase of UI issues, this method reads the search params and returns the JSON with search params """
        mailId = raw_input("Enter email ")
        firstName = raw_input('Enter First Name* ')
        lastName = raw_input('Enter Last Name ')
        school = raw_input('School ')
        title = raw_input('title ')
        params = {emailKey:mailId, 'firstName':firstName,'lastName':lastName, 'school':school, 'title':title}
        pJSON = json.dumps(params)
        return json.loads(pJSON) 
    
    def formSearchURL(self, params): #Here the parameters are converted to the URL.
        """ Creates the search url using the params """
        if params is None:
            return url1
        paramString = ''
        pKeys = params.keys() #getting the parameters.
        for key in pKeys:       # for each parameter, check
            if key == 'email':
                continue
            val = params[key]
            if val is None or val == '':
                continue
            val = val.replace(' ',spaceV) #replace spaces with %20, for making URLs ahead
            val = val.replace(amper, amperV) # replace ampersands with %26, for making URLs ahead
            paramString = paramString + key + equalTo + val + amper #making the complete URL for the profile
        tX = ''
        cX = ''
        if 'title' in pKeys:
            tX = titleScopeParam #this is as per the variables in a linkedIn URL
        if 'company' in pKeys:
            cX = companyScopeParam # as per variables in the linkedIn URL
        if 'postalCode' in pKeys:
            lX = locationSelectParam # as per variable in the linkedIn URL
        else:
            lX = locationNoSelectParam
        srchURL = paramBaseURL.format(paramString, tX, cX, lX) 
        # paramBaseURL is defined at the top, the {0}, {1} etc. positions are filled with the respictive indexed parameters
        return srchURL
    
    def checkLogin(self, homeUrl):
        """ checks if the user has already logged in into Linkedin """
        homepage = self.loadPage(homeUrl)
        homeSoup = BeautifulSoup(homepage)
        if homeSoup.find('form', 'login-form') is not None:
            self.loginPage()
            self.confirmLogin(homeUrl)
            
    def confirmLogin(self, homeUrl):
        """ Confirms if the user has already logged in, raises an exception if there is any issue with Credentials """
        homepage = self.loadPage(homeUrl)
        homeSoup = BeautifulSoup(homepage)
        if homeSoup.find('form', {'class':'login-form'}) is not None:
            raise Exception('Error: There is some problem signing into LinkedIn, Please check Credentials', 'Error')
             
    def loadPage(self, url, data=None):
        """
        Utility function to load HTML from URLs for us with hack to continue despite 404
        """
        try:
            self.trialCount = self.trialCount+1;
            if data is not None:
                response = self.opener.open(url, data)
            else:
                response = self.opener.open(url)
            self.trialCount = 0    
            return ''.join(response.readlines())
        except:
            # If URL doesn't load for ANY reason, try again for 5 times...
            # Quick and dirty solution for 404 returns because of network problems
            # after 5 trials, the program will terminate
            if self.trialCount < 5:
                #print 'There is some problem loading the page, might be a network issue or Linkedin might be down. Retrying again.'
                return self.loadPage(url, data)
            else:
                errMsg = 'There is some problem loading the page - URL: {0}'.format(url)
                sys.exit(errMsg)

    def loginPage(self, homeURL='https://www.linkedin.com/', loginURL='https://www.linkedin.com/uas/login-submit'):
        """
        Handle login. This should populate our cookie jar.
        """
        html = self.loadPage(homeURL)
        soup = BeautifulSoup(html)
        csrf = soup.find(id="loginCsrfParam-login")['value']        

        login_data = urllib.urlencode({
            'session_key': self.login,
            'session_password': self.password,
            'loginCsrfParam': csrf,
        })
        print "Login Now Processing"
        html = self.loadPage(loginURL, login_data)
        return

    def loadTitle(self, url=linkHome):
        """
        Simple function to test if the correct page has been loaded, by checking the title; This assumes that every page loaded has a title element.
        """
        html = self.loadPage(url)
        soup = BeautifulSoup(html)
        title = soup.find('title')
        if title is None:
            return None
        return title.string
    
    def printJSON(self, rJSON):
        keys = rJSON.keys()
        for key in keys:
            print key +' = '+rJSON[key]
        
    def printAdvSearchFields(self, searchFields):
        if searchFields is None:
            return
        for field in searchFields:
            if 'value' in field.keys():
                print field['labelName']+' : '+field['value']   
    
                  
    def loadSearch(self, url, firstName='results'):
        """
        Loads the search page using the url provided and returns raw search results
        """
        print " inside loadSearch .."
        sPage = self.loadPage(url)
        spContent = BeautifulSoup(sPage)
        #title = spContent.find('title')
        #if title is not None:
            #if title.string is not lSrchTitle:
                #sys.exit('There is some problem with url provided, it does not correspond to Linkedin Search')
        comments = spContent.findAll(text=lambda text:isinstance(text, Comment))
        cLen = len(comments)
        if cLen > 0 and cLen > 11:
            comment = comments[11]
        if comment is None:
            for cmnt in comments:
                if firstName in cmnt:
                    comment = cmnt
        return comment
                
    def formFullJSON(self, srchResult):
        """
        This is full JSON method, i.e. it forms the JSON with extensive information including all possible (or public) information. This increases the size of the document considerably
        """
        logging.info('::::::::::: JSON from the linkedIn URl ::::::::::::')
        
        if srchResult is None:
            sys.exit('There is some problem with loading search page and search results')
        rawResults = re.sub('\\\\u002d1', '\"\"', srchResult)
        try:
            rawJSON = json.loads(rawResults)
            fContent = rawJSON[contentKey]
            globalReqParams = fContent[gReqParamsKey]
            #below line is just to print request params, we can liberally remove /comment below line
            #self.printJSON(globalReqParams)
            fPageRes = fContent[pageKey]
            unifiedSearch = fPageRes[unifiedSearchKey]
            searchRes = unifiedSearch[searchKey]
            resultCount = searchRes['formattedResultCount']
            resultNo = int(resultCount)
            if resultNo == 0:
                print 'There are no matching results for the entered query'
                sys.exit('There are no matching results for the entered query')
            advSearchParams = searchRes[advSearchFormKey]
            baseData = searchRes[baseDataKey]
            resultCount = baseData[resultCountKey]
            print 'Total no of results matched your query params '+resultCount
            searchFields = advSearchParams[searchFieldsKey]
            #below line is just to print request params, we can liberally remove /comment below line
            #self.printAdvSearchFields(searchFields)
            results = searchRes[resultsKey]
            recObj = {recordKey : {gReqParamsKey:globalReqParams,advSearchFormKey:advSearchParams,baseDataKey:baseData,resultsKey:results}}
             # trying to send the value of recObj to the logging file.
            convertedRec = json.dumps(recObj)
            recObjJSON = json.loads(convertedRec) # loading the dump
            print json.dumps(recObjJSON, indent=4)
        except:
            sys.exit('There seems to be a problem with JSON, Might have occured if there is a change at LinkedIn Result structure or naming')
            
    def formTrimmedJSON(self, srchResult): ## The function being used primarily.
        """ Latest: forms the JSON with only general and mostly required information avoiding the redundant and actions information. """
        #logging.info(srchResult)
        if srchResult is None:
            raise Exception('Info: Either the query has not returned any results or there is some problem with linkedIn search', 'Info')
        rawResults = re.sub('\\\\u002d1', '\"\"', srchResult)
        try:
            rawJSON = json.loads(rawResults)
            fContent = rawJSON[contentKey]
            globalReqParams = fContent[gReqParamsKey]
            fPageRes = fContent[pageKey]
            unifiedSearch = fPageRes[unifiedSearchKey]
            searchRes = unifiedSearch[searchKey]
            resultCount = searchRes['formattedResultCount']
            resultNo = int(resultCount)
            if resultNo == 0:
                raise Exception('Info: There are no matching records for the query', 'Info')
            baseData = searchRes[baseDataKey]
            resultCount = baseData[resultCountKey]
            results = searchRes[resultsKey]
            allPersons = []
            for reslt in results:
                personObj = reslt[personKey]
                frmtedPerson = self.extractPerson(personObj)
                if frmtedPerson is not None:
                    allPersons.append(frmtedPerson)
            recObj = {recordKey : {gReqParamsKey:globalReqParams, resultsKey:allPersons, resultCountKey:resultCount}}
            return recObj
        except:
            raise Exception('Error: There seems to be some problem with either the query or response JSON. Please note this might occur, if LinkedIn does not respond appropriately', 'Error')
    
    def formCSRecord(self, srchResult, dbHost, dbPort, dbName):
        if srchResult is None:
            raise Exception('Info: Either the query has not returned any results or there is some problem with linkedIn search', 'Info')
        rawResults = re.sub('\\\\u002d1', '\"\"', srchResult)
        try:
            rawJSON = json.loads(rawResults)
            fContent = rawJSON[contentKey]
            globalReqParams = fContent[gReqParamsKey]
            fPageRes = fContent[pageKey]
            unifiedSearch = fPageRes[unifiedSearchKey]
            searchRes = unifiedSearch[searchKey]
            resultCount = searchRes['formattedResultCount']
            resultNo = int(resultCount)
            if resultNo == 0:
                raise Exception('Info: There are no matching records for the query', 'Info')
            baseData = searchRes[baseDataKey]
            resultCount = baseData[resultCountKey]
            results = searchRes[resultsKey]
            allPersons = []
            for reslt in results:
                personObj = reslt[personKey]
                frmtedPerson = self.extractPerson(personObj)
                pId = frmtedPerson['personId']
                if frmtedPerson is not None:
                    client = self.connect2DB(dbHost, dbPort)
                    self.storeCSRecord(dbRecord, frmtedPerson, pId, client)
        except:
            raise Exception('Error: There seems to be some problem with either the query or response JSON. Please note this might occur, if LinkedIn does not respond appropriately', 'Error')

               
    def extractPerson(self, personObj):
        """ Converts the person obj to required format """
        if personObj is None:
            print 'Person Object is None - Returning None'
            return None;
        try:
            keys = personObj.keys()
            
            authToken = emptyString
            if authTokenKey in keys:
                authToken = personObj[authTokenKey]
                
            authType = emptyString
            if authTypeKey in keys:
                authType = personObj[authTypeKey]
                
            connectCount = 0;
            if connecCountKey in keys:
                connectCount = personObj[connecCountKey]
                
            disLocale = emptyString
            if localeKey in keys:
                disLocale = personObj[localeKey]
                
            firstName = emptyString  
            if firstNameKey in keys:
                firstName = personObj[firstNameKey]
                
            lastName = emptyString
            if lastNameKey in keys:
                lastName = personObj[lastNameKey]
                
            curHeadLine = emptyString
            if headlineKey in keys:
                curHeadLine = personObj[headlineKey]
                
            curIndustry = emptyString
            if curIndustryKey in keys:
                curIndustry = personObj[curIndustryKey]
                
            curLocation = emptyString
            if curLocKey in keys:
                curLocation = personObj[curLocKey]
            
            prflName = emptyString
            if prflNameKey in keys:
                prflName = personObj[prflNameKey]
            
            profileId = 0
            if 'id' in keys:
                profileId = personObj['id']
            
            isBookmark = False 
            if bookmarkKey in keys:
                isBookmark = personObj[bookmarkKey]
                
            isConnectEnabled = False
            if connectEnableKey in keys:
                isConnectEnabled = personObj[connectEnableKey]
                
            isContact = False    
            if contactKey in keys:
                isContact = personObj[contactKey]
                
            isHeadless = False
            if headlessKey in keys:
                isHeadless = personObj[headlessKey]
                
            isNameMatched = False
            if nameMatchKey in keys:
                isNameMatched = personObj[nameMatchKey]
                
            searchLink1 = emptyString
            if searchLink1Key in keys:
                searchLink1 = personObj[searchLink1Key]
                
            searchLink2 = emptyString
            if searchLink2Key in keys:
                searchLink2 = personObj[searchLink2Key]
                
            profileLink1 = emptyString
            if profileLink1Key in keys:
                profileLink1 = personObj[profileLink1Key]
                
            profileLink2 = emptyString
            if profileLink2Key in keys:
                profileLink2 = personObj[profileLink2Key]
                
            logoBasedInfo = personObj[logoBaseKey]
            ghostImage = logoBasedInfo[genericGhostImageKey]
            imageKeys = logoBasedInfo.keys()
            if mediaPic100Key in imageKeys:
                isPicPresent = True
                photo100Pix = logoBasedInfo[mediaPic100Key]
                photo200Pix = logoBasedInfo[mediaPic200Key]
                photo400Pix = logoBasedInfo[mediaPic400Key]
                defPhoto = logoBasedInfo[mediaPicDefKey]
                profilePic = {profilePhoto:{genericGhostImageKey:ghostImage, mediaPicDefKey:defPhoto, mediaPic100Key:photo100Pix, mediaPic200Key:photo200Pix, mediaPic400Key:photo400Pix}}
            else:
                isPicPresent = False
                profilePic = {profilePhoto:{genericGhostImageKey:ghostImage}}
            personFormed = {personKey:{authTokenKey:authToken, authTypeKey:authType, connecCountKey:connectCount, localeKey:disLocale, firstNameKey:firstName, lastNameKey:lastName, headlineKey:curHeadLine, curIndustryKey:curIndustry, curLocKey:curLocation, prflNameKey:prflName, personIdKey:profileId, bookmarkKey:isBookmark, connectEnableKey:isConnectEnabled, contactKey:isContact, headlessKey:isHeadless, nameMatchKey:isNameMatched, searchLink1Key:searchLink1, searchLink2Key:searchLink2, profileLink1Key:profileLink1, profileLink2Key:profileLink2, isProfilePic:isPicPresent, logoBaseKey:logoBasedInfo, profilePhoto:profilePic}}
            return personFormed
        except Exception as e:
            raise Exception('Error: There is some problem forming Person record from the information provided', 'Error')    
            
    def formDBRecord(self, recordJSON, email):
        """ Forms the DB record which is further saved into DB, this will be the final document structure which gets stored in DB"""
        try:
            record = recordJSON[recordKey]
            searchParams = record[gReqParamsKey]
            resultCount = record[resultCountKey]
            result = record[resultsKey]
            utcD = datetime.datetime.utcnow()
            utcDate = datetime.datetime.isoformat(utcD)
            dbRecord = {recordKey : {emailKey:email, searchParamsKey:searchParams, userUpdateKey:False, resultCountKey:resultCount, resultsKey:result, dateCreateKey:utcDate, dateUpdateKey:utcDate, createByKey:systemVal, updateByKey:systemVal, emailSentKey:False, emailSentCountKey:0}}
            return dbRecord
        except:
            raise Exception('Error : There is some problem with forming the record to store, might have happened because of change in LinkedIn JSOn Structure. Contact Administrator to verify formDBRecord definition', 'Error')

#linkedInTool = Authenticate(username, password)
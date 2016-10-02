import json
import requests
from textblob import TextBlob

class QueryDeployer(object):

	def parse(self,text,type) :
    
	    wiki = TextBlob(text)
		##    wiki = TextBlob("how much balance do I have right now?")
		##    wiki = TextBlob("Please check balance in my account.")
		##    wiki = TextBlob("Please check myaccount balance.")

	    print(wiki.tags)

	    verbs = list()
	    nouns = list()
	    digits = list()
	    
	    for word,tag in wiki.tags:
	        if tag == 'VB':
	            verbs.append(word.lemmatize())
	        if tag == 'NN':
	            nouns.append(word.lemmatize())
	        if tag == 'CD':
	            digits.append(word.lemmatize())

	    print("verbs are :",verbs)
	    print("nouns are : " ,nouns)
	    print("digits are : ", digits)

	    if type == 2 :
	        if "89df" in digits:
	            return "match"
	        else:
	            return "not match"
	        
	    
	    if 'check' in verbs:
	        if 'account balance' in nouns:
	            return "account check";
	        if 'balance' in nouns:
	            return "account check";

	    if 'how' in wiki.words and 'balance' in nouns:
	        return "account check";
	        
	    if 'account' in nouns and 'money' in nouns and 'how' in wiki.words:
	        return "account check";

	    if 'transaction' in nouns and 'what' in wiki.words:
	        return "transaction check";
	    return "Error";

	def consumeGETRequestSync(self):
		data = '{"query":{"bool":{"must":[{"text":{"record.document":"SOME_JOURNAL"}},{"text":{"record.articleTitle":"farmers"}}],"must_not":[],"should":[]}},"from":0,"size":50,"sort":[],"facets":{}}'
		url = 'http://api.reimaginebanking.com/accounts/57f01c50267ebde464c489df/purchases?key=79b678ef3c6bd431c43a335a2b19de15'
		headers = {"Accept": "application/json"}
		# call get service with headers and params
		response = requests.get(url,data = data)
		## print ("code:",str(response.status_code))
		## print ("******************")
		## print ("headers:", str(response.headers))
		## print ("******************")
		response_data = str(response.text);
		#print ("content:", response_data)
		json_data = json.loads(response_data)
		print (self.getMerchantName(json_data[0]["merchant_id"]))
		print (json_data[0]["description"])
		print (json_data[0]["amount"])
		return "Your last transaction was : " + "Merchant - " + self.getMerchantName(json_data[0]["merchant_id"]) + " Description - " + json_data[0]["description"] + " Amount - " + str(json_data[0]["amount"]);

	def accountCheck(self):
		data = '{"query":{"bool":{"must":[{"text":{"record.document":"SOME_JOURNAL"}},{"text":{"record.articleTitle":"farmers"}}],"must_not":[],"should":[]}},"from":0,"size":50,"sort":[],"facets":{}}'
		url = 'http://api.reimaginebanking.com/customers/57f019d9267ebde464c489dd/accounts?key=79b678ef3c6bd431c43a335a2b19de15'
		headers = {"Accept": "application/json"}
		# call get service with headers and params
		response = requests.get(url,data = data)
		## print ("code:",str(response.status_code))
		## print ("******************")
		## print ("headers:", str(response.headers))
		## print ("******************")
		response_data = str(response.text);

		json_data = json.loads(response_data)
		return " You have " + str(json_data[0]["balance"]) + " amount in your account";
    

	def getMerchantName(self,id) :
		data = '{"query":{"bool":{"must":[{"text":{"record.document":"SOME_JOURNAL"}},{"text":{"record.articleTitle":"farmers"}}],"must_not":[],"should":[]}},"from":0,"size":50,"sort":[],"facets":{}}'
		url = 'http://api.reimaginebanking.com/merchants/'+ id +'?key=79b678ef3c6bd431c43a335a2b19de15'
		headers = {"Accept": "application/json"}
		# call get service with headers and params
		response = requests.get(url,data = data)
		## print ("code:",str(response.status_code))
		## print ("******************")
		## print ("headers:", str(response.headers))
		## print ("******************")
		response_data = str(response.text);
		json_data = json.loads(response_data)
		print(json_data["name"])
		return json_data["name"]

	def response1(self,text,type):
		print text
	    ret = self.parse(text,type)
	    print (ret)
	    if ret == "transaction check" :
	        return self.consumeGETRequestSync()
	    if ret == "account check" :
	        return self.accountCheck()

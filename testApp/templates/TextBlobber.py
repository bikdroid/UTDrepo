from textblob import TextBlob


class TextBlobber(object):
	def __init__(self):

		wiki = TextBlob("Please check my account balance.")
		wiki = TextBlob("Please check balance in my account.")

		print(wiki.tags)

		verbs = list()
		nouns = wiki.noun_phrases

		for word,tag in wiki.tags:
		    if tag == 'VB':
		        verbs.append(word.lemmatize())
		    if tag == 'NN':
		        nouns.append(word.lemmatize())

		print("verbs are :",verbs)
		print("nouns are : " ,nouns)

		if 'check' in verbs:
		    if 'account balance' in nouns:
		        print("account check")
		    if 'check balance' in nouns:
		        print("account check")

	def createQuery(self, query):
		print "This is query create."
		print "Function for "
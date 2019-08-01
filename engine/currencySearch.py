import twder

def currencySearch(search):
	dollerTuple = twder.now(search)
	reply = '{}\n{}日幣的即期賣出價:{}'.format(dollerTuple[0],search,dollerTuple[4])
	return reply
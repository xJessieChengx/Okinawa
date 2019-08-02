import twder

def currencySearch(search):
	dollerTuple = twder.now_all()[search]
	#reply = '{}\n{}即期賣出價:{}'.format(dollerTuple[0],search,dollerTuple[4])
	reply = '{}\n{}\n現金買入價：{}\n現金賣出價：{}\n即期買入價：{}\n即期賣出價：{}'.format(dollerTuple[0],search,dollerTuple[1],dollerTuple[2],dollerTuple[3],dollerTuple[4])
	return reply
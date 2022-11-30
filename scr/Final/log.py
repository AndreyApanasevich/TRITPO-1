from datetime import datetime

def Log(content):
	print("Log: %s - %s" %(datetime.now(), content))

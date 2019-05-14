import re

def findip(f):
	result = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", f)
	return result
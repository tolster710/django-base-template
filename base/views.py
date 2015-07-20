""" Views for the base application """

from django.shortcuts import render
#from couchbase.bucket import Bucket
#from couchbase.exceptions import NotFoundError
from django.http import HttpResponse
import urllib2, json
import numpy as np


def home(request):
    """ Default view for the root """
    return render(request, 'base/home.html')



def latest_readings(request, n=5):
	url_base = 'http://127.0.0.1:8092/dm-test/_design/dm/_view/latest_readings?descending=true&inclusive_end=true&stale=false&connection_timeout=60000&limit=%s&skip=0' %(n)
	c_key='c:LAST_READING_CACHE'
	msg = 'Latest Readings'
	view_range=[5,10,15,20,50]
	response = urllib2.urlopen(url_base)
	html = response.read()
	parsed = json.loads(html)['rows']
	new_arr=[]
	for i in parsed:
		try:
			tmp={}
			tmp.update({'id': i['id'], 'time': format_time(i['value'][0]), 'BAC':i['value'][1]})
			new_arr.append(tmp)
		except Exception as e:
			print e
			pass
	
	return render(request, 'latest_records.html', {'view_range': view_range, 'message':msg, 'entry':new_arr})


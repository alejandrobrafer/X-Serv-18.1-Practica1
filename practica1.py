#!/usr/bin/python3
"""
Práctica 1: Objetivo la creación de una aplicación web simple para
acortar URLs.
"""

import webapp
from urllib.parse import unquote
import csv

PREFIX = 'http://'
PRACTICE_NAME = "<head><title>URL shortener~SARO_2018</title></head>"
FILE_NAME = 'prueba.csv'

port = 1234
machine = "localhost"
origi_URL_dic = {}
simpli_URL_dic = {}


def read_data(file):
	dates = None
	try:
		with open(file, newline='') as csvfile:
			lines = csv.reader(csvfile, delimiter=' ', quotechar='|')
			for line in lines:
				text = (', '.join(line))
			dates = text[1:-1].split(', ')
	# Case: the file doesn't exist
	except IOError:
		csvfile = open(file, "wb")
	csvfile.close()
	return dates


def update_dictionary(opt, text):
	dictionary = {}
	if text is not None:
		for lines in text:
			dirty_key, dirty_value = lines.split(": ")
			key = dirty_key.split("'")[1]
			value = dirty_value.split("'")[1]
			if opt == "Actived":
				aux = key
				key = value
				value = aux 
			dictionary[key] = value
	return dictionary


def write_data(file, dic):
	f = open(file, 'w')
	data = csv.writer(f, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL) 
	data.writerow([dic])
	f.close()


def router(url):
	return ("<html>" + PRACTICE_NAME + "<head><META HTTP-EQUIV='REFRESH' CONTENT='5;URL=" + str(url) + "'>" +
	"</head><body>Redirecting in 5 seconds ...</body></html>")

form = """
<h1><font color="darkslategray"><center><u>URL shortener ~ SARO 2018</u></center></font></h1>
<br>
<form action="" method="POST"><input type="text" name="URL" value="" placeholder="Your original URL here"/>
<input type="submit" value="SHORTEN URL"/><input type="reset" value="Reset"></form>
<br><br>
<b><i>List of original and shortened URLs at this time:</i></b>
"""


Codes = {'200': 'OK', '404': 'Not Found', 
		'302': 'Found', '501': 'Not Implemented'}


def send_response(Code, Body):
	return (Code + " " + Codes[Code], "<html>" + PRACTICE_NAME + "<body><h1>" + Body + "</h1></body></html>")


class practice1App(webapp.webApp):

	def __init__(self, hostname, port):
		try:
			old_dic = read_data(FILE_NAME)
		# Case: the file is empty
		except UnboundLocalError:
			old_dic = None
		self.origi_URL_dic = update_dictionary(None, old_dic)
		self.simpli_URL_dic = update_dictionary("Actived", old_dic)
		super().__init__(hostname, port)
	
	def parse(self, request):
		"""Parse the received request, extracting the relevant information."""
		# request.split()[0] == metodo (GET, POST...)
		# request.split()[1] == recurso ('/', '/0', '/1'...)
		# I'm shipping request because I will need it for POST method 
		try:
			return (request.split()[0], request.split()[1], request)
		# Case: favicon.ico
		except IndexError: 
			return None

	def process(self, parsedRequest):
		"""Process the relevant elements of the request."""
		# Case: favicon.ico
		if not parsedRequest:
			response = send_response('200', "<center>Go awy!</center>")
		else:
			method, resource, petition = parsedRequest

			if method == 'GET' and resource == '/':
				response = send_response('200', form + str(self.origi_URL_dic))
			
			elif method == 'GET':
				num = resource.split('/')[1]
				key = "/" + num
				
				if key in self.origi_URL_dic:
					response = ('302 Found', router(self.origi_URL_dic[key]))
				else:
					response = send_response('404', "<center>Resource Not Found!</center>")
				
			elif method == 'POST' and resource == '/':
				body = petition.split('\r\n\r\n', 1)[1]
				headers = petition.split('\r\n\r\n', 1)[0]
				content_length = int(headers.split('Content-Length: ')[1].split('\r\n')[0])

				if content_length < 5 or body.find("URL=") == -1:
					response = send_response('404', "<h2><center>URL not generated by this server.</center></h2>")
				else:
					_, url = body.split('=')
					# To convert the replace (%3A and %2F...) in the url. 
					url = unquote(unquote(url))
					# Case: If URL hasn't prefix 'http://' or 'https://'
					if url.find('http://', 0, 7) == -1 and url.find('https://', 0, 8) == -1:
						url = PREFIX + url
						# Note: I have considered that a URL with 'http://' is different that a URL with 'https://'
					
					# I search if the URL isn't in the dictionary
					if url not in self.simpli_URL_dic:
						self.origi_URL_dic["/" + str(len(self.origi_URL_dic))] = url
						self.simpli_URL_dic[url] = ("/" + str(len(self.origi_URL_dic) - 1))
						write_data(FILE_NAME, self.origi_URL_dic)	

					links = ("<h2><font color='darkslategray'>Choose one:</font></h2>" +
							"<h4>Your shortened URL: <a href='//" + str(machine) + ":" + str(port) + str(self.simpli_URL_dic[url]) +
							"'>http://" + str(machine)+ ":" + str(port) + str(self.simpli_URL_dic[url]) + "</a>" +
							"<br>Your original URL: <a href='" + str(self.origi_URL_dic[self.simpli_URL_dic[url]]) + "'>" + 
							str(self.origi_URL_dic[self.simpli_URL_dic[url]]) + "</a></h4>")
					response = send_response('200', links)
			else:
				response = send_response('501', "<center>Service not implemented on this server.</center>")
		
		"""Returns the HTTP code for the reply, and an HTML page."""
		print(self.origi_URL_dic, self.simpli_URL_dic)
		return response

if __name__ == "__main__":
	MyWebApp = practice1App(machine, port)

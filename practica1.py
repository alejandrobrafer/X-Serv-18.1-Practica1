#!/usr/bin/python3

"""
Práctica 1: Objetivo la creación de una aplicación web simple para
acortar URLs.
"""

import webapp
from urllib.parse import unquote

PREFIX = 'http://'
PRACTICE_NAME = "<head><title>URL shortener~SARO_2018</title></head>"
port = 1234
machine = "localhost"
origi_URL_dic = {}
simpli_URL_dic = {}

def router(url):
	return ("<html>" + PRACTICE_NAME + "<head><META HTTP-EQUIV='REFRESH' CONTENT='5;URL=" + str(url) + "'>" +
	"</head><body>Redirecting in 5 seconds ...</body></html>")

form = """
<h1><font color="Blue"><center><u>URL shortener ~ SARO 2018</u></center></font></h1>
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
	
	def parse(self, request):
		"""Parse the received request, extracting the relevant information."""
		# request.split()[0] == metodo (GET, POST...)
		# request.split()[1] == recurso '/'
		try:
			return (request.split()[0], request.split()[1], request)
		# Case: favicon.ico
		except IndexError: 
			return None

	def process(self, parsedRequest):
		"""Process the relevant elements of the request."""
		# Case: favicon.ico
		if not parsedRequest:
			response = send_response('200', "<center>Go awy!<center>")
		else:
			method, resource, petition = parsedRequest

			if method == 'GET' and resource == '/':
				response = send_response('200', form + str(origi_URL_dic))
			
			elif method == 'GET':
				num = resource.split('/')[1]
				key = "/" + num
				
				if key in origi_URL_dic:
					response = ('302 Found', router(origi_URL_dic[key]))
				else:
					response = send_response('404', "<center>Resource Not Found!</center>")
				
			elif method == 'POST':
				body = petition.split('\r\n\r\n', 1)[1]
				headers = petition.split('\r\n\r\n', 1)[0]
				content_length = int(headers.split('Content-Length: ')[1].split('\r\n')[0])

				if content_length < 5 or body.find("URL=") == -1:
					response = send_response('200', "<h2><center>This server was unable to generate this URL.</center></h2>")
				else:
					_, url = body.split('=')
					# To convert the replace(%3A and %2F ...) in the url. 
					url = unquote(unquote(url))
					# If URL hasn't prefix 'http://' or 'https://'
					if url.find('http://', 0, 7) == -1 and url.find('https://', 0, 8) == -1:
						url = PREFIX + url
					
					# I search if the URL isn't in the dictionary
					if not url in simpli_URL_dic:
						origi_URL_dic["/" + str(len(origi_URL_dic))] = url
						simpli_URL_dic[url] = ("/" + str(len(origi_URL_dic) - 1))
						
					links = ("<h2><font color='Blue'>Choose one:</font></h2>" +
							"<h4>Your shortened URL: <a href='//" + str(machine) + ":" + str(port) + str(simpli_URL_dic[url]) +
							"'>http://" + str(machine)+ ":" + str(port) + str(simpli_URL_dic[url]) + "</a>" +
							"<br>Your original URL: <a href='" + str(origi_URL_dic[simpli_URL_dic[url]]) + "'>" + 
							str(origi_URL_dic[simpli_URL_dic[url]]) + "</a></h4>")
					response = send_response('200', links)
			else:
				response = send_response('501', "<center>Service not implemented on this server.</center>")
		
		"""Returns the HTTP code for the reply, and an HTML page."""
		print(origi_URL_dic, simpli_URL_dic)
		return response

if __name__ == "__main__":
    MyWebApp = practice1App(machine, port)

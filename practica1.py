#!/usr/bin/python3

"""
Práctica 1: Objetivo la creación de una aplicación web simple para
acortar URLs
"""

import webapp
from urllib.parse import unquote

PREFIX = 'http://'

origi_URL_dic = {}
simpli_URL_dic = {}

def redirector(url):
	return ("<html><head><title>Redirigir al navegador a otra URL</title>" +
	"<META HTTP-EQUIV='REFRESH' CONTENT='5;URL=" + str(url) + "'>" +
	"</head><body>Esta página cambia en 5 segundos por la portada de DesarrolloWeb.com</body></html>")

form = """
<html>
<head><title>SHORTEN URL~SARO_2018</title></head>
<body>
 
<h3>Simplify your links</h3>
 
<form action="" method="POST">
  Your original URL here:
  <input type="text" name="URL" value="None"/>
  <br/>
  <input type="submit" value="SHORTEN URL" />
</form>
  <br/>
<h4>We currently have the following shortened URLs:</h4>
</body>
</html>
"""

Codes = {'200': 'OK', '404': 'Not Found', 
		'302': 'Found', '501': 'Not Implemented'}

def send_response(Code, Body):
	return (Code + " " + Codes[Code], "<html><body><h1>" + Body + "</h1></body></html>")

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
			response = send_response('200', 'Go awy!')
		else:
			method, resource, petition = parsedRequest

			if method == 'GET' and resource == '/':
				response = send_response('200', form + str(origi_URL_dic))
			
			elif method == 'GET':
				num = int(resource.split('/')[1])
				
				if num in origi_URL_dic:
					response = ('302 Found', redirector(origi_URL_dic[num]))
				else:
					response = send_response('404', "Resource Not Found!")
				
			elif method == 'POST':
				body = petition.split('\r\n\r\n', 1)[1]
			
				if body.find("URL=None") != -1 or not body: # el or para el caso de POSTER sin nada en el body
					response = send_response('501', "Server error in form")
				else:
					_, url = body.split('=')
					# To convert the replace(%3A and %2F ...) in the url. 
					url = unquote(unquote(url))
					# If URL hasn't prefix 'http://' or 'https://'
					if url.find('http://', 0, 7) == -1 and url.find('https://', 0, 8) == -1:
						url = PREFIX + url
					
					# I search if the URL isn't in the dictionary
					if not url in simpli_URL_dic:
						origi_URL_dic[len(origi_URL_dic)] = url
						simpli_URL_dic[url] = len(origi_URL_dic) - 1
						
					link = ("<a href='//localhost:1234/" + str(simpli_URL_dic[url]) + "'>Your shortened URL</a>" +
							"<br><a href='" + str(origi_URL_dic[simpli_URL_dic[url]]) + "'>Your original URL</a>")
					response = send_response('200', link)
			else:
				response = send_response('404', "Resource Not Found!")
		
		"""Returns the HTTP code for the reply, and an HTML page."""
		print(origi_URL_dic, simpli_URL_dic)
		return response

if __name__ == "__main__":
    MyWebApp = practice1App("localhost", 1234)

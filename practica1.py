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

class practice1App(webapp.webApp):
	
	def parse(self, request):
		"""Parse the received request, extracting the relevant information."""
		# request.split()[0] == metodo (GET, POST...)
		# request.split()[1] == recurso '/'
		try:
			return (request.split()[0], request.split()[1], request)
		except IndexError: 
			return None

	def process(self, parsedRequest):
		"""Process the relevant elements of the request."""
		if not parsedRequest:
			return ("200 OK", "<html><body><h1> Go Away!"+"</h1></body></html>")
		else:
			method, resource, petition = parsedRequest

			if method == 'GET' and resource == '/':
				response = form + str(origi_URL_dic)
			
			elif method == 'POST':
				body = petition.split('\r\n\r\n', 1)[1]
			
				if body.find("URL=None") != -1:
					response = "Server error in form"
				else:
					_, url = body.split('=')
					# To convert the replace(%3A and %2F ...) in the url. 
					url = unquote(unquote(url))
					# If URL hasn't prefix 'http://' or 'https://'
					if url.find('http://', 0, 7) == -1 and url.find('https://', 0, 8) == -1:
						url = PREFIX + url
					
					# antes de meter tendre que buscar haber si esta
					if not url in simpli_URL_dic:
						print("IIIIIIIIIIIINNNNNNNNNNNN")
						origi_URL_dic[len(origi_URL_dic)] = url
						simpli_URL_dic[url] = len(origi_URL_dic) - 1
						
					link1 = "<a href='//localhost:1234/" + str(simpli_URL_dic[url]) + "'>Your shortened URL</a>" 
					link2 = "<br><a href='" + str(origi_URL_dic[simpli_URL_dic[url]]) + "'>Your original URL</a>"
					response = link1 + link2
			else:
				response = "Not Found!"
		
			"""Returns the HTTP code for the reply, and an HTML page."""
			print(origi_URL_dic, simpli_URL_dic)
			return ("200 OK", "<html><body><h1>" + response + "</h1></body></html>")

if __name__ == "__main__":
    MyWebApp = practice1App("localhost", 1234)

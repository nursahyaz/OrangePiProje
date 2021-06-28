
import os
import sys

if not os.getegid() == 0:
    sys.exit('Script must be run as root')


from time import sleep
from pyA20.gpio import gpio
from pyA20.gpio import port
from http.server import BaseHTTPRequestHandler, HTTPServer

led = port.PA20

gpio.init()
gpio.setcfg(led, gpio.OUTPUT)

Request = None

class RequestHandler_httpd(BaseHTTPRequestHandler):
  def do_GET(self):
    global Request
    messagetosend = bytes('merhaba',"utf")
    self.send_response(200)
    self.send_header('Content-Type', 'text/plain')
    self.send_header('Content-Length', len(messagetosend))
    self.end_headers()
    self.wfile.write(messagetosend)
    Request = self.requestline
    Request = Request[5 : int(len(Request)-9)]
    print(Request)
    if Request == 'on':
      gpio.output(led, 1)
    if Request == 'off':
      gpio.output(led, 0)
    return


server_address_httpd = ('192.168.1.105',8000)
httpd = HTTPServer(server_address_httpd, RequestHandler_httpd)
print('starting server')

try:
        httpd.serve_forever()
except KeyboardInterrupt:
        httpd.server_close()
GPIO.cleanup()

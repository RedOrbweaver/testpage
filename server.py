#/usr/bin/python3
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import random
import sys
import io
import os

if (len(sys.argv) >= 2 and (sys.argv[1] == "--help" or sys.argv[1] == "-h" or sys.argv[1] == "help")):
    print("server.py/testserver.py [hostname] [port] [directory]")
    exit(0)

hostName = "localhost" if len(sys.argv) <= 1 else sys.argv[1]
serverPort = 8081 if len(sys.argv) <= 2 else int(sys.argv[2])
if (len(sys.argv) >= 4):
    os.chdir(sys.argv[3])

headers = []
quotes = [] 

def loadlines(filename: str):
    ret = []
    contents = ""
    with open(filename, 'r') as file:
        contents = str(file.read())
    for line in contents.split("\n"):
        if(line != "" and line != " " and line != "\n" and line.replace(" ", "") != ""):
            ret.append(line.replace("\\n", "\n"))
    return ret


def randnotlast(start, end, last):
    if(end-start <= 1):
        return 0
    n = 0
    for i in range(0, 10):
        n = random.randrange(start, end)
        if(n != last):
            return n
    if(n == 0):
        return n+1
    return n-1

class MyServer(BaseHTTPRequestHandler):
    lastq=-1
    lasth=-1
    def do_GET(self):
        headers = loadlines("Headers")
        quotes = loadlines("Quotes")
        headquote = headers[lastq := randnotlast(0, len(headers), self.lastq)]
        bodyquote = quotes[lasth := randnotlast(0, len(quotes), self.lasth)]
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=UTF-8")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>" + headquote + "</title></head>", "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))        
        self.wfile.write(bytes("<p>This is a test page.\n</p>", "utf-8"))
        self.wfile.write(bytes("<p>The quote for this GET request is:\n</p>", "utf-8"))
        if(bodyquote[-1] != "." and bodyquote[-1] != "!" and bodyquote[-1] != "?"):
            bodyquote += "."
        for line in bodyquote.split("\n"):
            if(line.find("<p") > 0 and line.find("</p>") > 0):
                self.wfile.write(bytes(line, "utf-8"))
            else:
                self.wfile.write(bytes("<p>" + line + "</p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))
    # def __init__():
    #     self.lastq=
if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")

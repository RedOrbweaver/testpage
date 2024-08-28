from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import random
import sys
import io

hostName = "localhost" if len(sys.argv) <= 1 else sys.argv[1]
serverPort = 8081 if len(sys.argv) <= 2 else sys.argv[2]

headers = []
quotes = [] 

def loadlines(filename: str):
    ret = []
    contents = ""
    with open(filename, 'r') as file:
        contents = str(file.read())
    for line in contents.split("\n"):
        if(line != "" and line != " " and line != "\n" and line.replace(" ", "") != ""):
            line = line.replace("\"", "&quot").replace("\'", "&quot").replace("&", "&amp")
            ret.append(line.replace("\\n", "\n"))
    return ret



class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        headers = loadlines("Headers")
        quotes = loadlines("Quotes")
        headquote = headers[random.randrange(0, len(headers))]
        bodyquote = quotes[random.randrange(0, len(quotes))]
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>" + headquote + "</title></head>", "utf-8"))
        self.wfile.write(bytes("<body>", "utf-8"))        
        self.wfile.write(bytes("<p>This is a test page.\n</p>", "utf-8"))
        self.wfile.write(bytes("<p>The quote for this GET request is:\n</p>", "utf-8"))
        if(bodyquote[-1] != "." and bodyquote[-1] != "!" and bodyquote[-1] != "?"):
            bodyquote += "."
        for line in bodyquote.split("\n"):
            self.wfile.write(bytes("<p>" + line + "</p>", "utf-8"))
        self.wfile.write(bytes("</body></html>", "utf-8"))

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
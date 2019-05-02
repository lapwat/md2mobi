#!/usr/bin/env python
import os
import http.server as server
import cgi

class HTTPRequestHandler(server.SimpleHTTPRequestHandler):
  def do_POST(self):
    os.chdir('..')

    # save markdown file
    form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={
      'REQUEST_METHOD':'POST',
      'CONTENT_TYPE': self.headers['Content-Type'],
    })
    file = form['file'].file
    filename = form['file'].filename
    file_path = os.path.basename(filename)
    file_length = int(self.headers['Content-Length'])
    with open(file_path, 'wb') as output_file:
      output_file.write(file.read(file_length))

    # convert file
    title = form['title'].value
    author = form['author'].value
    file_path = file_path.replace('$', '-')
    title = title.replace('$', '-')
    author = author.replace('$', '-')
    os.system(f"./convert.sh '{file_path}' '{title}' '{author}'")

    # craft response with mobi file
    self.send_response(200)
    self.send_header('Content-type', 'application/octet-stream')
    self.send_header('Content-Disposition', f'attachment; filename="{filename.replace(".md", ".mobi")}"')
    self.end_headers()
    with open('ebook.mobi', 'rb') as file:
      self.wfile.write(file.read())

    os.chdir('html')

if __name__ == '__main__':
    os.chdir('html')
    server.test(HandlerClass=HTTPRequestHandler)

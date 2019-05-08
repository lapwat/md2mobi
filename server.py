#!/usr/bin/env python
import os
import http.server as server
import cgi

class HTTPRequestHandler(server.SimpleHTTPRequestHandler):
  def do_POST(self):
    # save markdown file
    form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={
      'REQUEST_METHOD':'POST',
      'CONTENT_TYPE': self.headers['Content-Type'],
    })

    file = form['file'].file
    filename = form['file'].filename
    filename = filename.replace('$', '-').replace('/', '-').replace('..', '-').replace('\'', '-').replace('"', '-')
    file_length = int(self.headers['Content-Length'])

    with open('../uploads/' + filename, 'wb') as output_file:
      output_file.write(file.read(file_length))

    # convert file
    title = form['title'].value
    author = form['author'].value
    title = title.replace('$', '-').replace('/', '-').replace('..', '-').replace('\'', '-').replace('"', '-')
    author = author.replace('$', '-').replace('/', '-').replace('..', '-').replace('\'', '-').replace('"', '-')
    os.system(f"sh ../convert.sh '{filename}' '{title}' '{author}'")

    # craft response with mobi file
    self.send_response(200)
    self.send_header('Content-type', 'application/octet-stream')
    self.send_header('Content-Disposition', f'attachment; filename="{filename.replace(".md", ".mobi")}"')
    self.end_headers()
    with open(f'../uploads/ebook.mobi', 'rb') as file:
      self.wfile.write(file.read())

if __name__ == '__main__':
    try:
        os.mkdir('uploads')
    except OSError as exc:
        pass

    os.chdir('html')
    server.test(HandlerClass=HTTPRequestHandler)

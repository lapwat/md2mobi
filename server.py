#!/usr/bin/env python
import os
import http.server as server
import cgi
from datetime import datetime
from mailjet_rest import Client
import base64
import markdown2

class HTTPRequestHandler(server.SimpleHTTPRequestHandler):
  @staticmethod
  def email_file(email, filename):
    # # convert to html
    # html_content = str(markdown2.markdown_path(f'../uploads/{filename}'))
    # print(type(html_content))
    # f = open('test.html', 'w')
    # f.write(html_content.encode('utf8'))
    # f.close()

    with open(f'../uploads/{filename}', "rb") as fd:
      content = base64.b64encode(fd.read())

    b64content = str(base64.b64encode(content))
    filename = os.path.splitext(filename)[0] + '.mobi'

    # send html
    api_key = os.environ['API_KEY']
    api_secret = os.environ['API_SECRET']
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')
    data = {
      'Messages': [
        {
          "From": {
            "Email": "q.lapointe@gmail.com",
            "Name": "Quentin"
          },
          "To": [
            {
              "Email": "q.lapointe@gmail.com",
              "Name": "Quentin"
            }
          ],
          "Subject": "",#"md2mobi",
          "TextPart": "",#"Thank you for using Md2mobi. Please find enclose your file converted to MOBI.",
          "Attachments": [
            {
              "ContentType": "text/plain",
              "Filename": filename,
              "Base64Content": b64content
            }
          ]
        }
      ]
    }
    result = mailjet.send.create(data=data)
    print(result.json())

  def do_POST(self):
    # save markdown file
    form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={
      'REQUEST_METHOD':'POST',
      'CONTENT_TYPE': self.headers['Content-Type'],
    })

    title = form['title'].value
    author = form['author'].value
    textarea = form['file'][0]
    
    # protect against injections
    author = author.replace('$', '-').replace('/', '-').replace('..', '-').replace('\'', '-').replace('"', '-')
    title = title.replace('$', '-').replace('/', '-').replace('..', '-').replace('\'', '-').replace('"', '-')
    timestamp = int(datetime.timestamp(datetime.now()))

    if (textarea.value):
      filename = f'{author} - {title}_{timestamp}.md'
      writeToFile = textarea.value.encode()
    else:
      filename = f'{author} - {title}_({form["file"][1].filename})_{timestamp}.md'
      file = form['file'][1].file
      file_length = int(self.headers['Content-Length'])
      writeToFile = file.read(file_length)

    filename = filename.replace('$', '-').replace('/', '-').replace('..', '-').replace('\'', '-').replace('"', '-')
    with open('../uploads/' + filename, 'wb') as output_file:
      output_file.write(writeToFile)
    
    # convert file
    os.system(f"sh ../convert.sh '{filename}' '{title}' '{author}'")

    converted_filename = os.path.splitext(filename)[0] + '.mobi'
    if ('email' in form.keys()):
      email = form['email'].value
      # send to kindle
      # self.email_file(email, filename)
    else:
      # craft response with mobi file
      self.send_response(200)
      self.send_header('Content-type', 'application/octet-stream')
      self.send_header('Content-Disposition', f'attachment; filename="{converted_filename}"')
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

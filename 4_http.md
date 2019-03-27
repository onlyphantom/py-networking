# Introduction to HTTP
HTTP is an application layer protocol and almost always used on top of TCP. It consists of two elements:
- **request** made by client, asking for a particular resource specified by a URL
- **response** sent by server, supplies the resource that the client requested or fail with an error code

Under HTTP, all interactions are initiated by the client; The server never sends anything to the client without the client explicitly asking for it.

## Requests with `urllib.request`
For making requests and receiving responses, we use the `urllib.request` module

Consider the following example:
```py
from urllib.request import urlopen
response = urlopen("http://python.org")
response
# <http.client.HTTPResponse object at 0x10d1468d0>
response.readline()
# b'<!doctype html>\n'
```

`urllib.request.urlopen()` is used for sending a request and receiving a response for the resource at `http://python.org`. `readline()` prints the first line. We can take a closer iook at the attributes and methods on this object (`dir(response)`). 


```py {cmd="/anaconda3/envs/networking/bin/python"}
from urllib.request import urlopen
response = urlopen("http://python.org")
print(response.url, "\n", response.status)
```

Status codes are classified by their first digit:
- 100: Informational
- 200: Success
- 300: Redirection
- 400: Client error
- 500: Server error

Instead of reading line by line using `readline()` we can use `read()`. The following function calls print the first 120 bytes:
```py
response = urlopen('http://python.org')
response.read(120)
# b'<!doctype html>\n<!--[if lt IE 7]>   <html class="no-js ie6 lt-ie7 lt-ie8 lt-ie9"> <![endif]-->\n<!--[if IE 7]> <ht'
```

Once the data (or lines of it) has been read (either by `read()` or `readline()`), it cannot be re-read. Executing a second `response.read()` for example will return `b''`. Commonly, we would capture the output of our `read()` in a variable for processing later. Also, both `read` and `readline` return bytes objects without decoding the data they receive to Unicode.

### Handling errors
```py {cmd="/anaconda3/envs/networking/bin/python"}
import urllib.error
from urllib.request import urlopen
try:
    urlopen('https://python.org/dontexist')
except urllib.error.HTTPError as e:
    print('status', e.code)
    print('reason', e.reason)
    print('url', e.url)
```
 When we execute `urlopen('https://python.org/dontexist').readline()` in a Python session, it raises the following error, giving us a clue to the exception we should be trying to catch:

> raise HTTPError() urllib.error.HTTPError: HTTP Error 404: Not Found

### HTTP Headers
Requests and responses are made up of **headers** and a **body**. Headers are lines of protocol-specific information at the beginning of raw message sent over the TCP connection. The body is the rest of the message and separated from the headers by a blank line. 

An example of headers in a HTTP request:
```bash
GET / HTTP/1.1 # request method + path to resource + HTTP version
Accept-Encoding: identity
Host: www.python.org
Connection: close
User-Agent: Python-urllib/3.4
```
The first line is the **request line** and the rest of the lines are request headers. Each line follows the format of `header-name: value`. Headers in a request can be used for many purposes, including passing in cookies and authorization credentials, or asking the server for preferred formats of resources.




```py {cmd="/anaconda3/envs/networking/bin/python"}
from urllib.request import urlopen
response = urlopen('https://python.org')
print(response.getheaders())
```
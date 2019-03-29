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

An important header is the `Host`. Many web server applications provide the facilities to host more than one website on the same server using the same IP address. Effectively, the web server is given multiple hostnames one for each website it hosts. Since IP and TCP operates solely on IP addresses, they can't make requests using the hostname information. The HTTP protocol's implementation of a `Host` header solves this.

An example a response (headers separated from the body by a blank line):
```bash
HTTP/1.1 200 OK
Date: Thu, 28 Mar 2019 10:28:45 GMT
Content-Type: text/html
Content-Length: 4729
Server: Apache
Content-Language: en

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN">\n
...
```

In a response, the server can use headers to inform the client about things such as the length of the body, the cookie data, content language etc. We can call `getheaders()` on a response object returned by `urlopen()` to see the headers returned as a list of tuples: 

```py {cmd="/anaconda3/envs/networking/bin/python"}
from urllib.request import urlopen
response = urlopen('https://python.org')
print(response.getheaders())
```

### Customizing requests
We can add headers to a request before sending it. Instead of `urlopen()`, we will do the following:
- Create a `Request` instance
- Add headers to the `Request` instance
- Use `urlopen()` to send the request

```py
from urllib.request import urlopen, Request
req = Request("https://debian.org")
req.add_header('Accept-Language', 'de')
response = urlopen(req)
print(response.readlines()[:5])
# <title>Debian -- Das universelle Betriebssystem </title>
```

`header_items()` return the header present in a request. When we run our `Request` instance through `urlopen()`, a few more headers get added to it:

```py {cmd="/anaconda3/envs/networking/bin/python"}
from urllib.request import urlopen, Request
req = Request('http://www.python.org')
req.add_header('Accept-Language', 'id')
print(req.header_items(), "\n ---")
# [('Accept-Language', 'id')]
response = urlopen(req)
print(req.header_items())
# [('Host', 'www.python.org'), ('User-agent', 'Python-urllib/3.7'), ('Accept-language', 'id')]
```

We can add headers at the same time that we create our request object:
```py {cmd="/anaconda3/envs/networking/bin/python"}
from urllib.request import urlopen, Request
headers = {'Accept-Language': 'id'}
req = Request('http://python.org', headers=headers)
print(req.header_items())
```
We simply supply the header as a `dict` to the `Request` object constructor as the `headers` argument.

### Content compression
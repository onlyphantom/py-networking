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
print(response.headers)
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
We can also use the `Accept-Encoding` request header and the `Content-Encoding` response header to temporarily encode the body of a response for transmission over the network, reducing the amount of data that needs to be transferred:
1. Client sends a request with acceptable encodings listed in an `Accept-Encoding` header
2. Server picks an encoding method that it supports and encodes the body using this encoding method
3. Server sends the response specifying the encoding it has used in a `Content-Encoding` header
4. Client decodes the response using the specified encoding method

```py {cmd="/anaconda3/envs/networking/bin/python"}
from urllib.request import  urlopen, Request
import gzip
req = Request('http://www.debian.org')
req.add_header('Accept-Encoding', 'gzip')
response = urlopen(req)
print(response.getheader('Content-Encoding')) # returns gzip
content = gzip.decompress(response.read()) # client decodes
```

We can then proceed to print the content using `print(content.splitlines()[:5])` and obtained the following output:
```
[b'<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">', 
b'<html lang="en">', 
b'<head>', 
b'  <meta http-equiv="Content-Type" content="text/html; charset=utf-8">', 
b'  <title>Debian -- The Universal Operating System </title>']
```

Encodings are registered with IANA and currently contains `gzip`, `compress`, `deflate` and `identity`. First three are compression methods and `identity` states the client's preference to not have any encoding applied.

The client can tell the server that it accepts more than one encoding:
```py
req = Request('http://www.debian.org')
encodings = 'deflate, gzip, identity'
req.add_header('Accept-Encoding', encodings)

response = urlopen(req)
response.getheader('Content-Encoding') #gzip
```

Relative weightings can be given by adding a `q` value:
`encodings = 'gzip, defate;q=0.8, identity;q=0.0 '`

The default value of `q` is 1.0, which is also its maximum value, so the line above states the first preference should be `gzip`, second is `deflate` and `identity` if nothing else is available.

Content compression (`Accept-Encoding`) and Language selection (`Accept-Language`) are examples of **content negotiation** where the client specifies its preferences regarding the format and the content of the requested resource. Other examples of content negotiation include the following headers:
- `Accept`: Requesting a preferred file format
- `Accept-Charset`: Requesting the resource in a preferred character set

### Content types
HTTP can be used as a transport for any type of file or data. The server can use the `Content-Type` header in a response to inform the client about the type of data it has sent.

```py
response = urlopen("http://python.org")
response2 = urlopen("https://github.com/onlyphantom/verisr2/blob/master/README_files/collapse.png?raw=true")

response.getheader("Content-Type") # returns 'text/html; charset=utf-8'
response2.getheader("Content-Type") # returns 'image/png'
```
Notice that content type values, as in the case of the example above, can contain addiitional parameters to provide further information about the type -- typically the character set. This parameter is included after a semicolon and takes the form of a key/value pair. We could extract the character set directly using `split()`:
```py
format, params = response.getheader("Content-Type").split(";")
print(format) # returns text/html
print(params) # returns charset=utf-8

charset = params.split("=")[1] # print(charset) prints 'utf-8'
content = response.read().decode(charset) # decode content using the supplied charset
```

Values in this header are taken from a list maintained by IANA. They are also called **Internet media types** or **MIME types** (Multipurpose Internet Mail Extensions) and common ones include:
- `text/html`: HTML document
- `text/plain`: Plain text document
- `image/jpeg`: JPG image
- `application/pdf`: PDF document
- `application/json`: JSON data

The `application/octet-stream` media type is used for files that don't have an applicable media type, for example a pickled Python object or a file whose format is not known by the server. Possible approaches to discovering the format of these files are:
- Examine the filename extension of the downloaded resource (if it has one) using the `mimetypes` module
- Download the data and use a file type analysis tool. Python standard library `imghdr` module can be used for images, and the third-party `python-magic` package or the `GNU` file command can be used for other types

## User Agents
`User-Agent`, another example of a request header, is used by client to identify themselves in every request. Any client that communicates using HTTP can be referred to as a **user agent**.

As an exercise, we can fire up a web browser and use the built-in console to write the following Javascript to retrieve the user agent:
```js
navigator.userAgent 
// "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.2 Safari/605.1.15"
```
On Safari, we will get the same value by copying from: "Develop > User Agent > Other". 

Its syntax follows the convention: `User-Agent: <product> / <product-version> <comment>` and web browsers typically carry the following format:
`User-Agent: Mozilla/<version> (<system-information>) <platform> (<platform-details>) <extensions>`

When developers set the user agent such that it mimics a different browser, this is known as **spoofing**:

```py {cmd="/anaconda3/envs/networking/bin/python"}
from urllib.request import Request, urlopen
req = Request("http://www.python.org")
urlopen(req)
print(req.get_header('User-agent'), "\n ---")

req = Request("http://www.python.org")
req.add_header('User-Agent', 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_1 like Mac OS X) AppleWebKit/604.4.7 (KHTML, like Gecko) Version/11.0 Mobile/15C153 Safari/604.1')
response = urlopen(req)
print(req.headers['User-agent'].split("(")[1])
print(req.get_header("User-agent"))
```
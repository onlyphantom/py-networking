# The Request library

From Part 1 to 7 we've been using Python's standard `urllib` library. A popular third-party library, `Requests` offers much of the same functionality through a simplified API. 

Much of the commands between `urllib.request.urlopen` and `requests` look similar:
```py
from urllib.request import urlopen
response = urlopen("http://python.org")
print(response.url) # https://www.python.org/
print(response.status) # 200
print(response.reason) # OK
print(response.getheader('Content-Type')) # text/html; charset=utf-8
```

With `Requests`, the keys in the `headers` attribute are case-insensitive:
```py {cmd="/anaconda3/envs/networking/bin/python"}
import requests
response = requests.get('https://python.org')
response.url # https://www.python.org/
response.status_code # 200
response.reason # OK
response.headers['content-type'] # text/html; charset=utf-8
response.ok # True indicates status code in the 200 range
response.is_redirect # False in this case
response.request.headers # {'User-Agent': 'python-requests/2.21.0', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive'}
response.headers['Content-Encoding'] # 'gzip'
```

Notice that `Requests` automatically handle compression for us: in the request headers it has the `Accept-Encoding` and in `response.headers` we can see the key-value pair indicating a `gzip` type encoding. To print the response content, we can do `response.content`. But because `Request` also performs automatic decoding for us (by using values in the headers to determining a character set), we can use `response.text` instead to get the decoded content in Unicode. The returned values will be `str` rather than `bytes`.

```py
import requests
response = requests.get('https://google.com')
print(response.encoding) # see what encoding Requests use for this response
response.content # byte objects from HTTPResponse
response.text  # get the decoded content
```

- We can change the encoding (e.g `response.encoding = 'utf-8'`). 
- We can get the cookies from our responses (`response.cookies`)

The `Requests` library has a `Session` class which allows the reuse of cookies similar to how we use `http.CookieJar` and `HTTPCookieHandler`:
```py {cmd="/anaconda3/envs/networking/bin/python"}
import requests
from urllib.parse import parse_qs
s = requests.Session()
res = s.get('http://google.com')
print(dict(res.cookies)['NID'])
responsecookies = res.headers['Set-Cookie']

response = s.get('http://google.com')
requestcookies = response.request.headers['Cookie']

print(parse_qs(responsecookies)[' domain'][0])
print(parse_qs(requestcookies)[' NID'][0])
```
After our first request, the server sent its response the header of which contains a `Set-Cookie` header item. As we'll see, when we use the same session, there is a `Cookie` header containing the same cookie that was assigned to us by the server in our first request.

Compare that to the code block below, which is syntatically similar but you'll notice that the second request do not contain a `Cookie` header because these are two separate **sessions**.
```py {cmd="/anaconda3/envs/networking/bin/python"}
import requests
from urllib.parse import parse_qs
res = requests.get('http://google.com')
print(dict(res.cookies)['NID']) # 180=Xcj5zaq9vwndLK9VciAQvNQ...

response = requests.get('http://google.com')
print(response.request.headers) # No 'Cookie' key
```

Instead of a `GET` method, we can use other methods directly with `Request`:
```py
# HEAD is identical to GET except the server MUST NOT return a message-body in the response
response = requests.head('http://google.com') 
response.status_code # 200

data = {'P': 'Python'}
response = requests.post('http://search.debian.org/cgi-bin/omega', data=data)

params = {':action': 'search', 'term': 'models'}
response = requests.get('http://pypi.python.org/pypi', params=params)
```

One difference between `Request` and `urllib.request` is how error conditions are handled. `requests.get()` doesn't raise an exception unless we explicitly tells it to do so using `response.raise_for_status()`:

```py
import requests
response = requests.get('http://google.com/randompages')
print(response.status_code) # 404
```

The equivalent code in `urllib` however would throw an exception:
```py
from urllib.request import urlopen
response = urlopen('http://google.com/randompages')
print(response.status)
```

`raise_for_status()` returns `None` if there is no exception, making it suitable for a `try-except` block.
# URLs
## `urllib.parse`
A Uniform Resource Locator (**URL**) represent a resource on a given host. It can point to files on the server or the resources may be dynamically generated when a request is received. URLs are comprised of several sections and we can use `urllib.parse` to break it down into its component parts:

```py {cmd="/anaconda3/envs/networking/bin/python"}
from urllib.parse import urlparse
result = urlparse("https://github.com/onlyphantom/pedagogy")
print(result)
print(result.netloc) # network location
print(result.path)
```

Notice that the returned value recognizes `https` as the **scheme**, `github.com` as the **network location** and `/onlyphantom/pedagogy` as the **path**. When we use http or https to locate a specific resource, we need to know the host that it resides on and the TCP port we should connect to (together these are the `netloc` component); we also need to know the path to the resource on the host (`path` component)

### Port Numbers
Port numbers can be specified explicitly in a URL by appending them to the host:
```py {cmd="/anaconda3/envs/networking/bin/python"}
from urllib.parse import urlparse
result = urlparse('http://python.org:8080/')
print(result)
```
Notice that the `urlparse` method just interprets it as part of the netloc, which is fine because that's what handlers such as `urllib.request.urlopen()` expect. Without a supplied port, the default port 80 is used for `http` and 443 for `https`.

### `urllib.parse.urljoin`
Supposed we retrieved the `http://www.python.org` and within the source code found the relative URL for "Applications for Python" page is `about/apps`, we can create the final URL by joining the original URL with the relative URL:
```py {cmd="/anaconda3/envs/networking/bin/python"}
from urllib.parse import urljoin
path = urljoin('http://www.python.org', 'about/apps')
print(path)

path2 = urljoin('http://www.python.org/', 'about/apps')
print(path2)

path3 = urljoin('http://www.python.org/downloads', 'about/apps')
print(path3)

path4 = urljoin('http://www.python.org/downloads/', 'about/apps')
print(path4)

path5 = urljoin('http://www.python.org/downloads/other', '/about')
print(path5)
```

Three observations:
- Notice how `urljoin` filled in the slash between the host and the path when the base URL does not contain a path, but do a straightforward append when the base URL contains a path (example 1, 2 and 4)
- Notice how `urljoin` replaces the last path element in the base URL if doesn't end in a slash (example 3)
- Notice how we can force a path to replace all elements of a base URL by prefixing it with a slash (example 5)

If the 'relative' URL is actually an absolute URL, then the relative URL completely replaces the base URL. This is useful because we don't have to worry about testing whether a URL is relative or not before using it with `urljoin`
```py
urljoin('http://python.org', 'http://debian.org')
# returns 'http://debian.org'
```

## Query Strings
Another property of URLs is that they can contain additional parameters in the form of key/value pairs after the path. These are separated from the path by a question mark and multiple parameters are separated by ampersands (`&`):
`https://www.python.org/search/?q=urllib&submit=`

```py
from urllib.parse import urlparse, parse_qs
result = urlparse('https://www.python.org/search/?q=urllib&submit=true')

print(result) # ParseResult(scheme='https', netloc='www.python.org', path='/search/', params='', query='q=urllib&submit=true', fragment='')
print(parse_qs(result.query)) # {'q': ['urllib'], 'submit': ['true']}
```

Notice that `urlparse` recognizes the query string as the `query` component. Query strings provide additional parameters to the resource that we wish to retrieve and is usually used to customize the resource in some way. Additionally, the `urllib.parse.parse_qs` function is used to convert the query string into a dictionary.

## URL Encoding
URLs are restricted to the ASCII characters and within this set, some characters are reserved and need to be escaped using URL encoding (or **percent encoding** because it uses `%` as an escape character):
```py
quote("Marry you? Yes, everytime!")
# returns 'Marry%20you%3F%20Yes%2C%20everytime%21'
```
Notice how special characters like `' '`, `,` and `?` are replaced by escape sequences; The numbers in the escape sequences are the characters' ASCII codes in hexadecimal. 

`urllib` helps us contruct URLs by providing us methods to:
- escape any spaces or special characters in our path using `quote()`
- URL-encode our query strings using `urlencode()`
- Combine our path and query strings using `urlunparse()`

```py
from urllib.parse import quote, urlencode, urlunparse
path = 'en/2.2/search'
path_enc = quote(path)
query_dict = {'q':'model class', 'release': '2.2', 'page': '2'}
query_enc = urlencode(query_dict)
print(query_enc) # returns q=model+class&release=2.2&page=2

netloc = 'docs.djangoproject.com'
url = urlunparse(('http', netloc, path_enc, '', query_enc, ''))
print(url) # returns:
# http://docs.djangoproject.com/en/2.2/search?q=model+class&release=2.2&page=2
```

Notice that `/` and `-` are examples of accepted character so `quote` ignores and doesn't encode them. A path string `en/2.2/search+here` will be encoded to `en/2.2/search%2Bhere`: all of these are the intended behavior for paths.

### Caveats with `/` in resource name
When a resource name contains slashes (`/`), the slash doesn't get escaped and this will cause the url to be incorrectly interpreted as an extra level of directory structure:

```py
from urllib.parse import quote
username = '+Phantom/Onlyphantom+'
path = 'img/users/{}'.format(username)
print(quote(path)) # returns: img/users/%2BPhantom/Onlyphantom%2B
```

The solution is to escape each path element separately and then join them, passing `safe` so `quote` knows not to ignore slashes:
```py
'/'.join(('','dir')) # returns '/dir'
'/'.join(('root','dir','usr')) # returns 'root/dir/usr'

username = '+Phantom/Onlyphantom+'
quote(username) # '%2BPhantom/Onlyphantom%2B'
user_encoded = quote(username, safe='') # '%2BPhantom%2FOnlyphantom%2B'

path = '/'.join(('','img','users', user_encoded))
print(path)
```

# Example: python downloader/RFC_downloader.py 2324 | less
# 'less' is a terminal pager: https://en.wikipedia.org/wiki/Less_(Unix)

import sys, urllib.request

try:
    rfc_number = int(sys.argv[1])
except (IndexError, ValueError):
    print('Must supply an RFC number as first argument')
    sys.exit(2)

url = 'http://www.ietf.org/rfc/rfc{}.txt'.format(rfc_number)
rfc_raw = urllib.request.urlopen(url).read()
rfc = rfc_raw.decode() # decode to Unicode
print(rfc)
# HTTPie CLI — Snapshot Test

## Phase 1: Installation Verification

Verify httpie is installed.

> `command -v http`
```
/usr/local/bin/http
```

Check version.

> `http --version`
```
3.2.4
```

## Phase 2: Help Output

Test the help command structure.

> `http --help | head -30`
```
usage:
    http [METHOD] URL [REQUEST_ITEM ...]

HTTPie: modern, user-friendly command-line HTTP client for the API era. <https://httpie.io>

Positional arguments:
  
  These arguments come after any flags and in the order they are listed here.
  Only URL is required.

  METHOD
      The HTTP method to be used for the request (GET, POST, PUT, DELETE, ...).
      
      This argument can be omitted in which case HTTPie will use POST if there
      is some data to be sent, otherwise GET:
      
          $ http example.org               # => GET
          $ http example.org hello=world   # => POST
      
  URL
      The request URL. Scheme defaults to 'http://' if the URL
      does not include one. (You can override this with: --default-scheme=http/https)
      
      You can also use a shorthand for localhost
      
          $ http :3000                    # => http://localhost:3000
          $ http :/foo                    # => http://localhost/foo
      
  REQUEST_ITEM
      Optional key-value pairs to be included in the request. The separator used
```

## Phase 3: Offline Functionality

Test building a request without sending (print mode).

> `http --offline GET https://example.com/api/users Accept:application/json`
```
GET /api/users HTTP/1.1
Accept-Encoding: gzip, deflate
Connection: keep-alive
User-Agent: HTTPie/3.2.4
Accept: application/json
Content-Type: application/json
Host: example.com

```

Test POST request printing.

> `http --offline --ignore-stdin POST https://example.com/api/items name="Test Item" price:=9.99`
```
POST /api/items HTTP/1.1
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Length: 36
User-Agent: HTTPie/3.2.4
Accept: application/json, */*;q=0.5
Content-Type: application/json
Host: example.com

{"name": "Test Item", "price": 9.99}
```

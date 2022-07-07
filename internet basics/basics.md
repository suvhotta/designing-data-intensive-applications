## HTTP Basics
- Application layer protocol built on top of transport layer: TCP.
- Its a client server protocol, where the requests are mostly initiated from client side. (Exception being web-hooks
  where the requests are initiated from the server back to client)
- Client is otherwise known as user-agent.
- HTTP is stateless i.e. no link between successive requests in the same connection.


## HTTP Connection
- Connection is controlled at the transport layer. Since there isn't any state maintained between client and server, the
    underlying transport layer needs to be robust to not lose any messages. Thus, TCP is preferred over UDP for transport.
- Before a client/server can send messages, they need to establish a TCP connection, which happens over several round trips.
- HTTP 1.0: Separate TCP connection for each HTTP request/response pair. Was thus very slow
- HTTP 1.1: Introduced pipeline and persistent connections to mitigate issue in HTTP 1.0.
- HTTP 2.0: Introduced multiplexing to keep the connection warm for several Request/Response cycles.


##HTTP Methods:
- GET: Retrieve data
- HEAD: Asks for a response similar to the GET but without the actual body. Used if a URL might produce a large file
    then HEAD might give the Content-Length without actually downloading the file.
- POST: Sends data to the server. The type of the body of the request can be specified in the content-type header.
- PUT: Does a complete replacement of the target resource with the request payload. (Depends on the underlying server 
  implementation of the method)
- PATCH: Does a partial replacement.
- DELETE: Destroys the resource.

### Safe methods:
- Simple definition: Read-only operation are safe.
- A safe method doesn't alter the state of the server. eg: GET, HEAD

### Idempotent Methods:
- An identical request has always the same effect while leaving the server in the same state irrespective of number of
    times of invocation. Eg: All the methods except POST.

Depends also on how the server has implemented the HTTP Methods.


## Caching:
- Handled using the `cache-control` header. The max-age property tells if the cache is still fresh or stale.


## What is meant by same origin?
- Origin is a combination of the protocol, domain, port of the URL.
    2 URLs are said to be of the same origin if all the above match.
- The resource path doesn't matter while matching origins.

## What is CORS?
CORS is a security mechanism that allows a web page from one domain or Origin to access a resource with a different 
domain (a cross-domain request). CORS is a relaxation of the same-origin policy implemented in modern browsers. 
Without features like CORS, websites are restricted to accessing resources from the same origin through what is known 
as same-origin policy.

Any resource sharing across origins is through CORS.


## CORS Simple Request:
- Request made through GET, POST, HEAD.
- The browser adds the origin in the request. The server checks the Origin header and if the origin value is allowed, 
    it sets the Access-Control-Allow-Origin to the value in the request header Origin.
- When the browser receives the response, the browser checks the Access-Control-Allow-Origin header to see if it matches the origin of the tab. If not, the response is blocked. The check passes such as in this example if either the Access-Control-Allow-Origin matches the single origin exactly or contains the wildcard * operator.

## CORS Preflight Request:
- It is a request that checks to see if the CORS protocol is understood and server is aware using specific
    headers and methods. 
- It is an OPTIONS request using three HTTP request headers: Access-Control-Request-Method, 
    Access-Control-Request-Headers, and the Origin header.
 
## CORS Preflight requirement:
- It uses methods other than GET, HEAD or POST. Also, if POST is used to send request data with a Content-Type other 
  than application/x-www-form-urlencoded, multipart/form-data, or text/plain, e.g. if the POST request sends an XML 
  payload to the server using application/xml or text/xml, then the request is preflighted.
- It sets custom headers in the request (e.g. the request uses a header such as X-PINGOTHER)

### Examples of preflight requests:
1. A website makes an AJAX call to POST JSON data to a REST API meaning the Content-Type header is application/json

2. A website makes an AJAX call to an API which uses a token to authenticate the API in a request header such Authorization

## CORS Prefetch
- Before performing the actual sharing of resources through CORS protocol, 
    the browser sends an OPTIONS request to check if the server is aware using specific
    methods and HEADERS.
- This request is automatically sent by the browser and needn't be explicitly sent from frontend.

- It is an OPTIONS request using three HTTP req HEADERS: Access-Control-Request-Method, 
     Access-Control-Request-Headers, and the Origin header.

- Access-Control-Request-Method is a header to specify which HTTP method will be actually
    used after the preflight request. If the server allows it, it will send same in the
     Access-Control-Allow-Methods response header.

- Access-Control-Request-Headers similarly seeks to check with the server what all additional
    request headers are allowed to be passed. The response of the same is being passed on in 
    the access-control-allow-headers.

- Origin request header specifies what was the origin for the request.

- CORS preflight response is restricted to status 200 or 204.

- CORS failure results in errors which can be further diagnosed by checking the console output 
    of the browser.

## How state/session is maintained in HTTP?
- HTTP is a stateless protocol i.e. there isn't any continuously active session being maintained b/w client and server.
- User authentication can happen in 2 ways:
  - Sessions: The server creates and maintains a sessionID in a cookie at the browser/client and the sessionID is passed
        along from the client side every subsequent request being made. 
        Can log somebody out immediately by disabling the session ID.
        Know which user has logged in.
        Issues: CSRF, Maintenance overhead of server side sessions.
  - JWT: JSON Web tokens are tokens created with some signature specific to the server. If somebody tries to modify the
        payload then the signature validation would fail. However, anybody with access to the computer might read what is
        present in that JWT token. 
        Not possible to log out user immediately.
        Can't possibly know which user has logged in.

- Cookie is a piece of string. Whenever the server has to set a cookie on the user's browser, it does so by passing data
    along with the `set-cookie` response header.
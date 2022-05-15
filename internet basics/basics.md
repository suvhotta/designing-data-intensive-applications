## What is meant by same origin?
- Origin is a combination of the protocol, domain, port of the URL.
    2 URLs are said to be of the same origin if all the above match.
- The resource path doesn't matter while matching origins.

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
## Request-Response cycle in python
- When client makes a request to the flask server, it makes a Request object to encapsulate the HTTP request sent 
    by the client.


### Application & Request Context
- To avoid passing multiple variables, flask uses global variables known as context.
    `from flask import request` Here request is treated like it is a global variable. But in reality in a multi-threaded 
    system, there can be various threads each serving a different request. So flask uses something called context local.
    Context-local are a Werkzeug implementation of concept similar to python's thread-local.
- When a request is received, Flask provides 2 contexts:
  - application context: Keeps track of the application-level data (configuration variables, logger, database connection)
  2 variables available as part of application context:
    - current_app: an instance of the active application.
    - g: a stack to store temporary objects while handling a request. This variable is reset with every new request.
  These 2 variables become available when app_context.push() is fired after a request.
  - request context: Keeps track of the request-level data (URL, HTTP method, headers, request data, session info)
  2 variables available as part of request context:
    - request: the encapsulated current HTTP request.
    - session: dict to store values between requests.
  These 2 variables become available when request_context.push() is fired after a request.
    - endpoint: endpoint name for the route
    - method: HTTP method
    - host: host defined in request by client
    - URL
    - environ
- There are 4 request hooks available as decorators to perform certain actions before a request/response is served:
  - before_request: Before every request
  - before_first_request: Before the first request is served by the server. Can be useful in performing some server
        initialization tasks.
  - after_request: After each request only if no exception got raised.
  - teardown_request: After each request even if some unhandled exception got raised.


### Request Object:
- Contains all information about what the client sent in the actual HTTP request.
- There are method that are associated with the request object to access its data:
  - get_data
  - get_json
  - is_secure: if the request came through HTTP or HTTPs protocol.
- There are also some variables associated 

### How flask maps urls?
- All the routes for an app are stored on the `app.url_map` which contains a mapping to the urls to the view functions.
    The map also contains which all the HTTP methods which the view function supports.

### Request processing cycle:
- Client sends request -> web server -> WSGI server(like gunicorn) -> flask application.
- WSGI server is needed because it is an interface between the webserver and the python based web application. It is 
    required because a web server can't talk directly to a python application.
- Flask application -> WSGI server -> web server -> client received response.
- Flask development server is a WSGI server but not meant to be used in production. That's why for local testing we don't
    require a WSGI server.
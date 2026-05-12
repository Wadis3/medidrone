# medidrone

coords:
    fh1: [50.361825, 35.915570]
    fh2: [50.286543, 36.941948]

flask run --host=0.0.0.0
 * Serving Flask app 'drone.py'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://10.8.26.196:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 125-331-670
192.168.0.2 - - [12/May/2026 12:30:22] "POST / HTTP/1.1" 500 -
Traceback (most recent call last):
  File "/usr/lib/python3/dist-packages/urllib3/connection.py", line 198, in _new_conn
    sock = connection.create_connection(
    
  File "/usr/lib/python3/dist-packages/urllib3/util/connection.py", line 85, in create_connection
    raise err
  File "/usr/lib/python3/dist-packages/urllib3/util/connection.py", line 73, in create_connection
    sock.connect(sa)
    ~~~~~~~~~~~~^^^^
OSError: [Errno 113] No route to host

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/usr/lib/python3/dist-packages/urllib3/connectionpool.py", line 787, in urlopen
    response = self._make_request(
    
  File "/usr/lib/python3/dist-packages/urllib3/connectionpool.py", line 493, in _make_request
    conn.request(
    ^
  File "/usr/lib/python3/dist-packages/urllib3/connection.py", line 445, in request
    self.endheaders()
    ~~~~~~~~~~~~~~~^^
  File "/usr/lib/python3.13/http/client.py", line 1333, in endheaders
    self._send_output(message_body, encode_chunked=encode_chunked)
    ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.13/http/client.py", line 1093, in _send_output
    self.send(msg)
    ~~~~~~~~~^^^^^
  File "/usr/lib/python3.13/http/client.py", line 1037, in send
    self.connect()
    ~~~~~~~~~~~~^^
  File "/usr/lib/python3/dist-packages/urllib3/connection.py", line 276, in connect
    self.sock = self._new_conn()
                ~~~~~~~~~~~~~~^^
  File "/usr/lib/python3/dist-packages/urllib3/connection.py", line 213, in _new_conn
    raise NewConnectionError(
    ^^^^^^^^
urllib3.exceptions.NewConnectionError: <urllib3.connection.HTTPConnection object at 0x7f839d6f90>: Failed to establish a new connection: [Errno 113] No route to host

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/usr/lib/python3/dist-packages/requests/adapters.py", line 667, in send
    resp = conn.urlopen(
    
  File "/usr/lib/python3/dist-packages/urllib3/connectionpool.py", line 841, in urlopen
    retries = retries.increment(
    
  File "/usr/lib/python3/dist-packages/urllib3/util/retry.py", line 519, in increment
    raise MaxRetryError(_pool, url, reason) from reason  # type: ignore[arg-type]
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
urllib3.exceptions.MaxRetryError: HTTPConnectionPool(host='192.168.0.5', port=5001): Max retries exceeded with url: /base (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x7f839d6f90>: Failed to establish a new connection: [Errno 113] No route to host'))

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/usr/lib/python3/dist-packages/flask/app.py", line 1536, in __call__
    return self.wsgi_app(environ, start_response)
           ~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3/dist-packages/flask/app.py", line 1514, in wsgi_app
    response = self.handle_exception(e)
  File "/usr/lib/python3/dist-packages/flask_cors/extension.py", line 176, in wrapped_function
    return cors_after_request(app.make_response(f(*args, **kwargs)))
                                                ~^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3/dist-packages/flask/app.py", line 1511, in wsgi_app
    response = self.full_dispatch_request()
  File "/usr/lib/python3/dist-packages/flask/app.py", line 919, in full_dispatch_request
    rv = self.handle_user_exception(e)
  File "/usr/lib/python3/dist-packages/flask_cors/extension.py", line 176, in wrapped_function
    return cors_after_request(app.make_response(f(*args, **kwargs)))
                                                ~^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3/dist-packages/flask/app.py", line 917, in full_dispatch_request
    rv = self.dispatch_request()
  File "/usr/lib/python3/dist-packages/flask/app.py", line 902, in dispatch_request
    return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)  # type: ignore[no-any-return]
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
  File "/home/wadis3/Documents/medidrone/pi/drone.py", line 26, in main
    resp = session.post('http://' + myIP + ':5001/base', json=coords)
  File "/usr/lib/python3/dist-packages/requests/sessions.py", line 637, in post
    return self.request("POST", url, data=data, json=json, **kwargs)
           ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3/dist-packages/requests/sessions.py", line 589, in request
    resp = self.send(prep, **send_kwargs)
  File "/usr/lib/python3/dist-packages/requests/sessions.py", line 703, in send
    r = adapter.send(request, **kwargs)
  File "/usr/lib/python3/dist-packages/requests/adapters.py", line 700, in send
    raise ConnectionError(e, request=request)
requests.exceptions.ConnectionError: HTTPConnectionPool(host='192.168.0.5', port=5001): Max retries exceeded with url: /base (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x7f839d6f90>: Failed to establish a new connection: [Errno 113] No route to host'))


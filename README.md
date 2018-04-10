# Python Socket Proxy
Python3 HTTP and HTTPS man-in-the-middle proxy that supports a HEAD, POST, PUT, DELETE and CONNECT methods. GET supports only for redirecting to avoid interaction with mozilla detect portal. Proxy reads each request, its data and sends to recipient through sockets.
### Redirection
Add your host and forwarding host into the proxy.ini.
Default redirect hosts:
  - http://google.org -> https://bing.com
  - https://google.com -> https://bing.com
### Installation
```sh
$ git clone https://github.com/vadimk2016/SocketProxy.git
```
### Usage
Start a new terminal with command:
```sh
$ python proxy.py
```
Then set as default proxy in your browser:
```sh
localhost:1234
```
Try to open: https://www.bing.com
Or if you want to test redirection: http://google.org
### Todos
 - Modify a redirect option;
 - Add tests;
 - Add support for Windows.
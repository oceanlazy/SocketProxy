# Python Socket Proxy
Proxy passing through itself traffic. The following modules were used to implement:
  - http.server
  - socket
  - socketserver
### Installation
```sh
$ git clone https://github.com/vadimk2016/socket_web_proxy.git
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
Try to open: www.bing.com
### Todos
 - Modify a redirect option.

   [bing.com]: <https://www.bing.com>
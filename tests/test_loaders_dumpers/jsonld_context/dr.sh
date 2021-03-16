docker run -it --rm -d -p 8000:80 -p 8443:443 --name context_server -v `pwd`/:/usr/share/nginx/html context_server 

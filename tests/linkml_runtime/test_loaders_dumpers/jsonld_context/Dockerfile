FROM nginx

LABEL maintainer="Harold Solbrig <solbrig@jhu.edu>"
LABEL description="Local docker image for loader/dumper testing context"

# Add the application/ld+json to the mime types setting
COPY nginx/mime.types /etc/nginx/mime.types

# Include the various CORS settings and the like into the config file
COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf

# A set of non-signed certificates
COPY nginx/context_server.crt /etc/nginx/certs/context_server.crt
COPY nginx/context_server.key /etc/nginx/certs/context_server.key

# Add vim to the server so we can edit via exec if so desired
RUN apt-get update -y && \
    apt-get install apt-file -y && \
    apt-file update && \
    apt-get install vim -y && \
    rm -rf /var/cache/apk/*

EXPOSE 80 443

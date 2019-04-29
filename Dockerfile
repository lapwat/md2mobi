FROM nginx:alpine AS builder

# nginx:alpine contains NGINX_VERSION environment variable, like so:
ENV NGINX_VERSION 1.15.12
ENV ECHO_VERSION 0.61
ENV LUA_VERSION 0.10.15rc1
ENV UPLOAD_VERSION 2.3.0

# Download sources
RUN wget "http://nginx.org/download/nginx-${NGINX_VERSION}.tar.gz" -O nginx.tar.gz && \
  wget "https://github.com/openresty/echo-nginx-module/archive/v${ECHO_VERSION}.tar.gz" -O echo.tar.gz && \
  wget "https://github.com/openresty/lua-nginx-module/archive/v${LUA_VERSION}.tar.gz" -O lua.tar.gz && \
  wget "https://github.com/fdintino/nginx-upload-module/archive/${UPLOAD_VERSION}.tar.gz" -O upload.tar.gz

# For latest build deps, see https://github.com/nginxinc/docker-nginx/blob/master/mainline/alpine/Dockerfile
RUN apk add --no-cache --virtual .build-deps \
  gcc \
  libc-dev \
  make \
  openssl-dev \
  pcre-dev \
  zlib-dev \
  linux-headers \
  curl \
  gnupg \
  libxslt-dev \
  gd-dev \
  geoip-dev \
  lua \
  lua-dev \
  lua5.3-dev \
  luajit \
  luajit-dev

# Reuse same cli arguments as the nginx:alpine image used to build
RUN CONFARGS=$(nginx -V 2>&1 | sed -n -e 's/^.*arguments: //p') \
  # mkdir /usr/src && \
	tar -zxC /usr/src -f nginx.tar.gz && \
  tar -xzvf "echo.tar.gz" && \
  tar -xzvf "upload.tar.gz" && \
  tar -xzvf "lua.tar.gz" && \
  ECHODIR="$(pwd)/echo-nginx-module-${ECHO_VERSION}" && \
  LUADIR="$(pwd)/lua-nginx-module-${LUA_VERSION}" && \
  UPLOADDIR="$(pwd)/nginx-upload-module-${UPLOAD_VERSION}" && \
  cd /usr/src/nginx-$NGINX_VERSION && \
  ./configure --with-compat $CONFARGS --add-dynamic-module=$ECHODIR --add-dynamic-module=$UPLOADDIR --add-dynamic-module=$LUADIR && \
  make && make install


RUN ls /usr/local/nginx/modules/

FROM nginx:alpine
# Extract the dynamic module NCHAN from the builder image
COPY --from=builder /usr/local/nginx/modules/ngx_http_echo_module.so /usr/local/nginx/modules/ngx_http_echo_module.so
COPY --from=builder /usr/local/nginx/modules/ngx_http_lua_upload_module.so /usr/local/nginx/modules/ngx_http_lua_module.so
COPY --from=builder /usr/local/nginx/modules/ngx_http_upload_module.so /usr/local/nginx/modules/ngx_http_upload_module.so

RUN rm /etc/nginx/conf.d/default.conf

# COPY nginx.conf /etc/nginx/nginx.conf
# COPY default.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
STOPSIGNAL SIGTERM
CMD ["nginx", "-g", "daemon off;"]

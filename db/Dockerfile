FROM mdillon/postgis:11

# download directory
RUN mkdir data
WORKDIR /data

# copy build script
ADD ./create.sh /docker-entrypoint-initdb.d/z_create.sh
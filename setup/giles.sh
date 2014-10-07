# bash script to setup environment on Ubuntu 14.04 for giles

sudo apt-get install golang git mongodb

git clone https://github.com/gtfierro/giles
cd giles/giles
go get code.google.com/p/goprotobuf/proto
go get github.com/bitly/go-simplejson
go get github.com/gorilla/mux
go get gopkg.in/mgo.v2
go get gopkg.in/mgo.v2/bson
go build

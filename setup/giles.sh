# bash script to setup environment on Ubuntu 14.04 for giles

sudo add-apt-repository ppa:cal-sdb/smap
sudo apt-get update
sudo apt-get install -y golang git mongodb mercurial libprotobuf-dev readingdb python-pip

cd
export GOPATH=`pwd`/go
git clone https://github.com/gtfierro/giles
cd giles/giles
go get code.google.com/p/goprotobuf/proto
go get github.com/bitly/go-simplejson
go get github.com/gorilla/mux
go get gopkg.in/mgo.v2
go get gopkg.in/mgo.v2/bson
go build

# supervisor file

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
cat <<EOF > giles.conf
[program:giles]
command = /home/$USER/giles/giles/giles
directory = /home/$USER/giles/giles
priority = 90
autorestart = true
stdout_logfile = /var/log/giles.stdout.log
stdout_logfile_maxbytes = 50MB
stdout_logfile_backups = 5
stderr_logfile = /var/log/giles.stderr.log
stderr_logfile_maxbytes = 50MB
stderr_logfile_backups = 5

[program:mongo]
command = mongod --dbpath=/tmp
directory = /home/$USER/giles/giles
priority = 2
autorestart = true
stdout_logfile = /var/log/mongo.stdout.log
stdout_logfile_maxbytes = 50MB
stdout_logfile_backups = 5
stderr_logfile = /var/log/mongo.stderr.log
stderr_logfile_maxbytes = 50MB
stderr_logfile_backups = 5
EOF

sudo service mongo stop
sudo mv giles.conf /etc/supervisor/conf.d/giles.conf
sudo supervisorctl update

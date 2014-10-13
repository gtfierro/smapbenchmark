import boto.ec2
from configobj import ConfigObj
import time

config = ConfigObj('aws.ini')['aws']
print config
AWS_SECRET_ACCESS_KEY=config['AWS_SECRET_ACCESS_KEY']
AWS_ACCESS_KEY=config['AWS_ACCESS_KEY']
smap_ami = config['image_id']
key_name = config['key_name']
instance_type = config['instance_type']
security_group_ids = config['security_group_ids']
if not isinstance(security_group_ids, list):
    security_group_ids = [security_group_ids]
subnet_id = config['subnet_id']
region = config['region']

conn = boto.ec2.connect_to_region(region,
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

def create_security_group(conn):
    allopen = conn.create_security_group('allopen','All ports open')
    allopen.authorize('tcp',1,65535, '0.0.0.0/0')
    allopen.authorize('udp',1,65535, '0.0.0.0/0')

def get_instance(conn, ami, key, instance, security_groups, subnet):
    reservation = conn.run_instances(ami, key_name=key, instance_type=instance, security_group_ids=security_groups, subnet_id=subnet_id)
    instance = reservation.instances[0]
    instance.update()
    while instance.state == 'pending':
        print instance,instance.state,instance.ip_address
        time.sleep(5)
        instance.update()
    print 'GOT ip', instance, instance.state, instance.ip_address
    return instance

def create_some(num):
    ips = []
    for i in range(num):
        instance = get_instance(conn, smap_ami, key_name, instance_type, security_group_ids, subnet_id)
        ips.append(instance.ip_address)
    return ips

if __name__ == '__main__':
    import sys
    num = int(sys.argv[1])
    ips = create_some(num)
    with open('ips.csv','w+') as f:
        for ip in ips:
            f.write(ip+'\n')

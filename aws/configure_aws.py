import boto.ec2
from configobj import ConfigObj

config = ConfigObj('aws.ini')['aws']
print config
AWS_SECRET_ACCESS_KEY=config['aws']['AWS_SECRET_ACCESS_KEY']
AWS_ACCESS_KEY=config['aws']['AWS_ACCESS_KEY']
smap_ami = config['aws']['image_id']
key_name = config['aws']['key_name']
instance_type = config['aws']['instance_type']
security_group_ids = list(config['aws']['security_group_ids'])
subnet_id = config['aws']['subnet_id']
region = config['aws']['region']

#conn = boto.ec2.connect_vpc('vpc-3547ab50',
conn = boto.ec2.connect_to_region(region,
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

def create_security_group(conn):
    allopen = conn.create_security_group('allopen','All ports open')
    allopen.authorize('tcp',1,65535, '0.0.0.0/0')
    allopen.authorize('udp',1,65535, '0.0.0.0/0')

def get_instance(conn, ami, key, instance, security_groups, subnet):
    reservation = conn.run_instances(ami, key_name=key, instance_type=instance, security_group_ids=security_groups, subnet_id=subnet_id)
    return reservation.instances

def assign_ip(conn, instance):
    a = conn.allocate_address('vpc')
    try:
        a.associate(instance.id)
    except Exception as e:
        a.release()
    return a

def create_some(num):
    ips = []
    for i in range(num):
        instance = get_instance(conn, smap_ami, key_name, instance_type, security_group_ids, subnet_id)[0]
        a = assign_ip(conn, instance)
        ips.append(a.public_ip)
        print a.public_ip
    return ips

if __name__ == '__main__':
    import sys
    num = int(sys.argv[1])
    ips = create_some(num)
    with open('ips.csv','a+') as f:
        for ip in ips:
            f.write(ip+'\n')

import sys
import boto3
import ipaddress
from typing import List

USAGE = """
**USAGE**
python describe_unused_ips.py {vpc-id} [lb]
"""

ec2_client = boto3.client("ec2")


def main(vpc_id: str, mode: str):
    print(f"{vpc_id=} {mode=}")

    # get subnets
    subnets = get_subnets(vpc_id)

    # initialize counters
    total_reserved_ips = 0
    total_unused_ips = 0
    total_ips = 0

    # process each subnet
    for subnet_id in subnets:
        print(f"\nProcessing subnet: {subnet_id}")
        subnet_reserved_ips, subnet_unused_ips = process_subnet(subnet_id, mode)

        # accumulate counters
        total_reserved_ips += subnet_reserved_ips
        total_unused_ips += subnet_unused_ips
        total_ips += (subnet_reserved_ips + subnet_unused_ips)

    # print overall statistics
    print("\nOverall Statistics:")
    print(f"Total Reserved IPs: {total_reserved_ips}")
    print(f"Total Unused IPs: {total_unused_ips}")
    print(f"Total IPs: {total_ips}")


def process_subnet(subnet_id: str, mode: str):
    # get cidr ips
    cidr = get_cidr(subnet_id)
    cidr_ips = sorted(map(str, ipaddress.IPv4Network(cidr)))

    # extract reserved ips
    reserved_ips = sorted(cidr_ips[:4] + [cidr_ips[-1]])

    # get used ips
    used_ips = get_used_ips(subnet_id)
    used_ips.sort()

    # extract unused ips
    unused_ips = sorted(set(cidr_ips) - set(used_ips) - set(reserved_ips))

    # output
    print(f"{cidr=}")
    print_list("cidr_ips", cidr_ips, mode)
    print("-----------")
    print_list("reserved_ips", reserved_ips, mode)
    print("-----------")
    print_list("used_ips", used_ips, mode)
    print("-----------")
    print_list("unused_ips", unused_ips, mode)
    print("-----------")
    print(f"cidr={cidr} cidr_ips={len(cidr_ips)} reserved={len(reserved_ips)} used={len(used_ips)} unused={len(unused_ips)}")

    # return counts for the subnet
    return len(reserved_ips), len(unused_ips)


def print_list(label: str, target_list: List, mode: str):
    if mode == "lb":
        print(f"{label}=")
        for t in target_list:
            print(f"{t}")
    else:
        print(f"{label}={target_list}")


def get_cidr(subnet_id: str) -> str:
    response = ec2_client.describe_subnets(SubnetIds=[subnet_id])
    return response['Subnets'][0]['CidrBlock']


def get_used_ips(subnet_id: str) -> List[str]:
    response = ec2_client.describe_network_interfaces(Filters=[{'Name': 'subnet-id', 'Values': [subnet_id]}])
    private_ips = [ip['PrivateIpAddress'] for nw_if in response.get('NetworkInterfaces', []) for ip in nw_if.get('PrivateIpAddresses', [])]
    return private_ips


def get_subnets(vpc_id: str) -> List[str]:
    response = ec2_client.describe_subnets(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])
    return [subnet['SubnetId'] for subnet in response.get('Subnets', [])]


if __name__ == '__main__':
    args = sys.argv
    if 2 <= len(args) <= 3:
        main(vpc_id=args[1], mode=args[2] if len(args) == 3 else "normal")
        sys.exit(0)
    else:
        print("incorrect argument")
        print(USAGE)
        sys.exit(1)

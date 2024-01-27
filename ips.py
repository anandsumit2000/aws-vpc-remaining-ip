import sys
import boto3
import ipaddress
from typing import List


ec2_client = boto3.client("ec2")


def main(subnet_id: str):
    print(f"{subnet_id=}")

    # get cidr ips
    cidr = get_cidr(subnet_id)
    cidr_ips = sorted(map(str, ipaddress.IPv4Network(cidr)))

    # extract reserved ips
    reserved_ips = cidr_ips[0:4] + [cidr_ips[-1]]

    # get used ips
    used_ips = get_used_ips(subnet_id)
    used_ips.sort()

    # extract unused ips
    unused_ips = sorted(set(cidr_ips) - set(used_ips) - set(reserved_ips))

    # output
    print(f"{cidr=}")
    print_list("cidr_ips", cidr_ips)
    print("-----------")
    print_list("reserved_ips", reserved_ips)
    print("-----------")
    print_list("used_ips", used_ips)
    print("-----------")
    print_list("unused_ips", unused_ips)
    print("-----------")
    print(f"cidr={cidr} cidr_ips={len(cidr_ips)} reserved={len(reserved_ips)} used={len(used_ips)} unused={len(unused_ips)}")


def print_list(label: str, target_list: List):
    print(f"{label}=")
    for t in target_list:
        print(f"{t}")


def get_cidr(subnet_id: str) -> str:
    response = ec2_client.describe_subnets(SubnetIds=[subnet_id])
    return response['Subnets'][0]['CidrBlock']


def get_used_ips(subnet_id: str) -> List[str]:
    response = ec2_client.describe_network_interfaces(Filters=[{'Name': 'subnet-id', 'Values': [subnet_id]}])
    private_ips = [ip['PrivateIpAddress'] for nw_if in response.get('NetworkInterfaces', []) for ip in nw_if.get('PrivateIpAddresses', [])]
    return private_ips


if __name__ == '__main__':
    args = sys.argv
    if len(args) == 2:
        main(subnet_id=args[1])
        sys.exit(0)

    else:
        print("incorrect argument")
        sys.exit(1)
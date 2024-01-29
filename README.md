# Describe Unused IPs in AWS
## For sysadmins and SREs to identify the number of unused IPs


`ips.py` is a Python script designed to assist AWS users in identifying and listing unused IP addresses within all subnets in the specified VPC . By analyzing subnets in VPC, the CIDR block of the subnet, the script provides detailed information on reserved, used, and unused IP addresses.

## Prerequisites
Ensure you have the following prerequisites before running the script:
- Python >=3.10
- Boto3 library (pip3 install boto3=1.16.0)

## Usage
Export the AWS credentials to your working terminal.
```bash
export AWS_ACCESS_KEY_ID={access_key}
export AWS_SECRET_ACCESS_KEY={secret_key}
export AWS_DEFAULT_REGION={region name}
```
Run:
```bash
python describe_unused_ips.py {vpc-id}
```
- {vpc-id}: The ID of the VPC you want to analyze.


## Output
The script generates the following outputs:

- cidr_ips: All IP addresses in the subnet's CIDR block.
- reserved_ips: The first four and the last IP addresses in the CIDR block, which are reserved and cannot be assigned to instances.
- used_ips: IP addresses currently in use by instances in the subnet.
- unused_ips: IP addresses available for assignment in the subnet.

The output includes counts for each category and overall CIDR block information.

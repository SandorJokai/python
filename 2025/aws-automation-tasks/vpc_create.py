import boto3
import warnings
from boto3.exceptions import PythonDeprecationWarning
from botocore.exceptions import ClientError

warnings.filterwarnings("ignore", category=PythonDeprecationWarning)

ec2 = boto3.client('ec2')
vpc_name = 'vpc-with-python'
ig_name = 'ig-with-python'


def get_or_create_vpc(ec2, name):
    response = ec2.describe_vpcs(
        Filters=[{'Name': 'tag:Name', 'Values': [name]}]
    )
    vpcs = response.get('Vpcs', [])

    if vpcs:
        vpc_id = vpcs[0]['VpcId']
        print(f"VPC '{name}' - '{vpc_id}' is already exists, nothing to do.")
        return vpcs[0]['VpcId']

    try:
        vpc_response = ec2.create_vpc(
                CidrBlock='10.0.0.0/16',
                TagSpecifications=[{
                    'ResourceType': 'vpc',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': name,
                        },
                    ],
                }],
        )
        vpc_id = vpc_response['Vpc']['VpcId']
        print(f"VPC '{vpc_name}' with ID '{vpc_id}' has been created.")
    
    except ClientError as e:
        print(f"Failed to create VPC '{name}': {e.response['Error']['Message']}")


def add_internet_access(ec2, name, vpc_id):
    response = ec2.describe_internet_gateways(
        Filters=[{'Name': 'tag:Name', 'Values': [name]}]
    )
    ig = response.get('InternetGateways', [])

    if not ig:
        response = ec2.create_internet_gateway(
        TagSpecifications=[
            {
                'ResourceType': 'internet-gateway',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': name
                    },
                ]
            },
        ])
        print(f"Internet gateway '{name}' has been created.")

    elif ig and not ig[0]['Attachments']:
        ig_id = ig[0]['InternetGatewayId']
        ec2.attach_internet_gateway(VpcId=vpc_id, InternetGatewayId=ig_id)
        print(f"The gateway '{name}' has successfully got access to the internet.")

    else:
        print(f"The gateway '{name}' has already got access to the internet.")
        return ig[0]


if __name__ == "__main__":
    result = get_or_create_vpc(ec2, vpc_name)
    print(result)
    add_internet_access(ec2, ig_name, result)

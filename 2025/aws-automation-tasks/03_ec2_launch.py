import boto3
import warnings
from boto3.exceptions import PythonDeprecationWarning
from botocore.exceptions import ClientError

warnings.filterwarnings("ignore", category=PythonDeprecationWarning)

ec2 = boto3.resource('ec2')
instance_name = 'my-linux-node'

instances = list(ec2.instances.filter(
    Filters=[{'Name': 'tag:Name', 'Values': [instance_name]}]
))

if instances:
    instance_id = instances[0].id
    print(f"The instance '{instance_name}' with ID '{instance_id}' already exists!")

else:
    try:
        new_instance = ec2.create_instances(
            ImageId = 'ami-0cae6d6fe6048ca2c',
            InstanceType ='t3.micro',
            MinCount = 1,
            MaxCount = 1,
            SecurityGroups = [
                'WebAccess'
            ],
            Placement = {
                'AvailabilityZone': 'us-east-1a',
            },
            TagSpecifications = [ {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': instance_name,
                    },
                ],
            },
        ])
        print(f"{instance_name} has been created successfully!")
    
    except ClientError as e:
        print(f"Error occurred: {e}")


## Stopping the instance
ec2.instances.filter(InstanceIds=instance_id.split()).stop()
print(f"Instance '{instance_name}'-'{instance_id}' stopped.")

## And terminate
ec2.instances.filter(InstanceIds=instance_id.split()).terminate()
print(f"Instance '{instance_name}'-'{instance_id}' has been terminated.")

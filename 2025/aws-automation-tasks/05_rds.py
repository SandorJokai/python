import boto3
import warnings
import os
import time
from boto3.exceptions import PythonDeprecationWarning
from botocore.exceptions import ClientError

warnings.filterwarnings("ignore", category=PythonDeprecationWarning)

rds       = boto3.client('rds')
db_name   = 'mydb-via-boto3'
db_subnet = 'vpc-with-python'
password  = os.getenv('EXCH_API')
cluster   = 'db-cluster-01'
username  = 'db_user01'


## Creating a cluster is not eligible for Free tier account...
def check_or_create_cluster(rds, db_name, username, password, db_subnet, cluster) -> bool:
    try:
        response = rds.describe_db_clusters(DBClusterIdentifier=cluster)
        print(f"Cluster - '{cluster}' already exists. Skipping creation.")

    except rds.exceptions.DBClusterNotFoundFault:
        rds.create_db_cluster(
                DBClusterIdentifier=cluster,
                AvailabilityZones=[
                    'us-east-1a',
                ],
                DatabaseName=db_name,
                DBSubnetGroupName=db_subnet,
                EngineMode='serverless',
                EnableHttpEndpoint=True,
                Engine='mysql',
                EngineVersion='5.7.mysql_aurora.2.08.3',
                MasterUsername=username,
                MasterUserPassword=password,
                ScalingConfiguration={
                    'MinCapacity': 1,
                    'MaxCapacity': 1,
                    'AutoPause': True,
                    'SecondsUntilAutoPause': 300,
                },
            )
        print(f"Cluster - '{cluster}' has successfully been created.")
        return True


def create_or_check_database(rds, db_name, username, password) -> bool:
    try:
        response = rds.describe_db_instances(DBInstanceIdentifier=db_name)
        print(f"Database - '{db_name}' already exists. Skipping creation.")

    except rds.exceptions.DBInstanceNotFoundFault:
        rds.create_db_instance(
            DBInstanceIdentifier=db_name,
            AllocatedStorage=20,
            DBInstanceClass='db.t3.micro',
            Engine='mysql',
            MasterUsername=username,
            MasterUserPassword=password,
            PubliclyAccessible=True,
            BackupRetentionPeriod=1
        )
        print(f"Database - '{db_name}' has successfully been created.")

        while True:
            response = rds.describe_db_instances(DBInstanceIdentifier=db_name)
            status = response['DBInstances'][0]['DBInstanceStatus']
            print(f"Current status of the db is: '{status}'")

            if status == 'available':
                break

            print("Waiting for the db to be available...\n")
            time.sleep(60)

        return True


def scaling_db(rds, db_name) -> True:
    rds.modify_db_instance(
        DBInstanceIdentifier=db_name,
        ScalingConfiguration={
            'MinCapacity': 1,
            'MaxCapacity': 2,
            'AutoPause': True,
            'SecondsUntilAutoPause': 600,
        },
    )
    print(f"Database - '{db_name}' has been scaled.")
    return True


def delete_db(rds, db_name) -> True:
    rds.delete_db_instance(
        DBInstanceIdentifier=db_name,
        SkipFinalSnapshot=True,
    )
    print(f"Database - '{db_name}' is being deleted...")
    return True


if __name__ == "__main__":
#    check_or_create_cluster(rds, db_name, username, password, db_subnet, cluster)
    create_or_check_database(rds, db_name, username, password)
#    scaling_db(rds, db_name)
#    delete_db(rds, db_name)

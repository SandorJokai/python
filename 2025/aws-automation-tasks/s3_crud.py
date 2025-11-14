import boto3
import warnings
from boto3.exceptions import PythonDeprecationWarning

warnings.filterwarnings("ignore", category=PythonDeprecationWarning)

s3 = boto3.resource('s3')
bucket_name = 'new-bucket-lunched-with-python-2'

all_my_buckets = [bucket.name for bucket in s3.buckets.all()]

## Task 1 - Check whether the new bucket is already existing, create if its not
if bucket_name not in all_my_buckets:
    print(f"'{bucket_name}' bucket is not existing yet, creating now...")
    s3.create_bucket(
            Bucket = bucket_name,
## Uncomment this we can configure the AZ, but us#east#1 is the default without it.
#           CreateBucketConfiguration = {
#               'LocationConstraint': 'us#east#1'
#           }
        )

    print(f"'{bucket_name}' bucket created successfully.\n")
else:
    print(f"'{bucket_name}' already exists\n")


## Task 2 - Upload file_1.txt & file_2.txt

s3 = boto3.client('s3')
file_list = ['file_1.txt', 'file_2.txt']
for files in file_list:
    print(f"Uploading {files} to {bucket_name} bucket...")
    s3.upload_file(files, bucket_name, files)
print(f"Files {file_list} been successfully uploaded onto '{bucket_name}'.\n")


## Task 3 - Getting the object
print("Getting S3 object...")
response = s3.get_object(Bucket=bucket_name,
                         Key='file_1.txt')
print("Done, response body:")
print(response['Body'].read())


## Task 4 - Let's update the content of file_1 with file_2 (both files will be duplicates eventually)
print(f"\nUpdating the content of {file_list[0]} with {file_list[1]}...")
response = s3.put_object(Bucket=bucket_name, Body=open(file_list[1], 'rb'), Key='file_1.txt')


## Task 5 - Finally delete the contents as well as the bucket
print(f"Delete {file_list} from {bucket_name}...\n")
response = s3.delete_objects(
    Bucket=bucket_name,
    Delete={
        'Objects': [
            {
                'Key': 'file_1.txt'
            },
            {
                'Key': 'file_2.txt'
            }
            ]
        }
    )

print(f"Delete {bucket_name} bucket...\n")
response = s3.delete_bucket(
    Bucket=bucket_name,
)

import json
import urllib.parse
import boto3

print('Loading function')

s3 = boto3.client('s3')
ecs = boto3.client('ecs')

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    try:
        print("Uploaded file path: " + key)
        response = ecs.run_task(
        cluster='airbnb-ecs-cluster',
        launchType = 'FARGATE',
        taskDefinition='s3-to-rds-postgresql-pandas-td:3',
        count = 1,
        platformVersion='LATEST',
        networkConfiguration={
            'awsvpcConfiguration': {
                'subnets': [{{your_subnets}}],
                'securityGroups': [{{your_security_groups}}],
                'assignPublicIp': 'ENABLED'
            }
        },
        overrides={
                'containerOverrides': [
                    {
                        'name': 's3-to-rds-postgresql-pandas',
                        'environment': [
                            {
                                'name': 'S3_URI',
                                'value': 's3://{bucket}/{key}'.format(bucket=bucket,key=key)
                            },
                        ]
                    }
                ]
            }
        )
        return str(response)
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
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
        cluster='paidy-cluster',
        launchType = 'FARGATE',
        taskDefinition='paidy-task-def:1',
        count = 1,
        platformVersion='LATEST',
        networkConfiguration={
            'awsvpcConfiguration': {
                'subnets': ["subnet-0ec6a6b671f7099cc", "subnet-08da40cc786f105e2"],
                'securityGroups': ["sg-0343195d1821d1833"],
                'assignPublicIp': 'ENABLED'
            }
        },
        overrides={
                'containerOverrides': [
                    {
                        'name': 'paidy-container',
                        'environment': [
                            {
                                'name': 'S3_URI',
                                'value': 's3://{bucket}/{key}'.format(bucket=bucket,key=key)
                            },
                        ]
                    }
                ],
                'executionRoleArn': 'arn:aws:iam::456668253361:role/ecsTaskExecutionRole',
                'taskRoleArn': 'arn:aws:iam::456668253361:role/ecsTaskExecutionRole'
            }
        )
        return str(response)
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
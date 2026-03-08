import json
import boto3

ssm = boto3.client('ssm')
iam = boto3.client('iam')

WHITELISTED_USERS = ["Demo-USer"]

DENY_POLICY = json.dumps({
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Deny",
            "Action": "*",
            "Resource": "*"
        }
    ]
})

def lambda_handler(event, context):
    print("Received event:", json.dumps(event))

    try:
        username = event["detail"]["requestParameters"]["userName"]
        access_key_id = event["detail"]["responseElements"]["accessKey"]["accessKeyId"]

        print(f"User: {username}")
        print(f"AccessKeyId: {access_key_id}")

        response = ssm.start_automation_execution(
            DocumentName="disablenewaccesskey",
            Parameters={
                "UserName": [username],
                "AccessKeyId": [access_key_id],
                "AutomationAssumeRole": ["arn:aws:iam::326963733272:role/ssm-main-role"]
            }
        )
        print("Automation started:", response)

        if username not in WHITELISTED_USERS:
            iam.put_user_policy(
                UserName=username,
                PolicyName="QuarantinePolicy",
                PolicyDocument=DENY_POLICY
            )
            print(f"User {username} quarantined successfully!")
        else:
            print(f"User {username} is whitelisted, skipping quarantine!")

        return {
            "statusCode": 200,
            "body": "Automation triggered successfully"
        }

    except Exception as e:
        print("Error:", str(e))
        raise e

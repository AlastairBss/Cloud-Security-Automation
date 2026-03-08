# Cloud Security Monitoring & Automated Response System

## Overview
Automated cloud security response system that detects suspicious IAM activity 
in real-time using AWS CloudTrail and EventBridge, automatically disabling 
compromised access keys and quarantining affected users through Lambda and 
SSM Automation — reducing response time from hours to seconds.

## Architecture
CloudTrail → EventBridge → Lambda → SSM Automation → IAM → SNS

## What it does
- Detects when a new IAM access key is created via CloudTrail
- EventBridge triggers a Lambda function automatically
- Lambda extracts the username and access key ID
- SSM Automation disables the access key immediately
- Quarantine policy is attached to the user (Deny All)
- CloudWatch alarm sends email alert via SNS

## Services Used
- AWS CloudTrail
- Amazon EventBridge
- AWS Lambda (Python 3.12)
- AWS Systems Manager (SSM Automation)
- AWS IAM
- Amazon CloudWatch
- Amazon SNS

## Security Features
- Automatic access key disabling
- User quarantine (Deny All policy)
- Whitelisted trusted users
- Email alerts via SNS
- CloudWatch monitoring and alarms

## Challenges Faced
- **EventBridge Input Transformer** was passing JSONPath as literal strings 
  instead of resolving actual values from the CloudTrail event
- **Lambda not triggering** — discovered no EventBridge trigger was configured 
  in the Lambda function
- **Python 3.14 Durable Execution** — auto-enabled on Python 3.14 which 
  blocked normal Lambda invocations, fixed by switching to Python 3.12
- **Missing IAM permissions** — Lambda role was missing `ssm:StartAutomationExecution` 
  and `iam:PassRole` permissions, debugged using CloudWatch logs
- **Quarantine policy locked out main user** — implemented a whitelist to 
  protect trusted admin users from being quarantined
- **CloudWatch metric filter** — `?` prefix and case sensitivity caused 
  metric filters to not match log lines correctly

## Demo
https://drive.google.com/file/d/1BzDT_gk3IVnnjTJhEWhKdDp-NAGg4Bvt/view?usp=sharing

## Setup
1. Enable CloudTrail in your AWS account
2. Create SSM Automation document
3. Deploy Lambda function with required IAM permissions
4. Create EventBridge rule targeting Lambda
5. Set up SNS topic and CloudWatch alarms

## IAM Permissions Required
- Lambda role: `ssm:StartAutomationExecution`, `iam:PassRole`, `iam:PutUserPolicy`
- SSM role: `iam:UpdateAccessKey`

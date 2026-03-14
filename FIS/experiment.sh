aws fis create-experiment-template \
    --cli-input-json '{
        "actions": {
                "test-multiregion": {
                        "actionId": "aws:ec2:stop-instances",
                        "parameters": {
                                "startInstancesAfterDuration": "PT7M"
                        },
                        "targets": {
                                "Instances": "Instances-Target-1"
                        }
                }
        },
        "description": "test-multiregion",
        "experimentOptions": {
                "accountTargeting": "single-account",
                "emptyTargetResolutionMode": "fail"
        },
        "roleArn": "arn:aws:iam::XYZ:role/fis-ec2-stop-role",
        "stopConditions": [
                {
                        "source": "none"
                }
        ],
        "tags": {
                "Name": "test-multiregion"
        },
        "targets": {
                "Instances-Target-1": {
                        "resourceArns": [
                                "arn:aws:ec2:us-east-1:XYZ:instance/i-0bd0234125d25404c",
                                "arn:aws:ec2:us-east-1:XYZ:instance/i-0f02c47dabe59f7cb"
                        ],
                        "resourceType": "aws:ec2:instance",
                        "selectionMode": "ALL"
                }
        }
}'

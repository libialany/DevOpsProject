


```

aws cloudformation create-stack     --stack-name 'cloudformation-lambda'     --capabilities CAPABILITY_IAM     --template-body file://$(pwd)/cloudformation-lambda.yaml
aws cloudformation wait     stack-create-complete     --stack-name 'cloudformation-lambda'
aws cloudformation delete-stack     --stack-name 'cloudformation-lam
bda'

```
## CDK Python  Lambda

```
cdk ls   
cdk synth
cdk deploy
```

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
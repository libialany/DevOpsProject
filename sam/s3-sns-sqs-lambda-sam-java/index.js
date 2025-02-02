// Iac/s3-sns-sqs-lambda-sam-java/src/main/javascript/FileAudit.js
const AWS = require('aws-sdk');

exports.handler = async (event) => {
    event.Records.forEach(record => {
        console.log(record.Sns.Message);
    });
    return "Done";
};
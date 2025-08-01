import boto3
import sys

def main():
    sns_client = boto3.client('sns')

    # subscription_counts_by_topic_arn = {}

    # List topics
    paginator = sns_client.get_paginator('list_topics')
    try:
        for page in paginator.paginate():
            for topic in page.get('Topics', []):
                topic_arn = topic['TopicArn']
                subscription_counts_by_topic_arn[topic_arn] = 0
    except Exception as e:
        print(f"Error describing topics: {e}")
        sys.exit(1)

    # List subscriptions
    paginator = sns_client.get_paginator('list_subscriptions')
    try:
        for page in paginator.paginate():
            for subscription in page.get('Subscriptions', []):
                topic_arn = subscription.get('TopicArn')
                if topic_arn in subscription_counts_by_topic_arn:
                    subscription_counts_by_topic_arn[topic_arn] += 1
    except Exception as e:
        print(f"Error describing subscriptions: {e}")
        sys.exit(1)

    # Print topic ARNs with 0 subscriptions
    for topic_arn in sorted(subscription_counts_by_topic_arn.keys()):
        if subscription_counts_by_topic_arn[topic_arn] == 0:
            print(topic_arn)

if __name__ == "__main__":
    main()
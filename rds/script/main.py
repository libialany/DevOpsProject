import sys
import boto3
import datetime
import time

def get_log_events(log_group_name, start_time_str, end_time_str):
    print(f"🔹 Log Group: {log_group_name}")
    start_time = int(datetime.datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S").timestamp() * 1000)
    end_time = int(datetime.datetime.strptime(end_time_str, "%Y-%m-%d %H:%M:%S").timestamp() * 1000)

    logs_client = boto3.client('logs')

    
    paginator = logs_client.get_paginator('describe_log_streams')
    streams_iterator = paginator.paginate(
        logGroupName=log_group_name,
        orderBy='LastEventTime',
        descending=True
    )

    matching_streams = []

    for page in streams_iterator:
        for stream in page['logStreams']:
            
            if 'lastEventTimestamp' in stream and (
                stream['lastEventTimestamp'] >= start_time or
                stream['firstEventTimestamp'] <= end_time
            ):
                matching_streams.append(stream['logStreamName'])

    print(f"\nFound {len(matching_streams)} matching log stream(s). Fetching logs...\n")

    
    for stream_name in matching_streams:
        print(f"🔹 Log Stream: {stream_name}")
        next_token = None

        while True:
            kwargs = {
                'logGroupName': log_group_name,
                'logStreamName': stream_name,
                'startTime': start_time,
                'endTime': end_time,
                'startFromHead': True
            }
            if next_token:
                kwargs['nextToken'] = next_token

            response = logs_client.get_log_events(**kwargs)

            for event in response['events']:
                timestamp = datetime.datetime.fromtimestamp(event['timestamp'] / 1000.0)
                print(f"{timestamp} — {event['message'].strip()}")

            if 'nextForwardToken' in response and next_token != response['nextForwardToken']:
                next_token = response['nextForwardToken']
            else:
                break

        print("------ End of Stream ------\n")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script/main.py <start_date> <end_date>")
        sys.exit(1)

    log_group = "/aws/rds/instance/my-rds-instance/postgresql"
    start_date = sys.argv[1]
    end_date = sys.argv[2]

    get_log_events(log_group, start_date, end_date)
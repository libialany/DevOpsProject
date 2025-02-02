
def handler(event, context):
    print("File Content")
    print("----------------")
    f = open("/mnt/efs/datetime.txt", "r")
    msg = str(f.read())
    return {
        'statusCode': 200,
        'body': msg
    }
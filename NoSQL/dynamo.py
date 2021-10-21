import boto3
import csv

s3 = boto3.resource('s3', aws_access_key_id='access_key', aws_secret_access_key='secret_key')

# try:
    # s3.create_bucket(Bucket='exp-oct2021-navyashree', CreateBucketConfiguration={'LocationConstraint': 'us-east-2'})
# except Exception as e:
    # print ("Bucket exception!!")
    # print (e)

bucket = s3.Bucket("exp-oct2021-navyashree")
bucket.Acl().put(ACL='public-read')

body = open('D:\\14848-CloudInfra\\Assignment1\\NoSQL\\datafiles\\experiments.csv', 'rb')
o = s3.Object('exp-oct2021-navyashree', 'test').put(Body=body )
s3.Object('exp-oct2021-navyashree', 'test').Acl().put(ACL='public-read')

dyndb = boto3.resource('dynamodb',
    region_name='us-east-2',
    aws_access_key_id='access_key',
    aws_secret_access_key='secret_key'
)

try:
    table = dyndb.create_table(
        TableName='DataTable',
        KeySchema=[
            {
                'AttributeName': 'PartitionKey',
                'KeyType': 'HASH'
            },
            {
                'AttributeName': 'RowKey',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'PartitionKey',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'RowKey',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
except Exception as e:
    print (e)
    #if there is an exception, the table may already exist. if so...
    table = dyndb.Table("DataTable")

#wait for the table to be created
table.meta.client.get_waiter('table_exists').wait(TableName='DataTable')

print(table.item_count)

with open('D:\\14848-CloudInfra\\Assignment1\\NoSQL\\datafiles\\experiments.csv', 'r') as csvfile:
    csvf = csv.reader(csvfile, delimiter=',', quotechar='|')
    next(csvf)
    for item in csvf:
        print(item)
        body = open('D:\\14848-CloudInfra\\Assignment1\\NoSQL\\datafiles\\'+item[4], 'rb')
        s3.Object('exp-oct2021-navyashree', item[4]).put(Body=body)
        md = s3.Object('exp-oct2021-navyashree', item[4]).Acl().put(ACL='public-read')
        url = " https://s3-us-east-2.amazonaws.com/exp-oct2021-navyashree/"+item[4]
        metadata_item = {'PartitionKey': item[0], 'RowKey': item[1],
        'description' : item[4], 'date' : item[2], 'url':url}
        try:
            table.put_item(Item=metadata_item)
        except:
            print ("item may already be there or another failure")

response = table.get_item(
    Key={
    'PartitionKey': '1',
    'RowKey': '-1'
    }
)
print(response)

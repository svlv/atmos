#!/bin/python

import boto3

session = boto3.session.Session()

s3 = session.resource(
    service_name='s3',
    endpoint_url='https://ewr1.vultrobjects.com',
)

bucket = s3.Bucket("atmos-timelapse")
f = open('index.html', 'w')
videos=""
for obj in bucket.objects.filter():
    url = f'http://{bucket.name}.ewr1.vultrobjects.com/{obj.key}'
    videos += f"""
<video width="320" height="240" controls>
  <source src="{url}" type="video/mp4">
</video>
    """

f.write(f"""<!DOCTYPE html>
<html>
<head>
<title>Timelapse</title>
</head>
<body>
{videos}
</body>
</html>""")
f.close()

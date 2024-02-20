import os
import boto3
from PIL import Image

s3 = boto3.client('s3')

def resize_image(event, context):
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']
    
    # Download the image from S3
    download_path = '/tmp/{}'.format(object_key)
    s3.download_file(bucket_name, object_key, download_path)
    
    # Resize the image
    with Image.open(download_path) as image:
        resized_image = image.resize((300, 300))  # Adjust dimensions as needed
    
    # Save the resized image to a temporary file
    resized_path = '/tmp/resized_{}'.format(object_key)
    resized_image.save(resized_path)
    
    # Upload the resized image back to S3
    resized_key = 'resized/{}'.format(object_key)
    s3.upload_file(resized_path, bucket_name, resized_key)
    
    return {
        'statusCode': 200,
        'body': 'Image resized successfully'
    }


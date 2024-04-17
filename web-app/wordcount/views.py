from django.shortcuts import render
from django.conf import settings
import boto3

def index(request):
    # An empty string is created for messages
    upload_message = ""
    file_content = ""
    file_name = ""

    if request.method == "POST":
        action = request.POST.get('action')

        if action == "upload" and request.FILES["uploaded_file"]:
            uploaded_file = request.FILES["uploaded_file"]
            file_name = uploaded_file.name
            
            # Prepare file to be uploaded to AWS S3
            s3_client = boto3.client('s3',
                                     aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                     aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
            bucket_name = settings.AWS_STORAGE_BUCKET_NAME
            file_key = file_name

            # Upload file to S3
            try:
                s3_client.upload_fileobj(uploaded_file, bucket_name, file_key)
                upload_message = "The file has been uploaded successfully!"
            except Exception as e:
                upload_message = "An error occurred while uploading the file: {}".format(str(e))
        
        # When the file is loaded and displayed
        if action == "upload":
            # Get filename and content
            file_name = uploaded_file.name
            file_key = file_name

            # Read file from S3
            try:
                s3_client = boto3.client('s3',
                                         aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                         aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
                response = s3_client.get_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=file_key)
                file_content = response['Body'].read().decode('utf-8')
            except Exception as e:
                upload_message = "An error occurred while reading the file: {}".format(str(e))
    
    # Import data into Django template
    return render(request, 'index.html', {
        'upload_message': upload_message,
        'file_name': file_name,
        'file_content': file_content
    })

import boto3


def list_s3(bucket, prefix, ext=None):
    """Get listing of files on S3 with prefix and extension
    """
    s3 = boto3.resource('s3')
    s3_bucket = s3.Bucket(bucket)

    if ext:
        ext = '.' + ext.lstrip('.')
    else:
        ext = ''

    for item in s3_bucket.objects.filter(Prefix=prefix):
        key = item.key
        if not key.endswith(ext):
            continue

        yield key

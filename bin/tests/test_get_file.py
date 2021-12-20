import os
from moto import mock_s3
import boto3

from get_file import FetchS3Object

base = os.path.dirname(os.path.abspath(__file__))
test_file_path = base + "/resources/file.txt"


@mock_s3
def test_fetch_bucket_object():
    # given
    bucket_name = "test-bucket-name"
    dst_file_path = "bin/resources/file.txt"
    s3 = boto3.resource("s3")
    bucket = s3.Bucket(bucket_name)
    bucket.create()
    bucket.upload_file(test_file_path, dst_file_path)

    instance = FetchS3Object(bucket_name=bucket_name)

    # when
    ret = instance.fetch_objects()

    # then
    assert ret == [dst_file_path]

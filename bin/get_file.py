import boto3

class FetchS3Object:
    def __init__(self, bucket_name: str) -> None:
        self.s3_client = boto3.client("s3")
        bucket = self.s3_client.Bucket(bucket_name)
        self.bucket_name = bucket.name

    def fetch_objects(self, prefix: str = None):
        next_token = ""
        while True:
            if next_token == "":
                response = self.s3_client.list_objects_v2(Bucket=self.bucket_name, Prefix=prefix)
            else:
                response = self.s3_client.list_objects_v2(Bucket=self.bucket_name, Prefix=prefix, ContinuationToken=next_token)
            for content in response["Contents"]:
                key = content["Key"]
                prt = key.split("/")
                print(prt)
            if "NextContinuationToken" in response:
                next_token = response["NextContinuationToken"]
            else:
                break

if __name__ == "__main__":
    fetch_s3_objects = FetchS3Object("kame-practice-cicd")
    fetch_s3_objects.fetch_objects()
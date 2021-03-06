import boto3


class FetchS3Object:
    def __init__(self, bucket_name: str) -> None:
        self.s3_client = boto3.client("s3")
        bucket = boto3.resource("s3").Bucket(bucket_name)
        self.bucket_name = bucket.name

    def fetch_objects(self):
        ret_list = []
        next_token = ""
        while True:
            if next_token == "":
                response = self.s3_client.list_objects_v2(Bucket=self.bucket_name)
            else:
                response = self.s3_client.list_objects_v2(
                    Bucket=self.bucket_name, ContinuationToken=next_token
                )
            for content in response["Contents"]:
                key = content["Key"]
                ret_list.append(key)
            if "NextContinuationToken" in response:
                next_token = response["NextContinuationToken"]
            else:
                break

        return ret_list


if __name__ == "__main__":
    fetch_s3_objects = FetchS3Object("kame-practice-cicd")
    ret_list = fetch_s3_objects.fetch_objects()
    for file in ret_list:
        print(file)

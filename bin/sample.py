import boto3

ec2_client = boto3.Session(profile_name="kameda").client("ec2")
ec2_resource = boto3.Session(profile_name="kameda").resource("ec2")

instance = ec2_resource.Instance(id="i-0c6afcefddfbaa2d8")
name_tag = [x["Value"] for x in instance.tags if x["Key"] == "Name"]
name = name_tag[0] if len(name_tag) else ""

print(name)

tags = ec2_client.describe_instances(InstanceIds=["i-0c6afcefddfbaa2d8"])

for tag in tags["Reservation"][0]["Instances"][0]["Tags"]:
    if tag["Key"] == "Name":
        tag = tag["Value"]

print(tag)

import boto3
import logging
import json
from typing import Optional
from datetime import datetime

cp_client = boto3.client("codepipeline")
ec2_client = boto3.resource("ec2")


def put_job_success(job_id: str) -> None:
    """CodePipelineのジョブへ成功を返す.

    Args:
        job_id (str): CodePipeline Job ID
    Returns:
        None
    """
    cp_client.put_job_success_result(jobId=job_id)
    return None


def put_job_failure(job_id: str, err: Exception) -> None:
    """CodePipelineのジョブへ失敗を返す.

    Args:
        job_id (str): CodePipeline Job ID
        err (Exception): Error Details

    Returns:
        None
    """
    message = f"Function exception: {err}"
    cp_client.put_job_failure_result(
        jobId=job_id, failureDetails={"type": "JobFailed", "message": message}
    )
    return None


def create_ami(prefix: str, instance_id: str) -> None:
    """EC2インスタンスからAMIを作成する.

    Args:
        prefix (str): Prefix of AMI
        instance_id (str): EC2 Instance ID
    """
    image_name = "_".join([prefix, datetime.now().strftime("%Y%m%d-%H%M%S")])

    ec2_client.create_image(
        InstanceId=instance_id,
        Name=image_name,
        Description="Created automatically by Lambda for Backup",
        NoReboot=True,
    )
    return None


def generate_tag(instance_id: str) -> Optional[str]:
    """AMIに付与するタグを生成する.

    Args:
        instance_id (str): EC2 Instance ID

    Returns:
        tag (str): AMI tag of EC2 Instance
    """
    tag = None
    tags = ec2_client.describe_instances(InstanceIds=[instance_id])
    for tag in tags["Reservations"][0]["Instances"][0]["Tags"]:
        if tag["Key"] == "Name":
            tag = tag["Value"]

    return tag


def delete_ami(image_id: str) -> None:
    """指定されたAMIを削除する.

    Args:
        image_id (str): AMI ID
    """
    logging.INFO(f"[DELETE] ImageId: {image_id}")
    ec2_client.Image(image_id).deregister()
    logging.INFO("Image Deleted.")
    return None


def lambda_handler(event, context):
    try:
        job_id = event["CodePipeline.job"]["id"]
        job_data = event["CodePipeline.job"]["data"]

        user_parameters = json.loads(
            job_data["actionConfiguration"]["configuration"]["UserParameters"]
        )

        pipeline_name = user_parameters["PipelineName"]
        usage = user_parameters["Usage"]

        logging.INFO(f"[START] PipelineName: {pipeline_name}")
        if usage == "create":
            instance_id = user_parameters["InstanceId"]
            logging.INFO(f"[CREATE] InstanceId: {instance_id}")
            prefix = generate_tag(instance_id)
            if prefix is None:
                raise Exception("Cannot generate prefix.")
            create_ami(prefix, instance_id)

        elif usage == "delete":
            image_id = user_parameters["ImageId"]
            logging.INFO(f"[DELETE] ImageId: {image_id}")
            delete_ami(image_id)

        else:
            raise Exception(f"Invalid Usage: {usage}")

        logging.INFO(f"[FINISH] PipelineName: {pipeline_name}")

        put_job_success(job_id)

    except Exception as e:
        put_job_failure(job_id, e)

    return "Complete."

import boto3
import logging
import json
import traceback

logger = logging.getLogger()
logger.setLevel(logging.INFO)

codepipeline_client = boto3.client("codepipeline")
imagebuilder_client = boto3.client("imagebuilder")


# 正常終了
def put_job_success(job_id):
    logger.info("Putting jub success")
    codepipeline_client.put_job_success_result(jobId=job_id)


# 処理継続/CodePipelineに継続トークン返却
def continue_job_later(job_id, image_builder_version_arn):
    logger.info("Putting job continuation")
    continuation_token = json.dumps({"ImageBuildVersionArn": image_builder_version_arn})
    codepipeline_client.put_job_success_result(
        jobId=job_id, continuation_token=continuation_token
    )


# 異常終了
def put_job_failure(job_id, err):
    logger.error("Putting job failed")
    message = str(err)
    codepipeline_client.put_job_failure_result(
        jobId=job_id, failureDetails={"type": "JobFailed", "message": message}
    )


def lambda_handler(event, context):
    try:
        job_id = event["CodePipeline.job"]["id"]
        job_data = event["CodePipeline.job"]["data"]

        # CodePipelineユーザパラメータ取得
        user_parameters = json.loads(
            job_data["actionConfiguration"]["configuration"]["UserParameters"]
        )
        image_pipeline_arn = user_parameters["imageBuildVersionArn"]

        logger.info(f"ImagePipelineArn is {image_pipeline_arn}")
        logger.info(f"CodePipeline Event is {event['CodePipeline.job']}")

        # 継続トークン有無確認
        if "continuationToken" in job_data:
            continuation_token = json.loads(job_data["continuationToken"])
            image_build_version_arn = continuation_token["ImageBuildVersionArn"]

            logger.info(image_build_version_arn)

            # ビルドの状態取得
            response = imagebuilder_client.get_image(
                imageBuildVersionArn=image_build_version_arn
            )
            build_status = response["image"]["state"]["status"]
            logger.info(build_status)

            if build_status == "AVAILABLE":
                put_job_success(job_id)
            elif build_status == "FAILED":
                errmsg = "Build Error"
                put_job_failure(job_id, errmsg)
            else:
                continue_job_later(job_id, image_build_version_arn)
        else:
            # ビルド実行
            response = imagebuilder_client.start_image_pipeline_execution(
                imagePipelineArn=image_pipeline_arn
            )
            image_build_version_arn = response["imageBuildVersionArn"]
            logger.info(f"imageBuildVersionArn is {image_build_version_arn}")
            continue_job_later(job_id, image_build_version_arn)

    except Exception as err:
        logger.error(f"Function exception: {err}")
        traceback.print_exc()
        put_job_failure(job_id, f"Function exception: {err}")

    logger.info("Function complete")
    return "Complete"

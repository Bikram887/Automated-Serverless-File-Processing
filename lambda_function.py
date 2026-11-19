
import boto3
import os
import urllib.parse

s3 = boto3.client("s3")
sns = boto3.client("sns")

OUTPUT_BUCKET = "vicky-file-processing-output-2026"
SNS_TOPIC_ARN = os.environ["SNS_TOPIC_ARN"]


def lambda_handler(event, context):
    try:
        for record in event["Records"]:
            input_bucket = record["s3"]["bucket"]["name"]
            file_key = urllib.parse.unquote_plus(
                record["s3"]["object"]["key"]
            )

            file_name = os.path.basename(file_key)
            file_extension = file_name.lower().split(".")[-1]

            response = s3.get_object(
                Bucket=input_bucket,
                Key=file_key
            )

            file_content = response["Body"].read()

            if file_extension == "txt":
                original_text = file_content.decode("utf-8")

                processed_content = (
                    "Processed successfully\n\n" + original_text
                ).encode("utf-8")

                s3.put_object(
                    Bucket=OUTPUT_BUCKET,
                    Key=f"processed-{file_name}",
                    Body=processed_content,
                    ContentType="text/plain"
                )

            elif file_extension in ["jpg", "jpeg", "png"]:
                content_type = (
                    "image/png"
                    if file_extension == "png"
                    else "image/jpeg"
                )

                s3.put_object(
                    Bucket=OUTPUT_BUCKET,
                    Key=f"processed-{file_name}",
                    Body=file_content,
                    ContentType=content_type
                )

            else:
                print(f"Unsupported file type: {file_name}")
                continue

            print(f"Successfully processed: {file_name}")

            sns.publish(
                TopicArn=SNS_TOPIC_ARN,
                Subject="File Processing Successful",
                Message=f"File {file_name} was processed successfully."
            )

        return {
            "statusCode": 200,
            "body": "File processing completed successfully"
        }

    except Exception as e:
        print(f"Processing failed: {str(e)}")

        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject="File Processing Failed",
            Message=f"File processing failed. Error: {str(e)}"
        )

        raise

# Automated Serverless Multi-File Processing System

## Project Overview
An event-driven serverless file-processing system built using AWS services. It automatically processes uploaded files and stores the output in a separate S3 bucket.

## AWS Services Used
- **Amazon S3:** Stores input and processed files.
- **AWS Lambda:** Processes files using Python.
- **Amazon SNS:** Sends success and failure email notifications.
- **AWS IAM:** Manages permissions for Lambda.
- **Amazon CloudWatch:** Stores Lambda execution logs.

## Architecture

```text
User Upload
    |
    v
S3 Input Bucket
    |
    v
S3 Event Notification
    |
    v
AWS Lambda (Python)
    |
    +------> TXT Processing
    |
    +------> JPG/JPEG/PNG Processing
    |
    v
S3 Output Bucket
    |
    v
Amazon SNS Email Notification
```

## S3 Buckets
- Input: `vicky-file-processing-input-2026`
- Output: `vicky-file-processing-output-2026`

## Lambda Function
`AutomatedFileProcessor`

### Processing Logic
- TXT files: Adds a processing-success message at the beginning.
- JPG/JPEG/PNG files: Copies the image without modifying its contents.
- Unsupported files: Skips processing.

Processed files are saved with the `processed-` prefix.

## Notifications
Amazon SNS sends email notifications for successful processing and attempts to send failure notifications when an exception occurs.

## Testing
- TXT file processing: Verified.
- JPG image processing: Verified.
- Success email notification: Verified.
- Failure email notification: Verified using a forced exception.
- PNG support: Included in code; separate testing not confirmed.

## Project Documentation
See [`docs/Project_Documentation.pdf`](docs/Project_Documentation.pdf) for detailed documentation and interview preparation.

## Important
AWS credentials are not included in this repository. Lambda uses its IAM execution role and the `SNS_TOPIC_ARN` environment variable.

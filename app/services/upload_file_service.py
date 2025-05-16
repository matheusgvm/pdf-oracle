import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class UploadFileService:

    def upload_file_to_s3(self, file_id: str, content: bytes) -> str:
        """
        Uploads a file content to S3 under the configured bucket and prefix.

        Args:
            file_id (str): Unique identifier to name the file in S3.
            content (bytes): File content in bytes.

        Returns:
            str: The S3 object key (path).

        Raises:
            ClientError: If upload fails.
            NoCredentialsError: If AWS credentials are missing.
        """
        s3_client = self._s3_client_setup()
        self._ensure_bucket_exists(s3_client)

        s3_file_path = f"{settings.S3_PREFIX}{file_id}.pdf"

        try:
            s3_client.put_object(
                Bucket=settings.S3_BUCKET_NAME,
                Key=s3_file_path,
                Body=content
            )
            logger.info(f"Uploaded file to s3://{settings.S3_BUCKET_NAME}/{s3_file_path}")
        except ClientError as e:
            logger.error(f"Failed to upload file to S3: {e}")
            raise

        return s3_file_path

    def _s3_client_setup(self):
        """
        Sets up and returns an S3 client using credentials from settings.

        Returns:
            boto3 S3 client
        """
        try:
            s3_client = boto3.client(
                "s3",
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_REGION,
            )
        except NoCredentialsError:
            logger.error("AWS credentials not found.")
            raise

        return s3_client

    def _ensure_bucket_exists(self, s3_client):
        """
        Checks if the bucket exists, creates it if it doesn't.

        Args:
            s3_client: boto3 S3 client instance

        Raises:
            ClientError: If bucket check or creation fails for reasons other than NotFound.
        """
        bucket_name = settings.S3_BUCKET_NAME
        try:
            s3_client.head_bucket(Bucket=bucket_name)
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == '404' or error_code == 'NoSuchBucket':
                logger.info(f"Bucket {bucket_name} not found, creating it...")
                try:
                    s3_client.create_bucket(
                        Bucket=bucket_name,
                        CreateBucketConfiguration={'LocationConstraint': s3_client.meta.region_name}
                    )
                    logger.info(f"Bucket {bucket_name} created successfully.")
                except ClientError as create_err:
                    logger.error(f"Failed to create bucket {bucket_name}: {create_err}")
                    raise
            else:
                logger.error(f"Failed to access bucket {bucket_name}: {e}")
                raise

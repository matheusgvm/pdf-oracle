import boto3
from app.core.config import settings
from botocore.exceptions import ClientError

class UploadFileService:

    def upload_file_to_s3(self, file_id: str, content: bytes):
        s3_client = self._s3_client_setup()

        self._ensure_bucket_exists(s3_client)
        s3_file_path = f"{settings.S3_PREFIX}{file_id}.pdf"

        s3_client.put_object(
            Bucket=settings.S3_BUCKET_NAME,
            Key=s3_file_path,
            Body=content
        )

    def _s3_client_setup(self):
        s3_client = boto3.client("s3",
                            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                            region_name=settings.AWS_REGION)

        return s3_client

    def _ensure_bucket_exists(self, s3_client):
        bucket_name = settings.S3_BUCKET_NAME
        try:
            s3_client.head_bucket(Bucket=bucket_name)
        except ClientError as e:
            error_code = int(e.response['Error']['Code'])
            if error_code == 404:
                print(f"Criando o bucket {bucket_name}")
                s3_client.create_bucket(
                    Bucket=bucket_name,
                    CreateBucketConfiguration={'LocationConstraint': s3_client.meta.region_name}
                )
            else:
                raise
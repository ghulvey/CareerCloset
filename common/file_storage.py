from storages.backends.s3boto3 import S3Boto3Storage
import uuid

class MediaStorage(S3Boto3Storage):
    location = ""
    default_acl = "public-read"
    file_overwrite = False
    custom_domain = False

    def get_available_name(self, name, max_length=None):
        ext = name.split('.')[-1]
        name = f"{uuid.uuid4()}.{ext}"
        return super().get_available_name(name, max_length=max_length)

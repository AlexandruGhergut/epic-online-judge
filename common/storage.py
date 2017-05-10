from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible
from azure.storage.blob import BlockBlobService, ContentSettings
from django.conf import settings


@deconstructible
class AzureStorage(Storage):

    def __init__(self, option=None):
        self.block_blob_service = \
            BlockBlobService(account_name=settings.AZURE_STORAGE_ACCOUNT_NAME,
                             account_key=settings.AZURE_STORAGE_ACCOUNT_KEY)
        self.block_blob_service.create_container(
            settings.AZURE_STORAGE_DEFAULT_CONTAINER
        )

    def _save(self, name, content):
        content.open()
        content_stream = content.read()
        self.block_blob_service.create_blob_from_bytes(
            'media',
            name,
            content_stream,
            content_settings=(
                ContentSettings(content_type=content.file.content_type)
            )
        )
        return name

    def exists(self, name):
        generator = self.block_blob_service.list_blobs('media')
        for blob in generator:
            if name == blob.name:
                return True
        return False

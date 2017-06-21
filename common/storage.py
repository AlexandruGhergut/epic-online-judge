import tempfile
from django.core.files.storage import Storage
from django.core.files import File
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

    def _open(self, name, mode='rb'):
        extension_index = name.rfind('.')
        extension = ''
        if extension_index != -1:
            extension = name[extension_index:]
        tmp_file = tempfile.NamedTemporaryFile(suffix=extension, delete=False)
        self.block_blob_service.get_blob_to_stream(
            container_name=settings.AZURE_STORAGE_DEFAULT_CONTAINER,
            blob_name=name,
            stream=tmp_file,
            max_connections=2
        )
        tmp_file.seek(0)

        return File(tmp_file)

    def exists(self, name):
        generator = self.block_blob_service.list_blobs('media')
        for blob in generator:
            if name == blob.name:
                return True
        return False

    def url(self, name):
        return self.name

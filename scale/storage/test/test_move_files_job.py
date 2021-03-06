from __future__ import unicode_literals

import os

import django
from django.test import TestCase
from mock import call, patch

from storage.brokers.broker import FileDownload, FileMove, FileUpload
from storage.models import ScaleFileManager, Workspace
from storage.move_files_job import move_files
from storage.test import utils as storage_test_utils


class TestMoveFiles(TestCase):

    def setUp(self):
        django.setup()
        
        self.old_workspace = storage_test_utils.create_workspace()
        self.new_workspace = storage_test_utils.create_workspace()

    @patch('storage.models.Workspace.get_file_system_paths', return_value=None)
    @patch('storage.models.ScaleFileManager.download_files')
    @patch('storage.models.ScaleFileManager.upload_files')
    @patch('storage.models.Workspace.delete_files')
    @patch('storage.move_files_job.CommandMessageManager')
    def test_move_file_new_workspace(self, mock_message, mock_delete, mock_upload, mock_download, mock_paths):
        """Tests moving a file"""

        volume_path = os.path.join('the', 'volume', 'path')
        file_path_1 = os.path.join('my_dir', 'my_file.txt')
        file_path_2 = os.path.join('my_dir', 'my_file.json')
        full_path_file_1 = os.path.join(volume_path, file_path_1)
        full_path_file_2 = os.path.join(volume_path, file_path_2)

        file_1 = storage_test_utils.create_file(file_path=file_path_1, workspace=self.old_workspace)
        file_2 = storage_test_utils.create_file(file_path=file_path_2, workspace=self.old_workspace)
        file_ids = [file_1.id, file_2.id]

        # Call function
        move_files(file_ids, new_workspace=self.new_workspace, new_file_path=None)

        # Check results
        mock_download.assert_called()
        mock_upload.assert_called()
        mock_delete.assert_called()

    @patch('storage.models.Workspace.get_file_system_paths', return_value=['/tmp/one','/tmp/two'])
    @patch('storage.models.ScaleFileManager.download_files')
    @patch('storage.models.ScaleFileManager.upload_files')
    @patch('storage.models.Workspace.delete_files')
    @patch('storage.move_files_job.CommandMessageManager')
    def test_move_file_new_workspace_without_download(self, mock_message, mock_delete, mock_upload, mock_download, mock_paths):
        """Tests moving a file"""

        volume_path = os.path.join('the', 'volume', 'path')
        file_path_1 = os.path.join('my_dir', 'my_file.txt')
        file_path_2 = os.path.join('my_dir', 'my_file.json')
        full_path_file_1 = os.path.join(volume_path, file_path_1)
        full_path_file_2 = os.path.join(volume_path, file_path_2)

        file_1 = storage_test_utils.create_file(file_path=file_path_1, workspace=self.old_workspace)
        file_2 = storage_test_utils.create_file(file_path=file_path_2, workspace=self.old_workspace)
        file_ids = [file_1.id, file_2.id]

        # Call function
        move_files(file_ids, new_workspace=self.new_workspace, new_file_path=None)

        # Check results
        mock_download.assert_not_called()
        mock_upload.assert_called()
        mock_delete.assert_called()

    @patch('storage.models.ScaleFileManager.move_files')
    @patch('storage.move_files_job.CommandMessageManager')
    def test_move_file_new_path(self, mock_message, mock_move):
        """Tests moving a file"""

        volume_path = os.path.join('the', 'volume', 'path')
        file_path_1 = os.path.join('my_dir', 'my_file.txt')
        file_path_2 = os.path.join('my_dir', 'my_file.json')
        full_path_file_1 = os.path.join(volume_path, file_path_1)
        full_path_file_2 = os.path.join(volume_path, file_path_2)

        file_1 = storage_test_utils.create_file(file_path=file_path_1, workspace=self.old_workspace)
        file_2 = storage_test_utils.create_file(file_path=file_path_2, workspace=self.old_workspace)
        file_ids = [file_1.id, file_2.id]

        # Call function
        move_files(file_ids, new_workspace=None, new_file_path='/test/path')

        # Check results
        mock_move.assert_called()
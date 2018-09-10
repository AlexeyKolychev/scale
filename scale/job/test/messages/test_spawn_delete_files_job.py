from __future__ import unicode_literals

import django
from django.test import TransactionTestCase
from django.utils import timezone

from job.messages.spawn_delete_files_job import create_spawn_delete_files_job, SpawnDeleteFilesJob
from job.models import Job, JobExecution, JobType
from job.test import utils as job_test_utils
from storage.models import ScaleFile
from storage.test import utils as storage_test_utils
from trigger.test import utils as trigger_test_utils

from django.db.models.query import QuerySet
from pprint import PrettyPrinter

def dprint(object, stream=None, indent=1, width=80, depth=None):
    """
    A small addition to pprint that converts any Django model objects to dictionaries so they print prettier.

    h3. Example usage

        >>> from toolbox.dprint import dprint
        >>> from app.models import Dummy
        >>> dprint(Dummy.objects.all().latest())
         {'first_name': u'Ben',
          'last_name': u'Welsh',
          'city': u'Los Angeles',
          'slug': u'ben-welsh',
    """
    # Catch any singleton Django model object that might get passed in
    if getattr(object, '__metaclass__', None):
        if object.__metaclass__.__name__ == 'ModelBase':
            # Convert it to a dictionary
            object = object.__dict__
    
    # Catch any Django QuerySets that might get passed in
    elif isinstance(object, QuerySet):
        # Convert it to a list of dictionaries
        object = [i.__dict__ for i in object]
        
    # Pass everything through pprint in the typical way
    printer = PrettyPrinter(stream=stream, indent=indent, width=width, depth=depth)
    printer.pprint(object)


class TestSpawnDeleteFilesJob(TransactionTestCase):

    fixtures = ['delete_files_job_type.json']

    def setUp(self):
        django.setup()

        self.count = 1
        self.job_type = job_test_utils.create_job_type()
        self.job = job_test_utils.create_job(job_type=self.job_type)
        self.job_exe = job_test_utils.create_job_exe(status='COMPLETED', job=self.job)
        self.wp1 = storage_test_utils.create_workspace()
        self.wp2 = storage_test_utils.create_workspace()
        self.prod1 = storage_test_utils.create_file(file_type='PRODUCT', workspace=self.wp1, job_exe=self.job_exe)
        self.prod2 = storage_test_utils.create_file(file_type='PRODUCT', workspace=self.wp1, job_exe=self.job_exe)
        self.prod3 = storage_test_utils.create_file(file_type='PRODUCT', workspace=self.wp2, job_exe=self.job_exe)
        self.event = trigger_test_utils.create_trigger_event()

    def test_json(self):
        """Tests coverting a SpawnDeleteFilesJob message to and from JSON"""

        # Make the message
        message = create_spawn_delete_files_job(job_id=self.job.pk, trigger_id=self.event.id, purge=True)

        # Convert message to JSON and back, and then execute
        message_json_dict = message.to_json()
        new_message = SpawnDeleteFilesJob.from_json(message_json_dict)
        result = new_message.execute()
        self.assertTrue(result)

        # Check for create_jobs messages
        self.assertEqual(len(new_message.new_messages), self.count)
        for msg in new_message.new_messages:
            self.assertEqual(msg.type, 'create_jobs')

    def test_execute(self):
        """Tests calling _generate_jobs_message successfully"""

        job_type_id = JobType.objects.values_list('id', flat=True).get(name='scale-delete-files')

        # Make the message
        message = create_spawn_delete_files_job(job_id=self.job.pk, trigger_id=self.event.id, purge=True)

        # Capture message that creates job
        result = message.execute()
        self.assertTrue(result)

        for msg in message.new_messages:
            msg.execute()

        # Check that job is created
        self.assertEqual(Job.objects.filter(job_type_id=job_type_id, event_id=self.event.id).count(), self.count)

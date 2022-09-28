from multiprocessing.connection import Client
from time import time
from django.test import TestCase
from unity.models import Subscriber
from django.urls import reverse
from datetime import datetime, timezone, timedelta
from faker import Faker
# from tasks import sending_mail
# Create your tests here.
fake = Faker()
class SubscriberTestCase(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        cls.subscriber = Subscriber.objects.create(email=fake.email())

        
    def test_subscriber(self):
        email = fake.email()
        response = self.client.post('/api/v1/subscribe', {'email': email}, content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_unsubscribe(self):
        response = self.client.post('/api/v1/unsubscribe', {'email': self.subscriber.email}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
    
    def test_email_validation(self):
        email = 'abc'
        response = self.client.post('/api/v1/subscribe', {'email': email}, content_type='application/json')
        self.assertEqual(response.status_code, 422)

    def test_email_validation(self):
        email = 'abc'
        response = self.client.post('/api/v1/subscribe', {'email': ''}, content_type='application/json')
        self.assertEqual(response.status_code, 422)

    def test_email_uniqueness(self):
        response = self.client.post('/api/v1/subscribe', {'email': ''}, content_type='application/json')
        self.assertEqual(response.status_code, 422)


    def test_counter(self):
        
        for i in range(5):
            Subscriber.objects.create(email=fake.email(), timestamp=datetime(year=2021, month=2, day=1, tzinfo=timezone.utc) )
        for i in range(20):
            Subscriber.objects.create(email=fake.email(), status='UNSUBSCRIBED')

        for i in range(10):
            Subscriber.objects.create(email=fake.email(), timestamp = datetime.now(timezone.utc))
        response = self.client.get(reverse('unity.index'))
        # check assert pagination
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['total_data'], 36) # + 1 from setUpTestData
        self.assertEqual(response.context['total_unsubscribers'], 20)
        self.assertEqual(response.context['total_subscriber_this_month'], 31)
        self.assertEqual(response.status_code, 200)


    # def test_mail_send(self):
    #     # send mail to fake email
    #     # check mail sent
    #     sending_mail()

# bookings/tests.py

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from .models import FitnessClass, Booking
from django.utils import timezone
from datetime import timedelta

class BookingAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.future_time = timezone.now() + timedelta(days=1)
        self.class1 = FitnessClass.objects.create(
            name='Yoga',
            instructor='Alice',
            scheduled_at=self.future_time,
            available_slots=2
        )

        self.valid_payload = {
            'class_id': self.class1.id,
            'client_name': 'John Doe',
            'client_email': 'john@example.com'
        }

    def test_get_classes(self):
        response = self.client.get('/backend/api/v1/classes')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_successful_booking(self):
        response = self.client.post('/backend/api/v1/book', data=self.valid_payload, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(FitnessClass.objects.get(id=self.class1.id).available_slots, 1)
        self.assertEqual(Booking.objects.count(), 1)

    def test_booking_no_slots_left(self):
        # Exhaust slots
        self.client.post('/backend/api/v1/book', data=self.valid_payload, format='json')
        self.client.post('/backend/api/v1/book', data=self.valid_payload, format='json')

        response = self.client.post('/backend/api/v1/book', data=self.valid_payload, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('No slots available', response.data['error'])

    def test_booking_missing_fields(self):
        invalid_payload = {'client_name': 'John'}
        response = self.client.post('/backend/api/v1/book', data=invalid_payload, format='json')
        self.assertEqual(response.status_code, 400)

    def test_get_bookings_by_email(self):
        self.client.post('/backend/api/v1/book', data=self.valid_payload, format='json')

        response = self.client.get('/backend/api/v1/bookings?email=john@example.com')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_get_bookings_missing_email(self):
        response = self.client.get('/backend/api/v1/bookings')
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.data)

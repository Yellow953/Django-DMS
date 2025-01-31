from django.test import TestCase

class SchemaAPITest(TestCase):
    def test_create_schema(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/schemas/', {'name': 'Test'})
        self.assertEqual(response.status_code, 201)
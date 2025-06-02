# apps/projects/tests/test_full_api.py

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class FullAPITest(APITestCase):
    def setUp(self):
        # создаем пользователя
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123'
        )
        self.client.force_authenticate(user=self.user)

    def test_full_flow(self):
        # 1. создать проект
        project_payload = {
            "name": "Test Project",
            "description": "Test project description"
        }
        response = self.client.post(reverse('project-list'), project_payload)
        print(f"POST Response: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        project_id = response.data.get('id')
        print(f"project_id: {project_id}")
        self.assertIsNotNone(project_id)

        # 💡💡💡 ВАЖНО:
        # Форсируем выборку, чтобы connection закоммитился
        from apps.projects.models import Project
        _ = Project.objects.get(pk=project_id)

        # 2. получить список проектов
        response = self.client.get(reverse('project-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

        # 3. получить детали проекта
        response = self.client.get(reverse('project-detail', kwargs={'pk': project_id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], project_payload['name'])

        # 4. обновить проект
        updated_project_payload = {
            "name": "Updated Project",
            "description": "Updated description"
        }
        response = self.client.put(reverse('project-detail', kwargs={'pk': project_id}), updated_project_payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], updated_project_payload['name'])

        # 5. создать КТС
        kts_payload = {
            "name": "Test KTS"
        }
        print(reverse('project-kts-list', kwargs={'project_pk': project_id}))
        response = self.client.post(reverse('project-kts-list', kwargs={'project_pk': project_id}), kts_payload)
        print(f"KTS POST Response: {response.status_code}, {response.content}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        kts_id = response.data['id']

        # 6. получить список КТС для проекта
        response = self.client.get(reverse('project-kts-list', kwargs={'project_pk': project_id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

        # 7. получить детали КТС
        response = self.client.get(reverse('kts-detail', kwargs={'pk': kts_id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], kts_payload['name'])

        # 8. обновить КТС
        updated_kts_payload = {
            "name": "Updated KTS"
        }
        response = self.client.put(reverse('kts-detail', kwargs={'pk': kts_id}), updated_kts_payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], updated_kts_payload['name'])

        # 9. создать комплектную единицу
        unit_payload = {
            "name": "Test Unit"
        }
        response = self.client.post(reverse('kts-units-list', kwargs={'kts_pk': kts_id}), unit_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        unit_id = response.data['id']

        # 10. получить список комплектных единиц
        response = self.client.get(reverse('kts-units-list', kwargs={'kts_pk': kts_id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

        # 11. получить детали комплектной единицы
        response = self.client.get(reverse('unit-detail', kwargs={'pk': unit_id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], unit_payload['name'])

        # 12. обновить комплектную единицу
        updated_unit_payload = {
            "name": "Updated Unit"
        }
        response = self.client.put(reverse('unit-detail', kwargs={'pk': unit_id}), updated_unit_payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], updated_unit_payload['name'])

        # 13. создать изделие
        item_payload = {
            "name": "Test Item",
            "supplier": "Test Supplier",
            "catalog_code": "TEST123",
            "quantity": 10,
            "price": 500.00,
            "manufacturer": "Test Manufacturer",
            "currency": "USD",
            "delivery_type": "DDP"
        }
        response = self.client.post(reverse('unit-items-list', kwargs={'unit_pk': unit_id}), item_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        item_id = response.data['id']

        # 14. получить список изделий
        response = self.client.get(reverse('unit-items-list', kwargs={'unit_pk': unit_id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

        # 15. получить детали изделия
        response = self.client.get(reverse('item-detail', kwargs={'pk': item_id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], item_payload['name'])

        # 16. обновить изделие
        updated_item_payload = {
            "name": "Updated Item",
            "supplier": "Updated Supplier",
            "catalog_code": "UPDATED123",
            "quantity": 20,
            "price": 1000.00,
            "manufacturer": "Updated Manufacturer",
            "currency": "EUR",
            "delivery_type": "FOB"
        }
        response = self.client.put(reverse('item-detail', kwargs={'pk': item_id}), updated_item_payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], updated_item_payload['name'])

        # 17. проверить итоговую спецификацию
        response = self.client.get(reverse('project-view-specification', kwargs={'pk': project_id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['project'], updated_project_payload['name'])
        self.assertGreaterEqual(len(response.data['kts']), 1)

        # 18. удалить изделие
        response = self.client.delete(reverse('item-detail', kwargs={'pk': item_id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # 19. удалить комплектную единицу
        response = self.client.delete(reverse('unit-detail', kwargs={'pk': unit_id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # 20. удалить КТС
        response = self.client.delete(reverse('kts-detail', kwargs={'pk': kts_id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # 21. удалить проект
        response = self.client.delete(reverse('project-detail', kwargs={'pk': project_id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

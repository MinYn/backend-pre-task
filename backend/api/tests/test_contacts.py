from django.urls import include, path, reverse
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase

from api.contacts.serializers.contacts import ContactDetailSerializer, LabelSerializer
from apps.models.contacts import Contact, Label

class ContactsTests(APITestCase, URLPatternsTestCase):
    urlpatterns = [
        path('api/', include('api.urls')),
    ]
    @classmethod
    def setUpTestData(cls):
        cls.contact_data = {
            "profile_picture": "https://avatars.githubusercontent.com/u/7910274?v=4",
            "name": "윤석민",
            "email": "ysmysm3@naver.com",
            "tel": "010-3039-4040",
            "company": "개인",
            "grade": "프리랜서",
            "note": "백엔드 개발자 입니다.",
            "address": "경기 화성시 동탄산척로2나길 10-12 202호",
            "birthday": "1994-12-02",
            "website": "https://github.com/MinYn",
            "labels": [
                {"name": "기본"},
                {"name": "가족"},
                {"name": "친구"},
            ]
        }
        serializer = ContactDetailSerializer(data=cls.contact_data)
        serializer.is_valid()
        cls.contact: Contact = serializer.save()

        cls.label_data = {
            "name": "레이블 테스트",
        }
        serializer = LabelSerializer(data=cls.label_data)
        serializer.is_valid()
        cls.label: Label = serializer.save()

    # 연락처 테스트
    def test_list_contacts(self):
        url = reverse('api_v1:contacts-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_contacts(self):
        url = reverse('api_v1:contacts-list')
        response = self.client.post(url, data=self.contact_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_contacts(self):
        url = reverse('api_v1:contacts-detail', kwargs={'pk': self.contact.pk})
        response = self.client.put(url, data=self.contact_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_contacts(self):
        url = reverse('api_v1:contacts-detail', self.contact.pk)
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # 연락처 레이블 추가, 삭제 테스트
    def test_add_contacts_label(self):
        url = reverse('api_v1:contacts-label', kwargs={'pk': self.contact.pk, 'label_id': self.label.pk})
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_contacts_label(self):
        url = reverse('api_v1:contacts-label', kwargs={'pk': self.contact.pk, 'label_id': self.label.pk})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # 레이블 테스트
    def test_list_label(self):
        url = reverse('api_v1:label-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_label(self):
        url = reverse('api_v1:label-list')
        response = self.client.post(url, data=self.label_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_label(self):
        url = reverse('api_v1:label-detail', kwargs={'pk': self.label.pk})
        response = self.client.put(url, data=self.label_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_contacts(self):
        url = reverse('api_v1:label-detail', kwargs={'pk': self.label.pk})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

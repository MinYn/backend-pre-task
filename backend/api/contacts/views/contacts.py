from rest_framework import viewsets, status
from rest_framework.filters import OrderingFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import CursorPagination

from drf_yasg.utils import no_body, swagger_auto_schema

from django_mysql.models import GroupConcat

from api.contacts.serializers.contacts import ContactDetailSerializer, ContactSerializer, LabelSerializer

from apps.models.contacts import Contact, Label


class StandardCursorPagination(CursorPagination):
    page_size = 10
    ordering = 'id'

class ContactsViewSet(viewsets.ModelViewSet):
    """
    Contacts
    ---
    연락처 조회, 생성, 수정, 삭제
    """
    queryset = Contact.objects.annotate(labels_names=GroupConcat('labels__name')).all()
    http_method_names = ['get', 'post', 'put', 'delete']
    serializer_class = ContactDetailSerializer
    pagination_class = StandardCursorPagination
    filter_backends = [OrderingFilter]
    ordering_fields = ['name', 'email', 'tel']
    ordering = ['id']

    def list(self, request, *args, **kwargs):
        self.serializer_class = ContactSerializer
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(method='post', request_body=no_body)
    @action(methods=['post', 'delete'], detail=True, url_path=r'label/(?P<label_id>[^/.]+)', url_name='label')
    def label(self, request, pk=None, label_id=None):
        contact = None
        if request.method == "POST":
            contact = self.add_label(pk, label_id)
        elif request.method == "DELETE":
            contact = self.delete_label(pk, label_id)
        if contact:
            return Response(status=status.HTTP_200_OK, data=self.serializer_class(contact).data)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def add_label(self, pk=None, label_id=None):
        contact = Contact.objects.get(pk=pk)
        contact.labels.add(Label.objects.get(pk=label_id))
        return contact

    def delete_label(self, pk=None, label_id=None):
        contact = Contact.objects.get(pk=pk)
        contact.labels.remove(Label.objects.get(pk=label_id))
        return contact


class LabelViewSet(viewsets.ModelViewSet):
    """
    Label CRUD
    ---
    레이블
    """
    queryset = Label.objects.all()
    http_method_names = ['get', 'post', 'put', 'delete']
    serializer_class = LabelSerializer

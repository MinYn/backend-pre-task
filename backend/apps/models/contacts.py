from django.db import models


class Contact(models.Model):
    """
        연락처
    """
    profile_picture = models.URLField(max_length=200, verbose_name="프로필 사진")
    name = models.CharField(max_length=50, verbose_name="이름")
    email = models.EmailField(max_length=100, verbose_name="이메일")
    tel = models.CharField(max_length=50, verbose_name="전화번호")
    company = models.CharField(max_length=50, verbose_name="회사", blank=True, null=True)
    grade = models.CharField(max_length=50, verbose_name="직책", blank=True, null=True)
    note = models.CharField(max_length=50, verbose_name="메모", blank=True, null=True)
    address = models.CharField(max_length=200, verbose_name="주소", blank=True, null=True)
    birthday = models.DateField(verbose_name="생일", blank=True, null=True)
    website = models.URLField(max_length=200, verbose_name="웹사이트", blank=True, null=True)
    labels = models.ManyToManyField('Label', through='ContactLabel', related_name='contacts')
    
    class Meta:
        db_table = "contacts"


class ContactLabel(models.Model):
    contact = models.ForeignKey('Contact', related_name='contact_labels', on_delete=models.CASCADE)
    label = models.ForeignKey('Label', related_name='contact_labels', on_delete=models.CASCADE)

    class Meta:
        db_table = "contacts_labels"
        constraints = [
            models.UniqueConstraint(fields=['contact', 'label'], name='unique_contact_label')
        ]


class Label(models.Model):
    """
        라벨
    """
    name = models.CharField(max_length=50, verbose_name="이름")
    
    class Meta:
        db_table = "label"

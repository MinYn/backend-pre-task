from rest_framework import serializers


from apps.models.contacts import Contact, ContactLabel, Label


class LabelSerializer(serializers.ModelSerializer):
    name = serializers.CharField(allow_blank=False, max_length=50)

    def create(self, validated_data):
        instance, created_result = Label.objects.get_or_create(**validated_data)
        return instance

    class Meta:
        model = Label
        fields = ['name']

class ContactSerializer(serializers.ModelSerializer):
    id = serializers.CharField()
    profile_picture = serializers.URLField()
    name = serializers.CharField()
    email = serializers.EmailField()
    tel = serializers.CharField()
    company = serializers.SerializerMethodField()
    labels = serializers.SerializerMethodField()

    def get_company(self, instance):
        return f'{instance.company}({instance.grade})'

    def get_labels(self, instance):
        return f'{instance.labels_names}' if instance.labels_names else ''

    class Meta:
        model = Contact
        fields = ['id', 'profile_picture', 'name', 'email', 'tel', 'company', 'labels']

class ContactDetailSerializer(serializers.ModelSerializer):
    profile_picture = serializers.URLField()
    name = serializers.CharField(allow_blank=False, max_length=50)
    email = serializers.EmailField()
    tel = serializers.CharField(allow_blank=False, max_length=50)
    company = serializers.CharField(max_length=50)
    grade = serializers.CharField(max_length=50)
    note = serializers.CharField(max_length=50)
    address = serializers.CharField(max_length=200)
    birthday = serializers.DateField()
    website = serializers.URLField()
    labels = LabelSerializer(many=True)

    def create(self, validated_data):
        labels_data = validated_data.pop("labels")
        instance: Contact = Contact.objects.create(**validated_data)
        for label in labels_data:
            label_data = dict(label)
            label, created_result = Label.objects.get_or_create(name=label_data['name'])
            ContactLabel.objects.get_or_create(contact=instance, label=label)
        return instance

    def update(self, instance, validated_data):
        labels_data = validated_data.pop('labels')
        for item in validated_data:
            if Contact._meta.get_field(item):
                setattr(instance, item, validated_data[item])
        ContactLabel.objects.filter(contact=instance).delete()
        for label in labels_data:
            label_data = dict(label)
            label, created_result = Label.objects.get_or_create(name=label_data['name'])
            ContactLabel.objects.get_or_create(contact=instance, label=label)
        instance.save()
        return instance

    class Meta:
        model = Contact
        fields = ['profile_picture', 'name', 'email', 'tel', 'company', 'grade', 'note', 'address', 'birthday', 'website', 'labels']

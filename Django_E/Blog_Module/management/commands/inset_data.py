from django.core.management.base import BaseCommand
from Account_Module.models import User, Profile
from Blog_Module.models import Post, Category
from faker import Faker
import random
from datetime import datetime

category_list = ["IT", "Design", "Fun"]


class Command(BaseCommand):
    help = "lorem Ipsum"

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.fake = Faker()

    def handle(self, *args, **options):
        phone_number = str(self.fake.ssn())
        phone = phone_number.replace("-", "")
        user_obj = User.objects.create_user(
            phone=phone, email=self.fake.email(), password="admin"
        )
        profile_obj = Profile.objects.get(user=user_obj)
        profile_obj.first_name = self.fake.first_name()
        profile_obj.last_name = self.fake.last_name()
        profile_obj.description = self.fake.paragraph(nb_sentences=5)
        profile_obj.save()

        for name in category_list:
            Category.objects.get_or_create(name=name)

        try:
            for _ in range(10):
                Post.objects.create(
                    author=profile_obj,
                    title=self.fake.paragraph(nb_sentences=1),
                    content=self.fake.paragraph(nb_sentences=10),
                    status=random.choice([True, False]),
                    category=Category.objects.get(
                        name=random.choice(category_list)
                    ),
                    published_date=datetime.now(),
                )
        except Post.MultipleObjectsReturned:
            print("can not create Post")

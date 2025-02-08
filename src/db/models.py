from tortoise import fields, models
import uuid
from datetime import datetime

class User(models.Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    username = fields.CharField(max_length=50, unique=True)
    is_verified = fields.BooleanField(default=False)
    password_hash = fields.CharField(max_length=255)
    created_at = fields.DatetimeField(default=datetime.now)
    updated_at = fields.DatetimeField(default=datetime.now)

    def __repr__(self):
        return f"<User {self.username}>"


class Routes(models.Model):
    id = fields.UUIDField(pk=True,default=uuid.uuid4)
    from_dan = fields.CharField(max_length=255)
    to_ga = fields.CharField(max_length=255)
    number = fields.IntField()
    description = fields.TextField()
    created_at = fields.DatetimeField(default=datetime.now)
    updated_at = fields.DatetimeField(default=datetime.now)

    def __repr__(self):
        return f"<Routes {self.id}>"
    

class Reviews(models.Model):
    id = fields.UUIDField(pk=True,default=uuid.uuid4)
    rating = fields.IntField()
    text = fields.TextField()
    created_at = fields.DatetimeField(default=datetime.now)

    def __repr__(self):
        return f"<Reviews {self.id}>"
    

class Adverts(models.Model):
    id = fields.UUIDField(pk=True, default=uuid.uuid4)
    title = fields.CharField(max_length=150)
    file = fields.CharField(max_length=255)
    description = fields.TextField()
    link = fields.CharField(max_length=150)
    date = fields.DatetimeField(default=datetime.now)

    def __repr__(self):
        return f"<Adverts {self.id}>"
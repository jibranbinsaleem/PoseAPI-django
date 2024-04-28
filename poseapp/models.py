from django.db import models
# from django.contrib.auth.models import AbstractUser
# from django.contrib.auth.models import User

# # Custom User Model
# class User(models.Model):
#     # Add any additional fields you need
#     username = models.CharField(max_length=100, unique=True)
#     email = models.EmailField()
#     password = models.CharField(max_length=100)


class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField()
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    firebase_id = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return f"{self.username}"



def get_default_scopes():
    return ["read"]
class APIKey(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    key = models.CharField(max_length=100, unique=True)
    secret = models.CharField(max_length=100, unique=True)
    #scopes field which is a list of permissions the APIkey has access to
    scopes = models.JSONField(default=get_default_scopes)
    expires = models.DateTimeField(default=None, null=True, blank=True)
    revoked = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"API Key for {self.user.username}"

class Subscription(models.Model):
    FREE = 'free'
    PREMIUM = 'premium'
    SUBSCRIPTION_TYPES = [
        (FREE, 'Free'),
        (PREMIUM, 'Premium'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=SUBSCRIPTION_TYPES, default=FREE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return f"{self.type} subscription for {self.user.username}"

class RateLimit(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscription = models.OneToOneField(Subscription, on_delete=models.CASCADE)
    api_calls_made = models.IntegerField(default=0)
    max_api_calls = models.IntegerField(default=10)  # 10 for free users, more for premium users
    reset_time = models.DateTimeField()  # time when the api_calls_made resets to 0

    def increment(self):
        self.api_calls_made += 1
        self.save()

    def can_make_api_call(self):
        return self.api_calls_made < self.max_api_calls
    def __str__(self):
        return f"Rate limit for {self.user.username}"
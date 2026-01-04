from django.db import models

class Conversation(models.Model):
    user_message = models.CharField(max_length=100)
    bot_response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_message[:30]

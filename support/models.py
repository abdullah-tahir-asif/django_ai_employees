from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from orders.models import Order

class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation between {self.user.id} and {self.user.username} / Order #{self.order.id}"

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    role=models.CharField(max_length=10, choices=[('user', 'User'), ('agent', 'Agent')])
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.role}: {self.content[:50]}..."


class AgentLog(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='agent_logs')
    event_type = models.CharField(max_length=50, choices=[('support', 'Support Agent'), ('tool_call', 'Tool Call'), ('tool result', 'Tool Result'), ('manager', 'Mannager Agent'),('manager result', 'Manager Result'),('risk', 'Risk Agent'),('Final', 'Final Reply')])
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.event_type}] - {self.message[:40]}"


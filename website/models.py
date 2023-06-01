from django.db import models
from django.contrib.auth.models import User

class Dialogue(models.Model):
	user = models.ForeignKey(User, related_name="code", on_delete=models.DO_NOTHING)
	question = models.TextField(max_length=5000)
	answer = models.TextField(max_length=5000)
	created_at = models.DateTimeField(auto_now_add=True)
	# completion_tokens = models.IntegerField(default=0)
	# prompt_tokens = models.IntegerField(default=0)
	total_tokens = models.IntegerField(default=0)
	openai_id = models.CharField(max_length=256, default="")


	def __str__(self):
		return self.question
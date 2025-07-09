from django.db import models

# Create your models here.

class Document(models.Model):
    file = models.FileField(upload_to='documents/')
    name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Chunk(models.Model):
    document = models.ForeignKey(Document, related_name='chunks', on_delete=models.CASCADE)
    text = models.TextField()
    embedding = models.BinaryField()  # Store as bytes; can be changed to ArrayField if using Postgres
    page_number = models.IntegerField(null=True, blank=True)
    order = models.IntegerField(default=0)  # Order of chunk in document

    def __str__(self):
        return f"Chunk {self.order} of {self.document.name}"

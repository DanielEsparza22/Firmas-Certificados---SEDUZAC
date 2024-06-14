from django.db import models

class FolioSequenceBD(models.Model):
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return f'{str(self.id)}'

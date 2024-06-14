from django.db import models

class FolioSequencePE(models.Model):
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return f'{str(self.id)}'
    
class FolioLetraPE(models.Model):
    letra = models.CharField(max_length=1, default='A')

    def __str__(self):
        return f'{self.letra}'

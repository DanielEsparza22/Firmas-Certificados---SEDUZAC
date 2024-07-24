from django.db import connection
from .models import FolioSequence


def reiniciar_secuencia_folio():
    with connection.cursor() as cursor:
        FolioSequence.objects.all().delete()

        cursor.execute("ALTER TABLE ConfiguracionApp_foliosequence AUTO_INCREMENT = 1;")
        

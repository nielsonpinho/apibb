from django.db import models
import datetime
# Create your models here.

class Pesquisa(models.Model):
    """Pesquisas realizadas pelos usuarios"""
    text = models.CharField(max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)
    usuario = models.CharField(max_length=100)

    def __str__(self):
        """Devolve uma representação em string do modelo"""
        return self.text + ' | ' + self.usuario + ' | ' + datetime.datetime.strftime(self.date_added, "%d/%m/%Y")
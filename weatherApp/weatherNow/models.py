from django.db import models

class Provincia( models.Model):
  """Creamos la tabla de provincias
  Args:
    models (repository): Lo usamos para crear la estructura de la tabla.
  """
  prov_code = models.CharField(max_length = 100,
                               unique = True,
                               blank = False)
  prov_name = models.CharField(max_length=100)
  autono_code = models.CharField(max_length=100)
  com_auton = models.CharField(max_length=100)
  capital_city = models.CharField(max_length=100)



class Municipios( models.Model):
  """Creamos la tabla de los municipios
  Args:
      models (repository): Lo usamos para crear la estructura de la tabla.
  """
  muni_code = models.CharField(max_length=100,
                               unique = True)
  muni_name = models.CharField(max_length=100)
  prov_code = models.ForeignKey( Provincia,
    related_name = "muni_prov_code",
    blank = False,
    null = False,
    on_delete = models.CASCADE
  )

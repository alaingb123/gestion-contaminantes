from django.utils import timezone

from django.utils.deprecation import MiddlewareMixin

from otras_fuentes.models import Municipio


from django.apps import apps

class InitialFilterMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Verifica que las aplicaciones estén listas
        if apps.ready:
            if request.path.startswith('/admin/Contaminantes/liquidos/'):
                if not request.GET.get('year__exact'):
                    year = timezone.now().year
                    request.GET._mutable = True
                    request.GET['year__exact'] = year
                    request.GET._mutable = False

                if not request.GET.get('municipio__exact'):
                    municipio_santa_clara = apps.get_model('tu_app', 'Municipio').objects.get(nombre='Santa Clara')
                    request.GET._mutable = True
                    request.GET['municipio__exact'] = municipio_santa_clara.id
                    request.GET._mutable  = False
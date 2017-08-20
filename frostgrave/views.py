from django.views.generic import ListView

from .models import Treasure

class TreasureListView(ListView):
    model = Treasure
    template_name = 'frostgrave/treasure-list.html'
    queryset = model.objects.all()

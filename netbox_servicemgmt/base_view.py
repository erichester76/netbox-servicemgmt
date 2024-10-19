from netbox.views import generic

class BaseObjectView(generic.ObjectView):
    template='default-detail.html'

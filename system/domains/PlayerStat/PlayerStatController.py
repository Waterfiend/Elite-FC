from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from system.helpers.FormValidationJS import FormValidationErrorsJS, ConfirmPasswordErrorJS
from ...models import PlayerStat
from django.urls import reverse_lazy

class HomeView(ListView):  # list all article posts on news page
    model = PlayerStat
    template_name = 'system/playerstat.html'
    
class PlayerDetailView(DetailView): 
    model = PlayerStat
    template_name = 'system/player_details.html'


class AddPlayerView(CreateView):
    model = PlayerStat
    template_name = 'system/add_player.html'
    fields = '__all__'

class UpdatePlayerView(UpdateView):
    model = PlayerStat
    template_name = 'system/update_player.html'
    fields = '__all__'

class DeletePlayerView(DeleteView):
    model = PlayerStat
    template_name = 'system/delete_player.html'
    success_url = reverse_lazy('playerstat')

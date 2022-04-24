from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from system.helpers.FormValidationJS import FormValidationErrorsJS, ConfirmPasswordErrorJS
from ...models import Team
from django.urls import reverse_lazy

class HomeView(ListView):  # list all article posts on news page
    model = Team
    template_name = 'system/teams/teams.html'
    ordering = ['-id']  # this puts oldest articles at the bottom

class TeamDetailView(DetailView):  # puts one news article on page
    model = Team
    template_name = 'system/teams/team_details.html'

class AddTeamView(CreateView):
    model = Team
    template_name = 'system/teams/add_team.html'
    fields = '__all__'


class UpdateTeamView(UpdateView):
    model = Team
    template_name = 'system/teams/update_team.html'
    fields = '__all__'


class DeleteTeamView(DeleteView):
    model = Team
    template_name = 'system/teams/delete_team.html'
    success_url = reverse_lazy('teams')
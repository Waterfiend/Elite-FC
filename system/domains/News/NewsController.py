from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from system.helpers.FormValidationJS import FormValidationErrorsJS, ConfirmPasswordErrorJS
from ...models import Post
from django.urls import reverse_lazy

# def create(request):
#     if request.method == 'POST':
#         form = listingForm(request.POST, request.FILES) 

class HomeView(ListView):  # list all article posts on news page
    model = Post
    template_name = 'system/news.html'
    ordering = ['-id']  # this puts oldest articles at the bottom

class HomeViewFront(ListView):
    model = Post
    template_name  = 'system/news_frontend.html'
    ordering = ['-id']

class ArticleDetailView(DetailView):  # puts one news article on page
    model = Post
    template_name = 'system/article_details.html'

class ArticleDetailViewFront(DetailView):
    model = Post
    template_name = 'system/article_det_frontend.html'

class AddPostView(CreateView):
    model = Post
    template_name = 'system/add_post.html'
    fields = '__all__'


class UpdatePostView(UpdateView):
    model = Post
    template_name = 'system/update_post.html'
    fields = ['title', 'body','image']


class DeletePostView(DeleteView):
    model = Post
    template_name = 'system/delete_post.html'
    success_url = reverse_lazy('news')
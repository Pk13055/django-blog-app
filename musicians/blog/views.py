from django.urls import reverse
from django.urls.base import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import DeleteView, UpdateView

from blog.models import Blog, Entry


class BlogListView(ListView):
    """Displays all the blogs in a paginated fashion"""

    template_name = "blog/blog_list.html.j2"
    context_object_name = 'blogs'
    paginate_by = 10
    model = Blog


class BlogDeleteView(DeleteView):
    """Displays a confirmation for the deletion of a blog"""

    template_name = 'blog/blog_delete_confirm.html.j2'
    model = Blog
    context_object_name = 'blog'
    success_url = reverse_lazy('blog:blog_list')


class EntryListView(ListView):
    """Displays all the entries in a blog in a paginated fashion"""

    template_name = 'blog/entry_list.html.j2'
    paginate_by = 5
    model = Entry

    def get_queryset(self):
        return super().get_queryset().filter(blog=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blog'] = Blog.objects.get(pk=self.kwargs['pk'])
        return context


class EntryDetailView(DetailView):
    """Displays the details of a particular entry"""

    template_name = 'blog/entry_details.html.j2'
    context_object_name = 'entry'
    model = Entry


class EntryDeleteView(DeleteView):
    """Displays a confirmation for the deletion of an entry"""

    model = Entry
    context_object_name = 'entry'
    template_name = 'blog/entry_delete_confirm.html.j2'

    def get_success_url(self) -> str:
        return reverse('blog:entry_list', kwargs={'pk': self.object.blog_id})


class EntryUpdateView(UpdateView):
    """Update form to update a given entry"""

    template_name = 'blog/entry_update_details.html.j2'
    model = Entry
    fields = ['blog', 'headline', 'body_text', 'pub_date', 'mod_date',
              'number_of_comments', 'number_of_pingbacks', 'rating', 'authors']


class BlogUpdateView(UpdateView):
    """Update form to update a blog"""

    template_name = 'blog/blog_update_details.html.j2'
    model = Blog
    fields = ['name', 'tagline']

from django.urls import reverse
from django.urls.base import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.views import redirect_to_login

from blog.models import Author, Blog, Entry


class UserAccessMixin(PermissionRequiredMixin):
    def dispatch(self, request, *args, **kwargs):

        if not self.request.user.is_authenticated:
            return redirect_to_login(
                self.request.get_full_path(),
                self.get_login_url(),
                self.get_redirect_field_name(),
            )
        if not self.has_permission():
            return redirect(reverse("login"))

        return super().dispatch(request, *args, **kwargs)


class BlogListView(UserAccessMixin, ListView):
    """Displays all the blogs in a paginated fashion"""

    permission_required = ("blog.view_blog",)

    template_name = "blog/blog_list.html.j2"
    context_object_name = "blogs"
    paginate_by = 10
    model = Blog


class BlogCreateView(PermissionRequiredMixin, CreateView):
    """Form to create a new blog"""

    permission_required = ("blog.add_blog",)

    template_name = "blog/blog_create.html.j2"
    model = Blog
    fields = ["name", "tagline"]


class BlogDeleteView(PermissionRequiredMixin, DeleteView):
    """Displays a confirmation for the deletion of a blog"""

    permission_required = ("blog.delete_blog",)

    template_name = "blog/blog_delete_confirm.html.j2"
    model = Blog
    context_object_name = "blog"
    success_url = reverse_lazy("blog:blog_list")


class EntryListView(PermissionRequiredMixin, ListView):
    """Displays all the entries in a blog in a paginated fashion"""

    permission_required = ("blog.view_entry",)
    raise_exception = False

    template_name = "blog/entry_list.html.j2"
    paginate_by = 5
    model = Entry

    def get_queryset(self):
        return super().get_queryset().filter(blog=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["blog"] = Blog.objects.get(pk=self.kwargs["pk"])
        return context


class EntryAuthorListView(PermissionRequiredMixin, ListView):

    permission_required = ("blog.view_entry",)

    template_name = "blog/entry_list.html.j2"
    paginate_by = 5
    model = Entry

    def get_queryset(self):
        return super().get_queryset().filter(authors=self.kwargs["author_id"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["author"] = Author.objects.get(pk=self.kwargs["author_id"])
        return context


class EntryDetailView(PermissionRequiredMixin, DetailView):
    """Displays the details of a particular entry"""

    permission_required = ("blog.view_entry",)

    template_name = "blog/entry_details.html.j2"
    context_object_name = "entry"
    model = Entry


class EntryDeleteView(PermissionRequiredMixin, DeleteView):
    """Displays a confirmation for the deletion of an entry"""

    permission_required = ("blog.delete_entry",)

    model = Entry
    context_object_name = "entry"
    template_name = "blog/entry_delete_confirm.html.j2"

    def get_success_url(self) -> str:
        return reverse("blog:entry_list", kwargs={"pk": self.object.blog_id})


class EntryCreateView(PermissionRequiredMixin, CreateView):
    """Form to create a new entry"""

    permission_required = ("blog.add_entry",)

    model = Entry
    template_name = "blog/entry_create.html.j2"
    fields = [
        "headline",
        "body_text",
        "pub_date",
        "mod_date",
        "number_of_comments",
        "number_of_pingbacks",
        "rating",
        "authors",
    ]

    def form_valid(self, form):
        form.instance.blog = Blog.objects.get(pk=self.kwargs["blog_id"])
        return super().form_valid(form)


class EntryUpdateView(PermissionRequiredMixin, UpdateView):
    """Update form to update a given entry"""

    permission_required = ("blog.change_entry",)

    template_name = "blog/entry_update_details.html.j2"
    model = Entry
    fields = [
        "blog",
        "headline",
        "body_text",
        "pub_date",
        "mod_date",
        "number_of_comments",
        "number_of_pingbacks",
        "rating",
        "authors",
    ]


class BlogUpdateView(PermissionRequiredMixin, UpdateView):
    """Update form to update a blog"""

    permission_required = ("blog.change_blog",)

    template_name = "blog/blog_update_details.html.j2"
    model = Blog
    fields = ["name", "tagline"]

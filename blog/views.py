from django.core.mail import send_mail
from django.views import View
from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .forms import *
from .models import *


# Create your views here.

def list_view(request):
    posts = Post.objects.filter(status=Post.StatusChoices.PUBLISHED, publish_time__lte=timezone.now())
    return render(request, 'blog/list.html', {'posts': posts})


class BlogListView(ListView):
    template_name = 'blog/list.html'
    # model = Post
    queryset = Post.objects.filter(status=Post.StatusChoices.PUBLISHED)
    context_object_name = 'posts'


def detail_view(request, year, month, day, slug):
    post = get_object_or_404(Post, status=Post.StatusChoices.PUBLISHED, publish_time__year=year,
                             publish_time__month=month,
                             publish_time__day=day, slug=slug)
    return render(request, 'blog/detail.html', {'post': post})


class BlogDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'

    def get_object(self, queryset=None):
        return Post.objects.get(status=Post.StatusChoices.PUBLISHED, publish_time__year=self.kwargs['year'],
                                publish_time__month=self.kwargs['month'],
                                publish_time__day=self.kwargs['day'], slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super(BlogDetailView, self).get_context_data()
        context['comments'] = Comment.objects.filter(post=self.get_object(), approved=True)
        context['comments_form'] = CommentForm()
        return context

    def post(self, request, year, month, day, slug):
        post = self.get_object()
        comment_data = CommentForm(request.POST)
        if comment_data.is_valid():
            comment = Comment(post=post,
                              user=request.user,
                              name=comment_data.cleaned_data.get('name'),
                              email=comment_data.cleaned_data.get('email'),
                              body=comment_data.cleaned_data.get('body'),
                              approved=False
                              )
            comment.save()
            self.object = self.get_object()
            return self.render_to_response(context=self.get_context_data())
        else:
            self.object = self.get_object()
            context = self.get_context_data()
            context['comments_form'] = comment_data
            return self.render_to_response(context=context)


def categories_view(request):
    categories = Category.objects.all()
    return render(request, 'blog/categories.html', {'categories': categories})


class SharePost(View):
    def get(self, request, pk):
        form = ShareForm()
        post = get_object_or_404(Post, pk=pk)
        return render(request, 'blog/share.html', {'form': form, 'post': post})

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        form = ShareForm(request.POST)
        if form.is_valid():
            send_mail(
                "Sharing a post".format(post.title),
                form.cleaned_data.get('comment'),
                form.cleaned_data.get('email'),
                form.cleaned_data.get('to'),
                fail_silently=False,
            )
            return redirect(post.get_absolute_url())
        else:
            return render(request, 'blog/share.html', {'form': form, 'post': post})

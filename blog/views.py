from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.http import Http404

from django.views.generic import ListView
from django.views.decorators.http import require_POST

from .forms import EmailPostForm, CommentForm
from .models import Post

# Create your views here. 
class PostListView(ListView):
    """Alternative to post_list function view."""
    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 3
    template_name = "blog/post/list.html"

"""def post_list(request):
    #posts = Post.published.all() #using custom manager to get published posts
    post_list = Post.published.all() #using custom manager to get published posts
    paginator = Paginator(post_list, 3)  #pagination with 3 posts per page.
    #request.GET reads query parameters from the URL (e.g. ?page=2).
    #If no page is given in the URL, it defaults to 1 (the first page).
    page_number = request.GET.get('page', 1) 

    try:
        posts = paginator.page(page_number) #get/fetches posts for the requested page.
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If the page is out of range (e.g. 9999), deliver the last page of results.
        posts = paginator.page(paginator.num_pages) #paginator.num_pages gives total number of pages.

    return render(
        request,
        'blog/post/list.html',
        {'posts' : posts}
    )
"""
"""def post_detail(request, id):
    try:
        post = Post.published.get(id = id) #get post by id using custom manager
    except Post.DoesNotExist:
        raise Http404("No post found.")
    return render(
        request,
        'blog/post/detail.html',
        {'post' : post}
    )
    # Using get_object_or_404 shortcut to simplify the above code
    post = get_object_or_404( 
        Post, id = id, status = Post.Status.PUBLISHED
    )
    return render(
        request, 'blog/post/detail.html',
        {'post' : post}
    ) """

def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post, slug = post,
        status = Post.Status.PUBLISHED,
        publish__year = year,
        publish__month = month,
        publish__day = day,
        )
    #List of active comments for this post.
    comments = post.comments.filter(active = True)
    #Form for users to comment.
    form = CommentForm()
    return render(
        request, 'blog/post/detail.html',
        {
            'post' : post,
            'comments': comments,
            "form" : form,
         },
    )

def post_share(request, post_id):
    #Retrive post by id.
    post = get_object_or_404(
        Post,
        id = post_id,
        status = Post.Status.PUBLISHED,
    )
    sent = False 
    if request.method == "POST":
        #Form was submitted.
        form = EmailPostForm(request.POST)
        if form.is_valid():
            #Form fields passed validation.
            cd = form.cleaned_data #retrive the validated data. 
            post_url = request.build_absolute_uri(
                post.get_absolute_url()
            )
            subject = (
                f"{cd["name"]} ({cd["email"]})"
                f"recommends you read {post.title}"
            )
            message = (
                f"Read {post.title} at {post_url}\n\n"
                f"{cd["name"]}\'s comments: {cd["comments"]}"
            )
            send_mail(
                subject = subject,
                message = message,
                from_email = None,
                recipient_list = [cd["to"]] 
            )
            sent = True
    else:
        form = EmailPostForm()
    return render(
        request,
        "blog/post/share.html",
        {
            "post" : post,
            "form" : form,
            "sent" : sent,
        }
    )    

@require_POST #A decorator to allow only POST requests for the view.
def post_comment(request, post_id):
    post = get_object_or_404(
        Post,
        id = post_id,
        status = Post.Status.PUBLISHED,
    )
    comment = None
    #A comment was posted.
    form = CommentForm(data = request.POST)
    if form.is_valid():
        #Create a COmment object wihtout saving it to the database.
        comment = form.save(commit = False)
        #Assign the post to the comment.
        comment.post = post
        #Save the comment to the database.
        comment.save()

    return render(
        request,
        'blog/post/comment.html',
        {
            'post' : post,
            'form' : form,
            "comment" : comment,
        }
    )
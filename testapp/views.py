from django.shortcuts import render, get_object_or_404, redirect
from testapp.models import Blog
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.mail import send_mail
from testapp.forms import EmailForm, CommentForm, AddPost, SignUp
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout
from django.utils.text import slugify
from django.shortcuts import HttpResponseRedirect
from dcrud import settings
from django.contrib import messages
# Create your views here.


def home(request):
    post_list = Blog.objects.all()
    paginator = Paginator(post_list, 3)
    page_num = request.GET.get('page')
    try:
        post_list = paginator.page(page_num)
    except PageNotAnInteger :
        post_list = paginator.page(1)
    except EmptyPage :
        post_list = paginator.page(paginator.num_pages)


    return render(request, "testapp/home.html", {'post_list':post_list})

@login_required()
def post_detail(request, year, month, day, post):
    post = get_object_or_404(Blog, slug=post, atatus="published", publish__year= year,
                             publish__month=month, publish__day=day)
    comments = post.comments.filter(active= True)
    csubmit = False
    if request.method=='POST':
        form =CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            csubmit=True
    else:
        form = CommentForm()

    return render(request, 'testapp/post.html', {'post':post, 'form':form, 'csubmit':csubmit, 'comments':comments})

def send_email(request, id):
    post = get_object_or_404(Blog, id=id , atatus='published')
    sent= False
    if request.method=="POST":
        form = EmailForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            subject = f"{cd['name']} ({cd['email']})recommended you to read {post.title}"
            post_url = request.build_absolute_uri(post.url())
            message = f"Read Post AT:\n{post_url}\n\n{cd['email']} comments:\n{cd['comments']}"
            send_mail(subject, message, 'hyndhavi9247@gmai.com', [cd['to']])

            sent =True
    else:
        form = EmailForm()
    return render(request, 'testapp/email.html', {'form':form, 'post':post, 'sent':sent})

@login_required()
def add_post(request):
    if request.method=='POST':
        form = AddPost(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = AddPost()
    return render(request,'testapp/add.html',{'form':form})

def log_out(request):
        logout(request)
        return render(request,"testapp/logged_out.html")
        # return redirect('home')

    # messages.success(request, ("You were logged out"))

        # class LogoutView(View):
#     def get(self, request):
#         logout(request)
#         return HttpResponseRedirect(settings.LOGIN_URL)
def sign_up(request):
    form = SignUp()
    if request.method == "POST":
        form = SignUp(request.POST)
        if form.is_valid():
            form.save()
        return redirect("/accounts/login ")
    return render(request,'testapp/signup.html', {'form':form})

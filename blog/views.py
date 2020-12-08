import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import models as django_models
from django.contrib.auth.models import User
from django.views import generic, View
from django.views import View
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from blog.models import Post,Likes
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from blog.forms import BlogForm,LoginForm,SignUpForm,PasswordResetForm
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


class ManagerRequiredMixin(AccessMixin):
	def dispatch(self, request, *args, **kwargs):
		if not request.user.is_authenticated or not hasattr(self.request.user, 'userprofile') or not self.request.user.userprofile.is_manager:
			return self.handle_no_permission()
		return super().dispatch(request, *args, **kwargs)


class PasswordResetView(LoginRequiredMixin, generic.FormView):
	form_class = PasswordResetForm
	success_url = '/blogs'
	template_name = 'password_reset.html'
	login_url = '/login'

	def form_valid(self, form):
		"""If the form is valid, redirect to the supplied URL."""
		self.request.user.set_password(form.cleaned_data['new_password'])
		self.request.user.save()
		update_session_auth_hash(self.request, self.request.user)
		return super().form_valid(form)
		
	def post(self, request, *args, **kwargs):
		form = self.get_form()
		form.user =  self.request.user
		if form.is_valid():
			return self.form_valid(form)
		else:
			return self.form_invalid(form)

class LikeBlog(LoginRequiredMixin,View):
	
	@method_decorator(csrf_exempt)
	def dispatch(self, *args, **kwargs):
		return super().dispatch(*args, **kwargs)
		
	def post(self, request, *args, **kwargs):
		blog_id = kwargs.get('pk')
		blog = get_object_or_404(Post,id=blog_id)
		like_object, created=Likes.objects.get_or_create(
		blog=blog, user=self.request.user
		)
		print(created)
		return HttpResponse('success')
	



#def blog(request):
#	blog=Post.objects.all()
#	return render(request, 'blog.html',{'blogs':blog})

class BlogListView(generic.ListView):
	paginate_by = 1
	template_name = 'blog.html'
	context_object_name = 'blogs'
	queryset = Post.objects.filter()

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['now'] = datetime.datetime.now()
		return context

def home(request):
    return render(request, 'home.html',{'home':home})

class Login(View):
	def get(self, request):
		form = LoginForm()
		return render(request, 'login.html', {'form': form})
	
	def post(self, request):
		form = LoginForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = django_models.User.objects.filter(username=username).first()
			if user:
				if user.check_password(password):
					login(request, user)
					return redirect('/blogs')
				else:
					return render(request, 'login.html', {'form': form, 'error': 'Invalid Credentials'})
			else:
				return render(request, 'login.html', {'form': form, 'error': 'User not found'})
		else:
			return render(request, 'login.html', {'form': form})

    

#def blog_detail(request,blog_id):
   # blog = Post.objects.filter(id=blog_id).first()
    #return render(request, 'blog_detail.html', {'blog': blogs})

class BlogDetailView(generic.DetailView):
	model = Post
	template_name = 'blog_detail.html'
	context_object_name = 'blog'
	def get_context_data(self,**kwargs):
		context=super().get_context_data(**kwargs)
		if self.request.user.is_authenticated:
			context['liked']=Likes.objects.filter(
				user=self.request.user,blog=self.get_object()
				).exists()
		return context
	
	
    # def get_object(self):
    #     obj = self.get_queryset().filter(id=1).first()
    #     print(obj)
    #     return obj

#class UpdateBlogView(generic.UpdateView):
#	success_url = '/blogs'
#	template_name = 'add_blog.html'
#	form_class = BlogForm
#	model = Post

class UpdateBlogView(LoginRequiredMixin, generic.UpdateView):
	success_url = '/blogs'
	template_name = 'add_blog.html'
	form_class = BlogForm
	model = Post
	login_url = '/login'
	
	def get_queryset(self):
		if hasattr(self.request.user, 'userprofile') and self.request.user.userprofile.is_manager:
			return super().get_queryset()
		return super().get_queryset().filter(created_by=self.request.user)
	
#def add_blog(request):
#	if request.method == 'GET':
#		form = BlogForm()
#		return render(request, 'add_blog.html', {'form': form})
#	else:
#		form = BlogForm(request.POST,request.FILES)
#		print(request.FILES)
#		if form.is_valid():
		#	form.save()
		#	return redirect('/blogs')
		#else:
		#	return render(request, 'add_blog.html', {'form': form}
class AddBlogCreateView(LoginRequiredMixin, generic.CreateView):
	login_url = '/login'
	success_url = '/blogs'
	template_name = 'add_blog.html'
	form_class = BlogForm
	
	def get_success_url(self):
		if self.request.user.is_authenticated:
			self.object.created_by = self.request.user
			self.object.save()
		return super().get_success_url()
	

	


#def delete_blog(request,id):
#	blog = Post.objects.get(id=id)
#	if request.method == 'POST':
#		blog.delete()
#		return redirect('/blog')
#	return render(request, 'delete_blog.html')

class DeleteBlogView(ManagerRequiredMixin, generic.DeleteView):
	"""
	Only manager can delete the product
	"""
	success_url = '/blogs'
	model = Post
	login_url = '/login'
	
	def get(self, request, *args, **kwargs):
		return self.delete(request, *args, **kwargs)


class UserDetailView(generic.DetailView):
	model = User
	template_name='user_detail.html'
	context_object_name='user'

	def get_context_data(self,**kwargs):
		context=super().get_context_data(**kwargs)
		context['blogs']=Post.objects.filter(created_by=self.get_object())
		return context

class UserProfileView(LoginRequiredMixin, generic.DetailView):
	login_url = '/login'
	model = User
	template_name = 'user_detail.html'
	context_object_name = 'user'

	def get_object(self):
		return self.request.user

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['blogs'] = Post.objects.filter(created_by=self.get_object())
		return context


def logout_user(request):
	logout(request)
	messages.success(request,('Youre now logged out'))
	return redirect('/home')

def register_user(request):
	if request.method =='POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request,user)
			messages.success(request, ('Youre now registered'))
			return redirect('/home')
	else: 
		form = SignUpForm() 

	context = {'form': form}
	return render(request, 'register.html', context)

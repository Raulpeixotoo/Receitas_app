from django.shortcuts import render,redirect, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout, login
from .models import Recipe, Profile, Follow
from .forms import ProfileForm

def home(request):
    if request.user.is_authenticated:
        # Feed personalizado: receitas dos perfis seguidos
        following = Follow.objects.filter(follower=request.user).values_list('followed', flat=True)
        recipes = Recipe.objects.filter(author__in=following).order_by('-created_at')
        recipes = Recipe.objects.all().order_by('-created_at')
    else:
        # Feed público: todas as receitas
        recipes = Recipe.objects.all().order_by('-created_at')
    
    print(recipes)  # Debug: Verifica se há receitas no terminal
    return render(request, 'recipes/home.html', {'recipes': recipes})

def custom_logout(request):
    logout(request)
    return redirect('home')  # Redireciona para a página inicial após o logout

@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    recipes = user.recipes.all()  # Receitas criadas pelo usuário

    # seguindo
    following_count = Follow.objects.filter(follower=user).count()
    following_users = Follow.objects.filter(follower=user).values_list('followed', flat=True)

    # Seguidores
    followers_count = Follow.objects.filter(followed=user).count()
    followers_users = Follow.objects.filter(followed=user).values_list('follower', flat=True)

    is_following = False
    if request.user.is_authenticated:
        is_following = Follow.objects.filter(follower=request.user, followed=user).exists()

    return render(request, 'recipes/profile.html', {
        'profile': profile,
        'recipes': recipes,
        'is_following': is_following,
        'following_count': following_count,
        'followers_count': followers_count,
        'following_users': User.objects.filter(id__in=following_users),
        'followers_users': User.objects.filter(id__in=followers_users)
    })

@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile', username=request.user.username)
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'recipes/edit_profile.html', {'form': form})


@login_required
def create_recipe(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        ingredients = request.POST['ingredients']
        instructions = request.POST['instructions']
        image = request.FILES.get('image')  # Obtém a imagem enviada pelo formulário

        recipe = Recipe.objects.create(
            title=title,
            description=description,
            ingredients=ingredients,
            instructions=instructions,
            author=request.user,
            image=image  # Salva a imagem no modelo
        )
        return redirect('recipe_detail', pk=recipe.pk)
    return render(request, 'recipes/create_recipe.html')

def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})

@login_required
def like_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if request.user in recipe.likes.all():
        recipe.likes.remove(request.user)
    else:
        recipe.likes.add(request.user)
    return redirect('recipe_detail', pk=pk)

@login_required
def follow_user(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    follow, created = Follow.objects.get_or_create(follower=request.user, followed=user_to_follow)
    if not created:
        follow.delete()
    return redirect('profile', username=username)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'recipes/register.html', {'form': form})
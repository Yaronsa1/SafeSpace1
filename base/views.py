from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Comment, Place, Restrictions, User
from base.forms import PlaceForm, UserForm, MyUserCreationForm
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.core.mail import send_mail, BadHeaderError
from django.utils.encoding import force_bytes
from django.contrib import messages

# Create your views here.


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "email.txt"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'admin@example.com', [user.email], fail_silently=True)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    messages.success(request, 'A message with reset password instructions has been sent to your inbox.')
                    return redirect('/password_reset/done')
            messages.error(request, 'An invalid email has been entered.')
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="password_reset.html",
                  context={"password_reset_form": password_reset_form})

def loginPage(request):
    page ='loginPage'
    if request.user.is_authenticated:
        return redirect('homePage')
    if request.method == 'POST':
        userName = request.POST.get('username') #####
        password = request.POST.get('password')
        try:
            user = User.objects.get(username = userName) 
        except:
            messages.error(request, 'שם המשתמש לא קיים במערכת') 
        user = authenticate(request, username = userName, password = password)
        if user is not None:
            login(request, user)
            return redirect('homePage')
        else:
            messages.error(request, 'שם המשתמש או סיסמה אינם נכונים') 
    context = {'page':page}
    return render(request, 'base/loginRegister.html',context)



def logoutPage(request):
    logout(request)
    return redirect('homePage')

def registerPage(request):
    page = 'register'
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username #####
            user.save()
            login(request,user)
            return redirect('homePage')
        else:
            messages.error(request, 'חלה שגיאה במהלך ההרשמה לאתר')
    context={'page':page,'form':form}
    return render(request, 'base/loginRegister.html', context)


def businessOwnerRegisterPage(request):
    page = 'businessRegister'
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username 
            user.permission = 1
            user.save()
            login(request,user)
            return redirect('createPlace')
        else:
            messages.error(request, 'על הסיסמה להיות בעלת 8 תווים לפחות הכוללים מספרים וסמלים')
    context={'page':page,'form':form}
    return render(request, 'base/loginRegister.html', context)

def homePage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    places = Place.objects.filter(
        Q(restrictions__name__icontains = q) |
        Q(name__icontains = q) |
        Q(description__icontains = q) |
        Q(placePhoneNumber__icontains = q)).distinct()
    placesComments = Comment.objects.filter(Q(place__restrictions__name__icontains = q)).distinct()
    restrictions = Restrictions.objects.all()
    context = {'places':places,'restrictions':restrictions,'placesComments':placesComments}
    return render(request, 'base/homePage.html',context)


def placePage(request,primaryKey):
    currentPlace = Place.objects.get(id = primaryKey)
    comments = currentPlace.comment_set.all()
    restrictions = Restrictions.objects.all()
    if request.method == "POST":
        comment = Comment.objects.create(
            owner = request.user,
            place = currentPlace,
            body = request.POST.get('body'),
        )
        return redirect('placePage', primaryKey = currentPlace.id)
    context = {'place':currentPlace, 'placesComments':comments,'restrictions':restrictions}
    return render(request, 'base/placePage.html',context)

@login_required (login_url= 'loginPage')
def userProfile(request,primaryKey):
    currentUser = User.objects.get(id = primaryKey)
    place = currentUser.place_set.all()
    placeComments = currentUser.comment_set.all()
    restrictions = Restrictions.objects.all()
    context = {'currentUser':currentUser,'places':place,'placesComments':placeComments,'restrictions':restrictions}
    return render(request, 'base/profile.html',context)

@login_required (login_url= 'loginPage')
def createPlace(request):
    form = PlaceForm()
    restrictions = Restrictions.objects.all()
    if request.method == 'POST':
        form = PlaceForm(request.POST)
        if form.is_valid():
            request.user.haveBusiness = True
            request.user.save()
            place = form.save(commit=False)
            place.owner = request.user
            place.save()
            return redirect('homePage')
            #return redirect(request, place.id)
    context = {'form':form,'restrictions':restrictions}
    return render(request, 'base/placeForm.html', context)

@login_required (login_url= 'loginPage')
def updatePlace(request,primaryKey):
    place = Place.objects.get(id = primaryKey)
    restrictions = Restrictions.objects.all()
    form = PlaceForm(instance=place)
    if request.user != place.owner:
        return HttpResponse('אינך ראשי/ת לבצע פעולה זו')
    if request.method == 'POST':
        form = PlaceForm(request.POST,instance = place)
        if form.is_valid():
            form.save()
            return redirect('homePage')
    context = {'form':form,'restrictions':restrictions}
    return render(request, 'base/placeForm.html', context)

@login_required (login_url= 'loginPage')
def deletePlace(request,primaryKey):
    place = Place.objects.get(id = primaryKey)
    if request.user != place.owner:
        return HttpResponse('אינך ראשי/ת לבצע פעולה זו')
    if request.method == "POST":
        place.delete()
        request.user.haveBusiness = False 
        request.user.save()
        return redirect('homePage')
    return render(request, 'base/placeDelete.html', {'obj':place})

@login_required (login_url= 'loginPage')
def commentDelete(request,primaryKey):
    currentComment = Comment.objects.get(id = primaryKey)
    if request.user != currentComment.owner:
        return HttpResponse('אינך ראשי/ת לבצע פעולה זו')
    if request.method == "POST":
        currentComment.delete()
        return redirect('homePage')
    return render(request, 'base/commentDelete.html', {'obj':currentComment})

@login_required(login_url= 'loginPage')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('userProfile', primaryKey=user.id)
    return render(request,'base/updateUser.html',{'form':form})

def contactUs(request):
    return render(request, 'base/contactUs.html')

#mobile
def restrictionsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    restrictions = Restrictions.objects.filter(name__icontains=q)
    return render(request, 'base/restrictions.html', {'restrictions':restrictions})

def activityPage(request):
    comments = Comment.objects.all()
    return render(request, 'base/activity.html',{'comments':comments})

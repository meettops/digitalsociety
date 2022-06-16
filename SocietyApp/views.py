import profile
from random import randint
from email.policy import default
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import redirect, render
from .models import *
from django.core.mail import send_mail
from django.conf import settings
from .paytm_checksum import generate_checksum, verify_checksum
from django.views.decorators.csrf import csrf_exempt

default_data ={
    'app_name':'Digital Society',
    'pages': [ 'signin', 'signup', 'otp','complain',],
    'page': 'index',
    'user_types': UserType.objects.all(),
    
}


def index(request):
    return render(request,'signin_page.html')

def signup_page(request):
    return render(request,'signup_page.html', default_data)

def security_page(request):
    return render(request,'security_page.html',default_data)

def otp_page(request):
    return render(request,'otp_page.html',default_data)

def payment_page(request):
    return render(request,'payment_page.html',default_data)

def event_page(request):
    load_event(request)
    return render(request,'event_page.html',default_data)

def society_rules_page(request):
    load_society_rules(request)
    return render(request,'society_rules_page.html',default_data)

def complain_page(request):
    load_user_complains(request)
    return render(request,'complain_page.html',default_data)


def profile_page(request):
    profile_data(request)
    return render(request,'profile_page.html',default_data)







def load_user_complains(request):
    master = Master.objects.get(Email = request.session['email'])
    
    com=Complain.objects.all()

    default_data['load_user_complains'] = com


def change_complain(request):
    master = Master.objects.get(Email = request.session['email'])
    user=User.objects.get(Master=master)
    
    Complain.objects.create(
        User=user,
        Title=request.POST['title'],
        Complain=request.POST['complain'],
    )

    return redirect(complain_page)   

def load_society_rules(request):
    master = Master.objects.get(Email = request.session['email'])
    
    soc_rules=Society_rules.objects.all()

    default_data['load_society_rules'] = soc_rules


def change_soc_rules(request):
    master = Master.objects.get(Email = request.session['email'])
    profile=Profile.objects.get(Master=master)
    
    Society_rules.objects.create(
        Master=master,
        Title=request.POST['title'],
        Society_rules=request.POST['society_rules'],
    )

    return redirect(society_rules_page)   

def load_event(request):
    master = Master.objects.get(Email = request.session['email'])
    
    event=Event.objects.all()

    default_data['load_event'] = event


def change_event(request):
    master = Master.objects.get(Email = request.session['email'])
    user=User.objects.get(Master=master)
    
    Event.objects.create(
        User=user,
        Eventname=request.POST['eventname'],
        Eventdescription=request.POST['eventdescription'],
    )

    return redirect(event_page)   




    


 
def user_profile_page(request):
    profile_data(request)
    return render(request,'user_profile_page.html',default_data)


def profile_data(request):
    master=Master.objects.get(Email= request.session['email'])
    role = master.UserType.Type

    if role == 'User':
        user=User.objects.get(Master=master)
        default_data['user_profile_page'] = user
    else:
        profile=Profile.objects.get(Master=master)
        default_data['profile_data'] = profile
     

def update_profile(request):
    master=Master.objects.get(Email= request.session['email'])
    user = ''
    role = master.UserType.Type
    # role_user = (role == 'User' or role == 'Admin')

    if  role=='User':
        user=User.objects.get(Master=master)
        user.Firstname = request.POST['firstname']
        user.Lastname =request.POST['lastname']
        user.Address =request.POST['address']
        user.City =request.POST['city']
        user.Country =request.POST['country']
        user.Mobile =request.POST['mobile']
        
    
        print('update data:',request.POST)
        user.save()
        return redirect(user_profile_page)
    else:
        profile=Profile.objects.get(Master=master)
        profile.FullName = request.POST['fullname']
        profile.Mobile =request.POST['mobile']
        profile.Address =request.POST['address']
        profile.Email =request.POST['email']


        print('update data:',request.POST)
     

        profile.save()

        return redirect(profile_page)

def change_password(request):
    master=Master.objects.get(Email= request.session['email'])
   
    role = master.UserType.Type
    role_user = (role == 'User' or role == 'Admin')

    if  role_user:
        if master.Password == request.POST['currentPassword']:
            if request.POST['newPassword'] == request.POST['confirmNewPassword']:
                master.Password = request.POST['newPassword']
                master.save()
                print('password change successful.')
            else:
                print('password are differnt.')
        else:
            print('invalid current Password.')
        return redirect(security_page)
    else:
        pass
        
        
#generate otp
#otp
def create_otp(request):
    email_to_list = [request.session['reg_data']['email'],]
    
    subject = 'OTP for DS Registration'
    

    otp = randint(1000,9999)

    print('OTP is: ', otp)

    request.session['otp'] = otp

    message = f"Your One Time Password for verification is: {otp}"
    
    email_from = settings.EMAIL_HOST_USER

    send_mail(subject, message, email_from, email_to_list)

# verify otp
@csrf_exempt
def verify_otp(request):
    master=Master.objects.get(Email= request.POST['email'])
    role = master.UserType.Type

    if role == 'User':
        if request.method == 'POST':
            otp = int(request.POST['otp'])

            if otp == request.session['otp']:
                user = User.objects.create(
                    
                    Email = request.session['reg_data']['email'],
                    Password = request.session['reg_data']['password'],
                    IsActive = True,
                )
                User.objects.create(
                    User = user,
                )

                del request.session['otp']
                del request.session['reg_data']

                print('otp verify success!')
            else:
                print('invalid otp')
                return redirect(otp_page)
            return redirect(signup_page)
        else:
            pass
    else:
        if request.method == 'POST':
            otp = int(request.POST['otp'])

            if otp == request.session['otp']:
                master = Master.objects.create(
                Email = request.session['reg_data']['email'],
                Password = request.session['reg_data']['password'],
                IsActive = True,
                )
                Profile.objects.create(
                    Master = master,
                )

                del request.session['otp']
                del request.session['reg_data']

                print('otp verify success!')
            else:
                print('invalid otp')
                return render(otp_page)
            return redirect(signup_page)
        else:
            pass

# def verify_otp(request, verify_for='reg'):
#     if request.method == 'POST':
#         if int(request.POST['otp']) == request.session['otp']:
#             master = Master.objects.get(Email=request.session['email'])
#             role = master.UserType.Type
#             if verify_for == 'rec':
#                 return JsonResponse({'url': 'otp_page_pass'})
#             elif verify_for == 'activate':
#                 master.IsActive = True
#                 master.save()

                
#                 return JsonResponse({'url': 'login_page'})
#             else:
#                 master.IsActive = True
#                 uid = f"{master.role}-{master.id}{datetime.now().strftime('%Y%m')}".upper()

                
#                 if role == 'User':
#                     User.objects.create(Master=master)
#                 else:
                    
#                     Profile.objects.create(Master=master)

#             master.save()

#             del request.session['otp'],
#             del request.session['email']
            
#             return JsonResponse({'url': 'login_page'})
#         else:
            
#             return render(request, 'otp_page.html')
#     else:
#         return render(request, 'otp_page.html')
# def signup(request):
#     print(request.POST)
#     request.session['reg_data'] = {

#         'email': request.POST['email'],
#         'password': request.POST['password'],
#     }

    
    
#     create_otp(request)

    

#     return redirect(otp_page)

def signup(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user_type_id = int(request.POST['user_type'])
        
        try:
            user_type = UserType.objects.get(id = user_type_id)
            
            master = Master.objects.create(
                Email = email,
                Password = password,
                UserType = user_type,
            )
            print(request.POST)
            request.session['reg_data']={
                'email': request.POST['email'],
                'password': request.POST['password'],
            }

            if user_type.Type == 'Admin':
                Profile.objects.create(Master=master)
            else:
                User.objects.create(Master=master)
            create_otp(request)

        except Exception as err:
            print('Error in register view: ', err)
            
               
        
        return redirect(otp_page)

    else:
        pass


# def signup(request):
#     print(request.POST)
#     master=Master.objects.create(
#         Email= request.POST['email'],
#         Password=request.POST['password'],
#         UserType =request.POST['user_type'],
        

#     )

#     Profile.objects.create(
#         Master=master,
       
#     )    
#     return redirect(index)

def signin(request):
    try:
        master=Master.objects.get(Email= request.POST['email'])
        role = master.UserType.Type
        if role=='User':
           if  master.Password==request.POST['password']:
                request.session['email']= master.Email
                return redirect(user_profile_page)
            # else:
            #     print('---------- incorrect password')
        
        elif master.Password==request.POST['password']:
            request.session['email']= master.Email
            return redirect(profile_page)
        else:
            print('---------- incorrect password')

    except Master.DoesNotExist as err:
        print('record not found.',err)
    return redirect(index)
    
        
    




def signout(request):
    if 'email' in request.session:
        del request.session['email']
        
    return redirect(index)



def initiate_payment(request):
    
    try:
        amount = 1000
        master = Master.objects.get(Email=request.session['email'])
        user = Profile.objects.get(Master=master)

        if user is None:
            raise ValueError
        
    except:
        print('Wrong Accound Details or amount')
        return redirect(profile_page)

    transaction = Transaction.objects.create(made_by=user, amount=amount)
    transaction.save()
    merchant_key = settings.PAYTM_SECRET_KEY

    params = (
        ('MID', settings.PAYTM_MERCHANT_ID),
        ('ORDER_ID', str(transaction.order_id)),
        ('CUST_ID', str(transaction.made_by.Master.Email)),
        ('TXN_AMOUNT', str(transaction.amount)),
        ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
        ('WEBSITE', settings.PAYTM_WEBSITE),
        # ('EMAIL', request.user.email),
        # ('MOBILE_N0', '9911223388'),
        ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
        ('CALLBACK_URL', 'http://127.0.0.1:8000/callback/'),
        # ('PAYMENT_MODE_ONLY', 'NO'),
    )

    paytm_params = dict(params)
    checksum = generate_checksum(paytm_params, merchant_key)

    transaction.checksum = checksum
    transaction.save()

    paytm_params['CHECKSUMHASH'] = checksum
    print('SENT: ', checksum)
    return render(request, 'redirect.html', context=paytm_params)

@csrf_exempt
def callback(request):
    if request.method == 'POST':
        received_data = dict(request.POST)
        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
        if is_valid_checksum:
            received_data['message'] = "Checksum Matched"
        else:
            received_data['message'] = "Checksum Mismatched"
            return render(request, 'callback.html', context=received_data)
        return render(request, 'callback.html', context=received_data)
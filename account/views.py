from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from .models import doctor, patient,blogs
from django.contrib.auth.hashers import check_password

def doc_sign(request):
    if request.method == 'POST':
        first_name = request.POST['first']
        last_name = request.POST['last']
        img = request.FILES.get('image')
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password']
        password2 = request.POST['confirm_password']
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        pincode = request.POST['pincode']

        if doctor.objects.filter(username=username).exists():
            messages.info(request, 'Username already exists')
            return render(request, 'signup.html', {'name': 'doctor'})

        if doctor.objects.filter(email_id=email).exists():
            messages.info(request, 'Email already exists')
            return render(request, 'signup.html', {'name': 'doctor'})

        if password1 != password2:
            messages.info(request, 'Passwords not matching')
            return render(request, 'signup.html', {'name': 'doctor'})

        hashed_password = make_password(password1)

        doc_user = doctor(
            first_name=first_name,
            Last_name=last_name,
            profile_pic=img,
            username=username,
            email_id=email,
            password=hashed_password,  # Store hashed password
            address=address,
            city=city,
            state=state,
            pincode=pincode
        )
        doc_user.save()
        messages.success(request, 'Registered successfully')
        return redirect('doc_login')  # Redirect to login page

    return render(request, 'signup.html', {'name': 'doctor'})

def pat_sign(request):
    if request.method == 'POST':
        first_name = request.POST['first']
        last_name = request.POST['last']
        img = request.FILES.get('image')
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password']
        password2 = request.POST['confirm_password']
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        pincode = request.POST['pincode']

        if patient.objects.filter(username=username).exists():
            messages.info(request, 'Username already exists')
            return render(request, 'signup.html', {'name': 'patient'})

        if patient.objects.filter(email_id=email).exists():
            messages.info(request, 'Email already exists')
            return render(request, 'signup.html', {'name': 'patient'})

        if password1 != password2:
            messages.info(request, 'Passwords do not match')
            return render(request, 'signup.html', {'name': 'patient'})

        hashed_password = make_password(password1)

        pat_user = patient(
            first_name=first_name,
            Last_name=last_name,
            profile_pic=img,
            username=username,
            email_id=email,
            password=hashed_password,  # Store hashed password
            address=address,
            city=city,
            state=state,
            pincode=pincode
        )
        pat_user.save()
        messages.success(request, 'Registered successfully')
        return redirect('pat_login')  # Redirect to login page

    return render(request, 'signup.html', {'name': 'patient'})

def doc_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        email_exist = doctor.objects.filter(email_id=email).exists()
        if email_exist:
            user = doctor.objects.get(email_id=email)

            #Using check_password() to verify hashed password
            if check_password(password, user.password):
                request.session['doctor_id'] = user.id
                request.session['doctor_name'] = user.username  # Store doctor's name in session
                bl=blogs.objects.filter(draft=False).all()
                b2=blogs.objects.filter(draft=True).all()
                return render(request,'blog.html',{'obj':user,'name':'doctor','blogs':bl,'drafts':b2}) 
            else:
                messages.info(request, 'Invalid credentials')
                return render(request, 'login.html', {'name': 'doctor'})
        else:
            messages.info(request, 'Invalid credentials')
            return render(request, 'login.html', {'name': 'doctor'})
    
    return render(request, 'login.html', {'name': 'doctor'})


def pat_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        email_exist = patient.objects.filter(email_id=email).exists()
        if email_exist:
            user = patient.objects.get(email_id=email)

            #Using check_password() to verify hashed password
            if check_password(password, user.password):
                request.session['patient_id'] = user.id
                request.session['patient_name'] = user.username  # Store doctor's name in session
                bl=blogs.objects.filter(draft=False).all()
                return render(request,'blog.html',{'obj':user,'name':'patient','blogs':bl}) 
            else:
                messages.info(request, 'Invalid credentials')
                return render(request, 'login.html', {'name': 'patient'})
        else:
            messages.info(request, 'Invalid credentials')
            return render(request, 'login.html', {'name': 'patient'})
    
    return render(request, 'login.html', {'name': 'patient'})

def blog_list(request):
    if request.method=="POST":
        title=request.POST['title']
        img=request.FILES.get('image')
        category=request.POST['category']
        summary=request.POST['summary']
        words=summary.split()
        summary=' '.join(words[:15])+('...' if len(words)>15 else '')
        content=request.POST['content']
        draft=request.POST.get('draft', 'off') == 'on'
        blog=blogs(title=title,img=img,category=category,summary=summary,content=content,draft=draft)
        blog.save()
        messages.info(request, 'blog created successsfully!')
        return redirect('blog_form')
    else:
        return render(request,'blog_form.html')
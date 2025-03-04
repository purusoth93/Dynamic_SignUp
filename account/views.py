from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .models import doctor, patient, blogs, booking
from googleapiclient.discovery import build
from google.oauth2 import service_account
import datetime

# Google Calendar API Setup
SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = 'service-account.json'  # Ensure this file is in the project root
CALENDAR_ID = 'dd31f36e3b86035cce4d29041198fe71e814095c42863c876ca43cf3b500ed84@group.calendar.google.com'  # Replace with your Calendar ID

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
                d1=doctor.objects.all()
                return render(request,'blog.html',{'obj':user,'name':'patient','blogs':bl,'doctors':d1}) 
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
    
def create_calendar_event(doc_name, pat_name, date, start_time, end_time, spec):
    """Create an event in Google Calendar."""
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('calendar', 'v3', credentials=creds)

    event = {
        'summary': f'Appointment with Dr. {doc_name}',
        'description': f'Patient: {pat_name}\nSpecialization: {spec}',
        'start': {
            'dateTime': f'{date}T{start_time}',
            'timeZone': 'Asia/Kolkata',
        },
        'end': {
            'dateTime': f'{date}T{end_time}',
            'timeZone': 'Asia/Kolkata',
        },
    }

    try:
        event_response = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
        print(f"DEBUG: Event created successfully: {event_response}")
    except Exception as e:
        print(f"ERROR: Failed to create event - {e}")

def book(request, id):
    """Handle booking of an appointment."""
    if request.method == "POST":
        doc_name = request.POST['doctor']
        pat_name = request.POST['patient']
        spec = request.POST['specialist']
        date = request.POST['date']
        start_time = request.POST['time'].strip()  

        try:
            # Convert start_time (12-hour format with AM/PM) to 24-hour format
            start_time_obj = datetime.datetime.strptime(start_time, "%I:%M %p")
            end_time_obj = start_time_obj + datetime.timedelta(minutes=45)

            # Format to Google Calendar's required format (HH:MM:SS)
            start_time_formatted = start_time_obj.strftime("%H:%M:%S")
            end_time_formatted = end_time_obj.strftime("%H:%M:%S")

            # Save appointment in database
            appoint = booking(
                doc_name=doc_name,
                pat_name=pat_name,
                spec=spec,
                book_date=date,
                start_time=start_time_formatted,
                end_time=end_time_formatted
            )
            appoint.save()

            # Add to Google Calendar
            create_calendar_event(doc_name, pat_name, date, start_time_formatted, end_time_formatted, spec)

            messages.success(request, 'Appointment booked and added to Google Calendar!')
            return render(request, 'book_success.html', {
                'doc_name': doc_name,
                'pat_name': pat_name,
                'spec': spec,
                'date': date,
                'start_time': start_time_formatted,
                'end_time': end_time_formatted
            })

        except ValueError as e:
            messages.error(request, f"Invalid time format: {e}")
            print(f"ERROR: {e}")  # Debugging
            return redirect('book', id=id)

    else:
        doc = get_object_or_404(doctor, id=id)
        return render(request, 'book.html', {'doc': doc})
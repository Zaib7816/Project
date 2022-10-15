from unicodedata import name
from django.db.models import Max, Avg
from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib import messages
from . import db
from .models import University
import os
import joblib as jb


def index(request):
    if request.method == 'POST':
       search = request.POST['search']
       universities = University.objects.filter(name__icontains=search)
    else:   
        universities = University.objects.all
    if db.cities_data():
        cities = db.cities_data()
    about = db.about_data()

    return render(request, 'index.html', {'universities': universities, 'cities': cities, 'about': about})


def register_page(request):
    cities_data = db.cities_data()
    return render(request, 'register.html', {'cities_data': cities_data})


def register(request):
    if request.method == 'POST':

        name = request.POST.get('name', 'default')
        email = request.POST.get('email', 'default')
        password = request.POST.get('password', 'default')
        confirm_password = request.POST.get('confirm_password', 'default')
        city = request.POST.get('city', 'default')
        role = 'user'
        if password != confirm_password:
            print(password, "and", confirm_password)
            messages.error(
                request, 'Password and confirm password does not match')
            return render(request, 'register.html')

        elif db.students_data():
            data = db.students_data()
            for i in data:
                if i[2] == email:
                    messages.error(request, 'Email already exists')
                    return render(request, 'register.html')

        if len(password) < 8:
            messages.error(request, 'Password must be atleast 8 characters')
            return render(request, 'register.html')

        elif db.insert(name, email, password, confirm_password, city, role):
            messages.success(request, 'Registration successful')
            return render(request, 'register.html')

    return render(request, 'register.html')


def login_page(request):
    return render(request, 'login.html')


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if db.login_funtion(email, password):
            data = db.login_funtion(email, password)
            name = data[0][1]
            role = data[0][6]
            user_id = data[0][0]
            if role == 'admin':
                request.session['user_id'] = user_id
                request.session['user_role'] = role
                return redirect('admin')
            else:
                request.session['user_id'] = user_id
                request.session['user_role'] = role
                request.session['user_name'] = name

                return redirect('user')

        else:
            messages.error(request, 'Invalid email or password')
    return render(request, 'login.html')


def student_page(request):
    if request.method == 'POST':
        search = request.POST.get('search', 'default')
        data = db.student_search(search)
    else:
        data = db.only_student_data()

    return render(request, 'admin/manage_students.html', {'data': data})


def admin(request):
    data = db.admin_data()
    student_data = db.only_student_data()
    count_stu = len(student_data)
    uni_data = University.objects.all()
    count_uni = len(uni_data)
    city_data = db.cities_data()
    count_city = len(city_data)

    return render(request, 'admin/admin.html', {'data': data, 'count_stu': count_stu, 'count_uni': count_uni, 'count_city': count_city})


def user(request):
    id = request.session['user_id']
    print('this is id of user', id)
    data = db.student_data_by_id(id)

    return render(request, 'user/user.html', {'data': data})


def update_admin_profile(request):
    if request.method == 'POST':
        id = request.POST.get('id', 'default')
        name = request.POST.get('name', 'default')
        email = request.POST.get('email', 'default')
        city = request.POST.get('city', 'default')

        if db.update_admin(id, name, email, city,):
            messages.success(request, 'Profile updated successfully')
    return redirect('admin')


def update_uesr_profile(request):
    if request.method == 'POST':
        id = request.POST.get('id', 'default')
        name = request.POST.get('name', 'default')
        email = request.POST.get('email', 'default')
        city = request.POST.get('city', 'default')

        if db.update_user(id, name, email, city,):
            messages.success(request, 'Profile updated successfully')
    return redirect('user')


def delete_student(request, id):

    if db.delete(id):

        messages.success(request, 'Student deleted successfully')
    return redirect('student_page')


def edit_student_profile(request, id):
    data = db.student_data_by_id(id)
    return render(request, 'admin/edit_students_details.html', {'data': data})


def update_student_profile(request):
    if request.method == 'POST':
        id = request.POST.get('id', 'default')
        name = request.POST.get('name', 'default')
        email = request.POST.get('email', 'default')
        password = request.POST.get('password', 'default')
        city = request.POST.get('city', 'default')

        if db.update_student(id, name, email, password, city,):
            messages.success(request, 'Profile updated successfully')
    return redirect('student_page')


def manage_universities(request):
    if db.cities_data():
        data = db.cities_data()

    universities = University.objects.all()

    return render(request, 'admin/manage_universities.html', {'universities': universities})


def add_university_form(request):
    if request.method == 'POST':
        uni = University()
        uni.name = request.POST.get('university_name', 'default')
        uni.city_id = request.POST.get('city_id', 'default')
        city_id = uni.city_id
        if db.select_city_for_university(city_id):
            city = db.select_city_for_university(city_id)
            uni.city = city[0][1]
        uni.low = request.POST.get('low_avg_stu', 'default')
        uni.log_avg = request.POST.get('low_avg_marks', 'default')
        uni.medium = request.POST.get('Mid_avg_stu', 'default')
        uni.medium_avg = request.POST.get('Mid_avg_marks', 'default')
        uni.high = request.POST.get('High_avg_stu', 'default')
        uni.high_avg = request.POST.get('High_avg_marks', 'default')
        uni.uni_link = request.POST.get('uni_link', 'default')
        uni.address = request.POST.get('university_address', 'default')
        uni.description = request.POST.get('description', 'default')
        if len(request.FILES) != 0:
            uni.image = request.FILES['university_img']
            uni.save()
            messages.success(request, 'University added successfully')
            redirect('manage_universities')
    if db.cities_data():
        cities = db.cities_data()

    return render(request, 'admin/add_university_form.html', {'cities': cities})


def delete_universities(request, id):
    print('this is id of user', id)
    if db.uni_delete(id):

        messages.success(request, 'Student deleted successfully')
    return redirect('manage_universities')


def edit_universities(request, id):
    data = University.objects.get(id=id)
    if request.method == 'POST':
        if len(request.FILES) != 0:
            if len(data.image) > 0:
                os.remove(data.image.path)
            data.image = request.FILES['university_img']
        data.name = request.POST.get('university_name', 'default')
        data.address = request.POST.get('university_address', 'default')
        data.save()
        messages.success(request, 'University updated successfully')
        return redirect('manage_universities')
    return render(request, 'admin/edit_universities.html', {'data': data})


def filter_unis_by_city(request, id):
    unis = University.objects.filter(city_id=id)
    return render(request, 'user/filter_unis_by_city.html', {'unis': unis})


def merit_page(request, id):

    if request.method == 'POST':
        year = request.POST.get('year', 'default')
        course = request.POST.get('course', 'default')
        merit = request.POST.get('merit', 'default')

        if db.add_merit(id, year, course, merit):
            messages.success(request, 'Merit Add successfully')
    if db.merit_data(id):
        data = db.merit_data(id)

        return render(request, 'admin/merit_page.html', {'data': data, 'clg_id': id})

    return render(request, 'admin/merit_page.html')


def univeristy_details(request, id):
    uni_data = University.objects.filter(id=id)
    city = uni_data[0].city
    idd = uni_data[0].id
    uni = University.objects.filter(city=city).exclude(id=idd)
    data2 = db.merit_data(id)

    return render(request, 'user/university_details.html', {'uni_data': uni_data, 'data2': data2, 'uni': uni})


def logout(request):
    request.session['user_id'] = ""
    request.session['user_role'] = ""
    request.session['user_name'] = ""

    return redirect('index')


def search_universities(request):
    if request.method == 'POST':
        name = request.POST.get('name', 'default')
        uni = University.objects.filter(name=name)

    return render(request, 'admin/search_universities.html', {'uni': uni})


def delete_merit(request, clg, id):
    if db.delete_merit(id):
        messages.success(request, 'Merit deleted successfully')
        clg = str(clg)
    return redirect('/merit_page/'+clg)


def add_city(request):
    if request.method == 'POST':
        city = request.POST.get('city', 'default')
        if db.add_city(city):
            messages.success(request, 'City added successfully')
    data = db.cities_data()
    return render(request, 'admin/manage_cities.html', {'data': data})


def recommendation(request):
    return render(request, 'user/recommendation.html')


def import_modal(request):
    if request.method == 'POST':
        marks = request.POST.get('marks', 'default')
        city = request.POST.get('city', 'default')
        uni_data = University.objects.filter(city=city)
        model = jb.load('rsapp/University-recommendation.joblib')
        prediction = model.predict([[marks]])
        result = prediction[0]
        if result == "low":
            data = University.objects.all().order_by(
                'low').order_by('-log_avg').order_by('-cgpa')[:3].values()

        elif result == "medium":
            data = University.objects.all().order_by(
                '-medium').order_by('-medium_avg').order_by('-cgpa')[:3].values()
        else:
            data = University.objects.all().order_by(
                'high').order_by('high_avg').order_by('-cgpa')[:3].values()
        return render(request, 'user/recommendation.html', {'result': result, 'data': data , 'uni_data': uni_data})
    else:
        return render(request, 'user/recommendation.html')


def add_feedback(request):
    if request.method == 'POST':

        feedback = request.POST.get('feedback', 'default')
        name = request.session['user_name']
        print(name)
        if db.add_feedback(name, feedback):
            messages.success(request, 'Feedback added successfully')
    return render(request, 'user/feedback.html')


def Manage_feedback(request):
    data = db.feedback_data()

    return render(request, 'admin/manage_feedback.html', {'data': data})


def delete_feedback(request, id):
    if db.delete_feedback(id):
        messages.success(request, 'Feedback deleted successfully')

    return redirect('/Manage_feedback')


def add_to_wishlist(request, id):
    check = db.check_wishlist(id)
    if check:
        messages.error(request, 'already in wishlist')
    else:
        student_id = request.session['user_id']
        db.add_to_wishlist(id, student_id)
        messages.success(request, 'Add to wishlist successfully')
    id = str(id)
    return redirect('/univeristy_details/'+id)


def wishlist(request):
    student_id = request.session['user_id']
    data = db.wishlist_data(student_id)
    data_a = []
    uni_names = []
    for i in data:
        data_a.append(i[1])
    for j in data_a:
        uni_data = University.objects.filter(id=j)
        for b in uni_data:
            uni_names.append(b)
    return render(request, 'user/wish_list.html', {'uni_names': uni_names, 'data_a': data_a})


def near_me(request):
    id = request.session['user_id']
    student_data = db.student_data_by_id(id)
    city = student_data[0][5]
    uni_data = University.objects.filter(city=city)

    return render(request, 'user/near_me.html', {'uni_data': uni_data})


def delete_uni_from_wishlist(request, id):
    student_id = request.session['user_id']
    db.delete_wishlist(id, student_id)
    messages.success(request, 'Delete from wishlist successfully')
    return redirect('/wishlist')


def contact_page(request):
    return render(request, 'user/contact.html')


def about_page(request):
    data = db.about_data()
    return render(request, 'user/about.html',{"data":data})


def send_mail(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        msg = request.POST['message']
        db.send_mail(first_name,last_name, email, msg)
        messages.success(request, 'Mail sent successfully')
    return redirect('contact_page')

def mail_page(request):
    data = db.mails_data()
    
    return render(request,'admin/manage_mails.html',{'data':data})



def delete_mail(request,id):
    db.delete_mail(id)    
    return redirect('mail_page')



def admin_about_page(request):  
    data = db.about_data() 
    return render(request,'admin/about_page.html',{"data":data})

def add_about(request):
    if request.method == 'POST':
        about = request.POST['about']
    db.add_about(about)   
    return redirect('admin_about_page')
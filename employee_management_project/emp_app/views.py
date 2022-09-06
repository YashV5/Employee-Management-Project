from multiprocessing import context
from django.shortcuts import render,HttpResponse
from . models import Employee,Role,Department
from datetime import datetime
from django.db.models import Q
# Create your views here.

def index(request):
    return render(request,'index.html') 

def all_emp(request):
    employees = Employee.objects.all()
    context = {
        "employees":employees
    }
    return render(request,'view_all_emp.html',context) 

def add_emp(request):
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        salary = int(request.POST["salary"])
        bonus = int(request.POST["bonus"])
        phone = int(request.POST["phone"])
        department = int(request.POST["department"])
        role = int(request.POST["role"])
        new_employee = Employee(first_name=first_name,
        last_name=last_name,
        salary=salary,
        bonus=bonus,
        phone=phone,
        department_id=department,
        role_id=role,
        hire_date = datetime.now())
        new_employee.save()
        return HttpResponse("Employee added Successfully")
    elif request.method=="GET":
        return render(request,'add_emp.html')
    else:
        return HttpResponse("An Exception Occured! Employee cant be added") 

def remove_emp(request,employee_id=None):
    if employee_id:
        try:
            delete_employee = Employee.objects.get(id=employee_id)
            delete_employee.delete()
            return HttpResponse("Employee Removed Successfully")
        except:
            return HttpResponse("Please Enter Valid Employee Id")

    employees = Employee.objects.all()
    context = {
        "employees":employees
    }
    return render(request,'remove_emp.html',context) 
    
def filter_emp(request):
    if request.method == "POST":
        name = request.POST['name']
        department = request.POST['department']
        role = request.POST['role']
        employees = Employee.objects.all()
        if name:
            employees = employees.filter(Q(first_name__icontains=name)|Q(last_name__icontains=name))
        if department:
            employees = employees.filter(department__name__icontains=department)
        if role:
            employees = employees.filter(role__name__icontains=role)
        
        context = {
            'employees':employees
        }

        return render(request,"view_all_emp.html",context)
    elif request.method == 'GET':        
        return render(request,'filter_emp.html') 
    else:
        return HttpResponse("An Exception Occurred")

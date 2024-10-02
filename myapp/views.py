from django.shortcuts import render,redirect
from django.views.generic import View
from myapp.forms import CategoryForm,TransactionsForm,TransactionFilterForm,RegistrationForm,SignUpForm
from myapp.models import Category,Transactions
from django.utils import timezone
from django.db.models import Sum
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from myapp.decorators import signin_required
from django.utils.decorators import method_decorator
# Create your views here.

@method_decorator(signin_required,name="dispatch") 
class CategoryCreateView(View):
    
    def get(self,request,*args, **kwargs):
        
        if not request.user.is_authenticated:
            
            messages.error(request,"Invalid session")
            
            return redirect("sign-up")
        
        form_instance=CategoryForm(user=request.user)
        
        qs=Category.objects.filter(owner=request.user)
        
        return render(request,"category_add.html",{"form":form_instance,"categories":qs})
    
    def post(self,request,*args, **kwargs):
        
        if not request.user.is_authenticated:
            
            messages.error(request,"Invalid session")
            
            return redirect("sign-up")
        
        form_instance=CategoryForm(request.POST,user=request.user,files=request.FILES)
        
        if form_instance.is_valid():
            
            # data=form_instamce.cleaned_data
            
            # Category.objects.create(**data)
            
            form_instance.instance.owner=request.user
        
            form_instance.save()
            
            return redirect("category-add")
        
        else:
            
            return render(request,"category_add.html",{"form":form_instance})
        

@method_decorator(signin_required,name="dispatch")       
class CategoryUpdateView(View):
    
    def get(self,request,*args, **kwargs):
        
        id=kwargs.get("pk")
        
        category_object=Category.objects.get(id=id)
        
        form_instance=CategoryForm(instance=category_object,user=request.user)
        
        return render(request,"category_edit.html",{"form":form_instance})
    
    def post(self,request,*args, **kwargs):
        
        id=kwargs.get("pk")
        
        cat_object=Category.objects.get(id=id)
        
        form_instance=CategoryForm(request.POST,instance=cat_object,user=request.user)
        
        if form_instance.is_valid():
            
            form_instance.save()
            
            return redirect("category-add")
        
        else:
            return render(request,"category_edit.html",{"form":form_instance})
   
@method_decorator(signin_required,name="dispatch")     
class CategoryDeleteView(View):
    
    def get(self,request,*args, **kwargs):
        
        id=kwargs.get("pk")
        
        Category.objects.get(id=id).delete()
        
        return redirect("category-add")
        

@method_decorator(signin_required,name="dispatch") 
class TransactionCreateView(View):
    
    def get(self,request,*args, **kwargs):
        
        form_instance=TransactionsForm()
        
        cur_month=timezone.now().month
        
        cur_year=timezone.now().year
        
        categories=Category.objects.filter(owner=request.user)
        
        qs=Transactions.objects.filter(created_date__month=cur_month,created_date__year=cur_year,owner=request.user)
        
        return render(request,'transaction_add.html',{"form":form_instance,"transactions":qs,"categories":categories})
    
    def post(self,request,*args, **kwargs):
        
        form_instance=TransactionsForm(request.POST)
        
        if form_instance.is_valid():
            
            form_instance.instance.owner=request.user
            
            form_instance.save()
            
            return redirect("transaction-add")
        
        else:
            
            return render(request,'transaction_add.html',{"form":form_instance})
        
 
@method_decorator(signin_required,name="dispatch")        
class TransactionUpdateView(View):
    
    def get(self,request,*args, **kwargs):
        
        id=kwargs.get("pk")
        
        trans_obj=Transactions.objects.get(id=id)
        
        form_instance=TransactionsForm(instance=trans_obj)
        
        return render(request,"transaction_edit.html",{"form":form_instance})
    
    def post(self,request,*args, **kwargs):
        
        id=kwargs.get("pk")
        
        trans_obj=Transactions.objects.get(id=id)
        
        form_instance=TransactionsForm(request.POST,instance=trans_obj)
        
        if form_instance.is_valid():
            
            form_instance.save()
            
            return redirect("transaction-add")
        
        else:
            
            return render(request,"transaction_edit.html",{"form":form_instance})
 
@method_decorator(signin_required,name="dispatch")        
class TransactionDeleteView(View):
    
    def get(self,request,*args, **kwargs):
        
        id=kwargs.get("pk")
        
        Transactions.objects.get(id=id).delete()
        
        return redirect("transaction-add")
    

@method_decorator(signin_required,name="dispatch") 
class ExpenseSummaryView(View):
    
    def get(self,request,*args, **kwargs):
        
        cur_month=timezone.now().month
        
        cur_year=timezone.now().year
        
        qs=Transactions.objects.filter(created_date__month=cur_month,created_date__year=cur_year,owner=request.user)
        
        total_expense=qs.values("amount").aggregate(total=Sum("amount"))
        
        category_summary=qs.values("category_object__name").annotate(total=Sum("amount"))
        
        payment_summary=qs.values("payment_method").annotate(total=Sum("amount"))
        
        data={
            "total_expense":total_expense.get("total"),
            "category_summary":category_summary,
            "payment_summary":payment_summary,
        }
        
        return render(request,"expense_summary.html",data)

@method_decorator(signin_required,name="dispatch")  
class TransactionSummaryView(View):
    
    def get(self,request,*args, **kwargs):
        
        form_instance=TransactionFilterForm()
        
        cur_month=timezone.now().month
        
        cur_year=timezone.now().year
        
        if "start_date" in request.GET and "end_date" in request.GET:
            
            start_date=request.GET.get("start_date")
            
            end_date=request.GET.get("end_date")
            
            qs=Transactions.objects.filter(created_date__range=(start_date,end_date))
            
            total_expense=qs.values("amount").aggregate(total=Sum("amount"))
            
        else:
            
            qs=Transactions.objects.filter(created_date__month=cur_month,created_date__year=cur_year)
            
            total_expense=qs.values("amount").aggregate(total=Sum("amount"))
                
        return render(request,'transaction_summary.html',{"transactions":qs,"form":form_instance,"total_expense":total_expense})


class ChartView(View):
    
    def get(self,request,*args, **kwargs):
        
        return render(request,"chart.html")
    
class SignupView(View):
    
    def get(self,request,*args, **kwargs):
        
        form_instance=RegistrationForm()
        
        return render(request,'register.html',{"form":form_instance})
    
    def post(self,request,*args, **kwargs):
        
        form_instance=RegistrationForm(request.POST)
        
        if form_instance.is_valid():
            
            form_instance.save()
            
            messages.success(request,"account created successfully")
            
            print("account created successfully")
            
            return redirect("sign-up")
            
        else:
            
            print("failed to create account")
            
            messages.error(request,"failed to create account")
            
            return render(request,'register.html',{"form":form_instance})
        
class SignUpView(View):
    
    def get(self,request,*args, **kwargs):
        
        form_instance=SignUpForm()
        
        return render(request,'signup.html',{'form':form_instance})
    
    def post(self,request,*args, **kwargs):
        
        form_instance=SignUpForm(request.POST)
        
        if form_instance.is_valid():
            
            data=form_instance.cleaned_data
            
            user_obj=authenticate(request,**data)
            
            if user_obj:
                
                login(request,user_obj)
                
                messages.success(request,"signin successfull")
                
                return redirect("summary")
        messages.error(request,"signin unsuccessfull")
            
        return render(request,'signup.html',{'form':form_instance})

@method_decorator(signin_required,name="dispatch")   
class SignOutView(View):
    
    def get(self,request,*args, **kwargs):
        
        logout(request)
        
        return redirect("sign-up")
            
        
        
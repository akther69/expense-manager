from django.shortcuts import render

# Create your views here.
from api.serializers import UserSerializer,CategorySerializer,TransactionSerializer

from rest_framework import generics

from myapp.models import User,Category,Transactions

from rest_framework.response import Response

from rest_framework import authentication,permissions

from api.permissions import OwnerOnly

from rest_framework.views import APIView

from rest_framework import viewsets

from django.db.models import Sum

from django.utils import timezone

class UserCreationView(generics.CreateAPIView):
    
    serializer_class=UserSerializer
    
    # password not be hassed
    
    # def post(self,request,*args, **kwargs):
        
    #     serializer_instance=UserSerializer(data=request.data)
        
    #     if serializer_instance.is_valid():
            
    #         data=serializer_instance.validated_data
            
    #         User.objects.create_user(**data)
            
    #         return Response(data=serializer_instance.data)
        
    #     return Response(data=serializer_instance.errors)
    
    
class CategoryListCreateView(generics.ListCreateAPIView):
    
    serializer_class=CategorySerializer
    
    queryset=Category.objects.all()
    
    # authentication_classes=[authentication.BasicAuthentication]
    
    authentication_classes=[authentication.TokenAuthentication]
    
    permission_classes=[permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        
        return serializer.save(owner=self.request.user)
    
    # def list(self,request,*args, **kwargs):
        
    #     qs=Category.objects.filter(owner=request.user)
        
    #     serializer_instance=CategorySerializer(qs,many=True)
        
    #     return Response(data=serializer_instance.data)
    
    def get_queryset(self):
        return Category.objects.filter(owner=self.request.user)
    
class CategoryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    
    serializer_class=CategorySerializer
    
    queryset=Category.objects.all()
    
    # authentication_classes=[authentication.BasicAuthentication]
    
    authentication_classes=[authentication.TokenAuthentication]
    
    permission_classes=[OwnerOnly]
    
    
class CategoryApiView(APIView):
    
    # authentication_classes=[authentication.BasicAuthentication]
    
    authentication_classes=[authentication.TokenAuthentication]
    
    permission_classes=[permissions.IsAuthenticated]
    
    def get(self,request,*args, **kwargs):
        
        qs=Category.objects.filter(owner=request.user)
        
        category_list=qs.values_list("name",flat=True)
        
        return Response(data=category_list)
    
    
class TransactionCreateView(generics.CreateAPIView):
    
    authentication_classes=[authentication.TokenAuthentication]
    
    permission_classes=[permissions.IsAuthenticated]
    
    serializer_class=TransactionSerializer
    
    queryset=Transactions.objects.all()
    
    def perform_create(self, serializer):
        
        id=self.kwargs.get("pk")
        
        category_obj=Category.objects.get(id=id)
        
        serializer.save(owner=self.request.user,category_object=category_obj)
        
        
class TransactionRetrieveUpdateDestroyView(viewsets.ViewSet):
    
    authentication_classes=[authentication.TokenAuthentication]
    
    permission_classes=[permissions.IsAuthenticated]
    
    def destroy(self,request,*args, **kwargs):
        
        id=kwargs.get("pk")
        
        Transactions.objects.get(id=id).delete()
        
        data={"message":"deleted"}
        
        return Response(data)
    
    def update(self,request,*args, **kwargs):
        
        id=kwargs.get("pk")
        
        trans_obj=Transactions.objects.get(id=id)
        
        serializer_instance=TransactionSerializer(data=request.data,instance=trans_obj)
        
        if serializer_instance.is_valid():
            
            serializer_instance.save()
            
            return Response(data=serializer_instance.data)
        
        return Response(data=serializer_instance.errors)
    
    def retrieve(self,request,*args, **kwargs):
        
        id=kwargs.get("pk")
        
        qs=Transactions.objects.get(id=id)
        
        serializer_instance=TransactionSerializer(qs)
        
        return Response(data=serializer_instance.data)
    
    
class TransactionSummaryApiView(APIView):
    
    # authentication_classes=[authentication.BasicAuthentication]
    
    authentication_classes=[authentication.TokenAuthentication]
    
    permission_classes=[permissions.IsAuthenticated]
    
    def get(self,request,*args, **kwargs):
        
        qs=Transactions.objects.filter(owner=request.user)
        
        category_summary=qs.values("category_object__name").annotate(total=Sum("amount"))
        
        payment_summary=qs.values("payment_method").annotate(total=Sum("amount"))
        
        total_expense=qs.values("amount").aggregate(total_amount=Sum("amount"))
        
        context={
            "category_summary":category_summary,
            "payment_summary":payment_summary,
            "total_expense":total_expense
        }
        
        return Response(data=context)
    
    
class TransactionListView(APIView):
    
    authentication_classes=[authentication.TokenAuthentication]
    
    permission_classes=[permissions.IsAuthenticated]
    
    def get(self,request,*args, **kwargs):
        
        cur_month=timezone.now().month
        
        cur_year=timezone.now().year
        
        qs=Transactions.objects.filter(created_date__month=cur_month,created_date__year=cur_year,owner=self.request.user)
        
        if "name" in self.request.query_params:
            
            name_value=self.request.query_params.get("name")
            
            qs=qs.filter(category_object__name=name_value)
            
        if "payment_method" in self.request.query_params:
                
            payment_method_value = self.request.query_params.get("payment_method")
            
            qs = qs.filter(payment_method=payment_method_value)
            
        serializer_instance=TransactionSerializer(qs,many=True)
            
        return Response(data=serializer_instance.data)
    
            
            
    
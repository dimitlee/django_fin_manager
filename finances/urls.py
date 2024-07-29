from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserCategoryListView.as_view(), name='index'),
    path('category/add/<int:pk>/', views.add_category, name='add-category'),
    path('category/user/', views.CategoryToAddListView.as_view(), name='my-categories'),
    path('category/<int:pk>/', views.UserCategoryDetailView.as_view(), name='category-detail'),
    path('category/create/', views.create_category, name='create-category'),
    path('transaction/create/', views.create_transaction, name='create-transaction'),
    path('transaction/delete/<int:pk>/', views.delete_transaction, name='delete-transaction'),
    path('scheduledtransaction/create/', views.create_scheduled_transaction, name='create-scheduled-transaction')
]

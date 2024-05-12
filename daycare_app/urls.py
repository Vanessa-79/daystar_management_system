from django.urls import path
from daycare_app import views
from django.contrib.auth import views as auth_views

urlpatterns = [
path('', views.Index, name='index'),
path('home/', views.home, name='home'),
path('base/', views.base, name='base'),
path('dashboard/', views.dashboard, name='dashboard'), 
path('login/',auth_views.LoginView.as_view(template_name ='login.html'), name = 'login'),
path('logout', views.logout_view, name='logout'),


 
 #babies
path('babie/', views.Babie, name='babie'),
path('baby_list/', views.baby_list, name='baby_list'), 
path('baby_departure/', views.baby_departure, name='baby_departure'),
path('add/', views.add_baby, name='add_baby'),
path('edit_baby/<int:baby_id>/', views.edit_baby, name='edit_baby'),
path('viewbaby/', views.view_baby, name='view_baby'),
path('babyupdate/', views.babyupdate, name='babyupdate'),
path('<int:id>', views.view_baby, name='view_baby'),
path('baby_signedoutlist/', views.baby_signedoutlist, name='baby_signedoutlist'),
path('delete_baby/<int:baby_id>/', views.delete_baby, name='delete_baby'), 
path("signinbaby/",views.signinbaby,name="signinbaby"),



#sitters
path('sitter/', views.Sitter, name='sitter'),
path('sitters_list/', views.sitters_list, name='sitters_list'),
path('add_sitter/', views.Sitter, name='add_sitter'),
path('<int:id>', views.sitter_view, name='sitter_view'),
path('sitter_edit/<int:id>', views.sitter_edit, name='sitter_edit'),
path('sitter_delete/<int:sitter_id>/', views.sitter_delete, name='sitter_delete'),
path('sitteronduty/', views.sitter_arrival_list, name='sitter_arrival_list'),
path('sitterarrival/', views.sitter_arrival, name='sitter_arrival'),


#payments
path('payment_baby/', views.payment_baby, name='payment_baby'), 
path('payment_list/', views.payment_list, name='payment_list'),
path('paymentsitter/', views.paymentsitter, name='paymentsitter'),
path('paymentsitter_list/', views.paymentsitter_list, name='paymentsitter_list'),



#dolls
path('doll_stock/', views.doll_stock, name='doll_stock'),
path('dolladd/', views.add_doll, name='add_doll'),
path('dollsale/<int:pk>/', views.dollsale, name='dollsale'),
path('delete_doll/<int:pk>/', views.doll_delete, name='delete_doll'),
path('add_newdoll/<int:pk>/',views.add_newdoll, name='add_newdoll'),
path('update_doll/<int:pk>/', views.update_doll, name='update_doll'),
path('doll_sell_list/', views.doll_sell_list, name='doll_sell_list'),
path('receipt/<int:pk>/', views.receipt, name='receipt'),


#procurement
path('procurement/', views.procurement, name='procurement'),
path('item_list/', views.item_list, name='item_list'),
path('issue_out/<int:pk>/', views.issued_out, name='issue_out'),
path('issue_in/<int:pk>/', views.issued_in, name='issue_in'),
]


 

from django.urls import path
from app import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from .forms import LoginForm,MyPasswordChangeForm,MyPasswordResetForm,MySetPasswordForm

urlpatterns = [
    path('search_query/', views.search_query, name='search_query'),
    path('orders/', views.orders, name='orders'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('',views.ProductView.as_view(),name="home"),  
    path('cart/', views.show_cart, name='showcart'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='app/password_reset.html',form_class=MyPasswordResetForm),name='password_reset'),
    path('password-reset/done',auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name = 'app/password_reset_complete.html'),name='password_reset_complete'),
    path('logout/',auth_views.LogoutView.as_view(next_page ='login'),name='logout'),
    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'), 
    path('fertilizer/<slug:data>',views.fertilizer,name='fertilizerdata'),
    path('fertilizer/', views.fertilizer, name='fertilizer'),
    path('insecticide/<slug:data>',views.insecticide,name='insecticidedata'),
    path('insecticide/', views.insecticide, name='insecticide'),
    path('pesticide/<slug:data>',views.pesticide,name='pesticidedata'),
    path('pesticide/', views.pesticide, name='pesticide'),
    path('manure/<slug:data>',views.manure,name='manuredata'),
    path('manure/', views.manure, name='manure'),
    path('add-to-cart',views.add_to_cart,name='add-to-cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('registration/',views.CustomerRegistrationView.as_view(),name="customerregistration"),
    path('accounts/login/',auth_views.LoginView.as_view(template_name='app/login.html',authentication_form=LoginForm),name='login'),
    path('passwordchange/',auth_views.PasswordChangeView.as_view(template_name='app/passwordchange.html',form_class=MyPasswordChangeForm,success_url='/passwordchangedone/'),name='passwordchange'),
    path('pluscart/',views.plus_cart),
    path('minuscart/',views.minus_cart),
    path('removecart/',views.remove_cart),
    path('paymentdone/',views.payment_done,name='paymentdone')


]+ static (settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)

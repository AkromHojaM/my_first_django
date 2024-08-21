from django.views.generic import TemplateView
from django.views import View
from main.models import Product, Category ,About_img,ShoppinCard,Product_img
from django.http import HttpResponse
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import render,redirect
import json
from django.http.response import JsonResponse
# Create your views here.
class HomeView(View):
    template_name = 'index.html'
    context = {}
    def get(self, request):
        about_items = Product.objects.all()
        about_img = Category.objects.all()
        menu_data = []
        about_data = []
        for menu in about_items:
            menu_img = Product_img.objects.filter(product=menu).first()
            menu.image=menu_img
            menu_data.append(menu)
        self.context.update({'menu_data':menu_data})

        for about in about_img:
            about_img = About_img.objects.filter(category=about).first()
            about.image=about_img
            about_data.append(about)
        self.context.update({'about_img':about_data})
        return render(request, self.template_name, self.context)


    def post(self, request):
        product_id = request.POST.get('product_id')
        if request.user is None:
            return redirect('/logins')
        user = request.user
        if not ShoppinCard.objects.filter(Q(user=user) & Q(product_id=product_id)).exists():
            shoping_card = ShoppinCard.objects.create(
                user=user,
                product_id=product_id)
            shoping_card.save()
            messages.info(request,message='Product Added Successfully')
            return redirect(f'/#product_{product_id}')
        messages.error(request,message='Product Not Found')
        return redirect(f'/#product_{product_id}')


class MenuView(View):
    template_name = 'menu.html'
    context = {}
    def get(self, request):
        products = Product.objects.all()
        menus = []
        for menu in products:
            menu_img = Product_img.objects.filter(product=menu).first()
            menu.image=menu_img
            menus.append(menu)
        self.context.update({'menu_items':products})
        return render(request, self.template_name,self.context)
    def post(self, request):
        product = request.POST.get('product_id')
        if request.user is None:
            return redirect('/logins')
        user = request.user
        if not ShoppinCard.objects.filter(Q(user=user)& Q(product_id=product)).exists():
            shopping_card = ShoppinCard.objects.create(user=user,product_id=product)
            shopping_card.save()
            return redirect(f'/#product_{product}')
        return redirect(f'/#product_{product}')



class AboutView(View):
    template_name = 'about.html'
    context = {}
    def get(self, request):
        return render(request, self.template_name,self.context)
    def post(self, request):
        return render(request, 'about.html')


class BlogView(View):
    template_name = 'blog.html'
    context = {}
    def get(self, request):
        return render(request, self.template_name,self.context)
    def post(self, request):
        return render(request, 'blog.html')


class GaleryView(View):
    template_name = 'gallery.html'
    context = {}
    def get(self, request):
        return render(request, self.template_name,self.context)
    def post(self, request):
       return render(request, 'gallery.html')


class ReservationView(View):
    template_name = 'reservation.html'
    context = {}
    def get(self, request):
        return render(request, self.template_name,self.context)
    def post(self, request):
        return render(request, 'reservation.html')

class ContactView(View):
    template_name = 'contact.html'
    context = {}
    def get(self, request):
        return render(request, self.template_name,self.context)
    def post(self,request):
        return render(request, 'contact.html')



class ShoppingCardView(View):
    template_name = 'card.html'
    context = {}
    def get(self, request):
        if request.user.id is None:
            return redirect('/logins')
        shopping_card = ShoppinCard.objects.filter(user=request.user)
        data = []
        summa = 0
        for index,value in enumerate(shopping_card):
            image = Product_img.objects.filter(product=value.product).first()
            value.img = image
            value.index = index+1
            summa += float(value.product.price * value.count)
            summa = round(summa,2)
            total = summa + 50
            data.append(value)
        self.context.update({'shopping_card_products':data})
        self.context.update({'summa':summa})
        return render(request, self.template_name,self.context)
    def post(self, request):
        shopping_card_id = request.POST.get('shopping_card_id')
        ShoppinCard.objects.get(pk=shopping_card_id).delete()
        return redirect('/cart')
from django.shortcuts import get_object_or_404


class BaseCountAPIView(View):
    def get_shopping_card(self,shopping_card_id):
        return get_object_or_404(ShoppinCard, pk=shopping_card_id)

class IncrementCountAPIView(BaseCountAPIView):
    def post(self,request):
        try:
            json_data = json.loads(request.body.decode('utf-8'))
            shopping_card_id = json_data.get('id')
            shopping_card = ShoppinCard.objects.get(pk=shopping_card_id)
            shopping_card.count += 1
            shopping_card.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success':False , 'error':(e)})


class DecrementCountAPIView(BaseCountAPIView):
    def post(self,request):
        try:
            json_data = json.loads(request.body.decode('utf-8'))
            shopping_card_id = json_data.get('id')
            shopping_card = ShoppinCard.objects.get(pk=shopping_card_id)
            if shopping_card.count > 0:
                shopping_card.count -= 1
                shopping_card.save()
                return JsonResponse({'success':True})
        except Exception as e:
            return JsonResponse({'success':False , 'error':(e)})



class ChangeCountAPIView(BaseCountAPIView):
    def post(self,request):
        try:
            json_data = json.loads(request.body.decode('utf-8'))
            shopping_card_id = json_data.get('id')
            product_count = json_data.get('product_count')
            shopping_card = ShoppinCard.objects.get(pk=shopping_card_id)
            if product_count is not None:
                shopping_card.count = product_count
                shopping_card.save()
                return JsonResponse({'success':True})
        except Exception as e:
            return JsonResponse({'success':False , 'error':(e)})

class AddProductView(View):
    template_name = 'add_product.html'
    context = {}
    def get(self, request):
        return render(request, self.template_name,self.context)
    def post(self, request):
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('desc')
        images = request.FILES.getlist('images')

        product  = Product.objects.create(name=name,
                                          price=price,
                                          description=description,
                                          username = request.user)

        product.save()

        for image in images:
            img = Product_img.objects.create(image=image,
                                             product=product,
                                             )
            img.save()
        return redirect('/add-product')
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from store.models import CartItem, Collection, Order, OrderItem, Product, Customer, Cart
from django.db import transaction
from django.db.models import Q, F, Value, Func
from django.db.models.functions import Concat
from django.db.models.aggregates import Count, Max, Min, Avg, Sum
from django.contrib.contenttypes.models import ContentType
from tags.models import TaggedItem, TaggedItemManager


def say_hello(request):
    # only a query statement in a lazy mode
    #queryset = Product.objects.all()

    # product = Product.objects.get(pk=1) #returns an object, execute the query
    # productexist = Product.objects.filter(pk=0).exist() #return bolean

    # use Field lookups
    # filtered_products = Product.objects.filter(unit_price__gt=20) #unit_price__range=(20, 30)
    #filtered_products = Product.objects.filter(title__icontains='coffee')
    #filtered_products = Product.objects.filter(last_updet__year=2021)
    #filtered_products = Product.objects.filter(description__isnull=True)

    # excersise 1
    # filtered_customers = Customer.objects.filter(email__iendswith='.com')

    # excersise 2
    # collections = Collection.objects.filter(featured_product__isnull=True)

    # excersise 3
    # products = Product.objects.filter(inventory__lt=10)

    # excersise 4
    # orders = Order.objects.filter(customer_id=1)

    # excersise 5
    # ordered_items = OrderItem.objects.filter(product__collection__id=3)

    # multiple condition with AND
    # queryset = Product.objects.filter(inventory__lt=10, unit_price__lt=20)

    # multiple condition with Q object, o use OR
    # queryset = Product.objects.filter(
    #     Q(inventory__lt=10) | Q(unit_price__lt=20)
    # )
    # using F objects (fields)
    # queryset = Product.objects.filter(inventory=F('collection__id'))

    # examples of sorting data
    # queryset = Product.objects.order_by("unit_price", '-title').reverse()
    # product = Product.objects.order_by('unit_price')[0] # return an object the query was executed

    # excersise
    # queryset = Product.objects.filter(
    #     id__in=OrderItem.objects.values('product_id').distinct()).order_by('title')

    # only
    # defer

    # related objects to get in the same query related tables
    # use select_related (1)
    # use prefetch (n)
    # queryset = Product.objects.select_related('collection').all()
    # queryset = Product.objects.prefetch_related('promotions').all()

    # get the last 5 orders, with their customer and items
    # orders = Order.objects.select_related('customer').prefetch_related('orderitem_set__product').order_by('-placed_at')[:5]

    # using aggregates
    # 1
    # result = Product.objects.filter(collection__id=1).aggregate(count=Count('id'), min_price=Min('unit_price'))
    # result = Order.objects.aggregate(orders=Count('id'))
    # 2
    # result = OrderItem.objects.filter(product__id=1).aggregate(quantity_of_pr1=Sum('quantity'))
    # 3
    # result = Order.objects.filter(customer__id=1).aggregate(quantity=Count('id'))
    # 4
    # result = Product.objects.filter(collection__id=3).aggregate(max_price=Max('unit_price'), min_price=Min('unit_price'), average_price=Avg('unit_price'))

    # annotating generate new fields
    # queryset = Customer.objects.annotate(new_id=F('id') + 1)

    # func
    # queryset = Customer.objects.annotate(
    #     full_name=Func(F('first_name'), Value(' '),
    #                    F('last_name'), function='CONCAT'))
    # another approach instead a Func
    # queryset = Customer.objects.annotate(
    #     full_name=Concat('first_name', Value(' '),
    #                    'last_name'))
    # grouping data
    # queryset = Customer.objects.annotate(
    #     orders_count=Count('order')
    # )

    # annotated exercise
    # 1
    # queryset = Customer.objects.annotate(last_order_id=Max('order__id'))
    # 2
    # queryset = Collection.objects.annotate(products=Count('product'))
    # 3
    # queryset = Customer.objects.annotate(orders=Count('order')).filter(orders__gt=5)
    # 5
    # queryset = Customer.objects.annotate(
    # total_spent=Sum(
    #     F('order__orderitem__unit_price') *
    #     F('order__orderitem__quantity')))
    # 6
    # queryset = Product.objects \
    #     .annotate(
    #         total_sales=Sum(
    #             F('orderitem__unit_price') *
    #             F('orderitem__quantity'))) \
    #     .order_by('-total_sales')[:5]

    # generic relationships custom managers
    # queryset = TaggedItem.objects.get_tags_for(Product, 1)

    # Creating custom object (insert sql to add new entries)
    # collection = Collection()
    # collection.title = 'Video Games'
    # collection.featured_product = Product(pk=1)
    # collection.save()
    # avoid create() because didnt update model names

    # Update values (objects)
    # first query to load in memory
    # method 1 could have performance problems
    # collection = Collection.objects.get(pk=11)
    # collection.featured_product = None
    # collection.save()
    # method 2 to avoid extra read
    # Collection.objects.filter(pk=11).update(featured_product=None)

    # delete objects
    # single
    # collection = Collection(pk=11)
    # collection.delete()
    # multiple
    # Collection.objects.filter(id__gt=5).delete()

    # excersise 1 create
    # cart = Cart()
    # cart.save()

    # item1 = CartItem()
    # item1.cart = cart
    # item1.product_id = 1
    # item1.quantity = 1
    # item1.save()

    # excersice 2 update
    # item = CartItem.objects.get(pk=1)
    # item.quantity = 2
    # item.save()

    # excersice 3 delete
    cart = Cart(pk=1)
    cart.delete()

    return render(request, 'hello.html', {'name': 'Mosh'})


# @transaction.atomic() # to wrap all execution in the transaction
def do_transactions(request):
    # other operations
    # ...

    with transaction.atomic():
        order = Order()
        order.customer_id = 1
        order.save()

        item = OrderItem()
        item.order = order
        item.product_id = 1
        item.quantity = 1
        item.unit_price = 10
        item.save()

    return render(request, 'hello.html', {'name': 'Mosh'})

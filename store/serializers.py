from rest_framework import serializers
from decimal import Decimal

from store.models import Product, Collection


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']

    products_count = serializers.IntegerField(read_only=True)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        # fields = '__all__' # brings all fields
        fields = ['id', 'title', 'slug', 'description', 'inventory',
                  'unit_price', 'price_with_tax', 'collection']
    # id = serializers.IntegerField()
    # title = serializers.CharField()
    # price = serializers.DecimalField(
    #     max_digits=6, decimal_places=2, source='unit_price')
    price_with_tax = serializers.SerializerMethodField(
        method_name='calculate_tax')

    # collection = serializers.PrimaryKeyRelatedField(
    #     queryset=Collection.objects.all()) # only get id number
    # collection = serializers.StringRelatedField() # select related in view module
    # collection = CollectionSerializer()

    # for hyperlink
    # collection = serializers.HyperlinkedRelatedField(
    #     queryset=Collection.objects.all(),
    #     view_name='collection-detail'
    # )

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)
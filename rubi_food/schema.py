from graphene import AbstractType,Field,Node,String,Int,ClientIDMutation
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django import DjangoConnectionField
from graphene_django.types import DjangoObjectType
from .models import *
# creating an object that can be accessed from the graphql endpoint
#the node classes are equivalent to the serializers in REST framework
class categoryNode(DjangoObjectType):
    class Meta:
        model=Category
        interfaces=(Node,)
        # can do read_only fields, exclude_fields,and so on
        filter_fields={'category_name':['icontains']}

class FoodNode(DjangoObjectType):
    class Meta:
        model=Food
        interfaces = (Node,)
        # a query can be made and filtered using this field
        filter_fields = {'food_name':['icontains']}

class OrderNode(DjangoObjectType):
    class Meta:
        model=Order
        interfaces=(Node,)

class CartNode(DjangoObjectType):
    class Meta:
        model=Cart
        interfaces=(Node,)
#-----------------------QUERIES------------------------retrieve data from db via api

class FoodQuery(AbstractType):
    # abstract so that they can be inherited in the root schema
    single_food=Node.Field(FoodNode)
    food=DjangoFilterConnectionField(FoodNode)
    all_foods=DjangoConnectionField(FoodNode)

class OrderQuery(AbstractType):
    single_order=Node.Field(OrderNode)# used when querying for a
    #  specific item using an ID
    all_orders=DjangoConnectionField(OrderNode)# used when you are retrieving all items
    # without using filters

class CategoryQuery(AbstractType):
    single_category=Node.Field(categoryNode)# used when querying for a
    #  specific item using an ID
    categories=DjangoFilterConnectionField(categoryNode)# used when retrieving some items with filters
    all_categories=DjangoFilterConnectionField(categoryNode)

class CartQuery(AbstractType):
    single_cart=Node.Field(CartNode)
    all_carts=DjangoConnectionField(CartNode)

#--------------------MUTATIONS------------ To add data to the db via the api
# the only records being added are cart and order records
class NewCart(ClientIDMutation):
    Cart_node = Field(CartNode) # the node that will be holding the data

    class Input: # appears as suggestions in the graphiQl interface in the input set
        Cart_no = String()


    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        temp = Cart( # model name
            cart_No=input.get('Cart_no'),# from the input set, derive the
            #value assigned to cart_no and assign to cart_No
            # ( actual naming in the model)

        )
        temp.save()
        return NewCart(Pnode=temp) #return an object of type NewCart which is a node

class NewOrder(ClientIDMutation):
    order_node = Field(OrderNode)

    class Input:
        name = String()
        client_description=String()
        email=String()
        product=String()

    @classmethod
    def mutate_and_get_payload(cls, input, context, info):
        temp = Order(
            ORD_No=input.get('no'),
            food_id=input.get('id'),
            ordered_by=input.get('client'),
            quantiy=input.get('qty'),
            destination_addr=input.get('addr'),

        )
        temp.save()
        return NewOrder(Pnode=temp)


class CartMutation(AbstractType):
    new_client = NewCart.Field()

class OrderMutation(AbstractType):
    new_product = NewOrder.Field()
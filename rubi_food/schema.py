from graphene import ObjectType, Field, Node, String, ClientIDMutation
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType
from .models import *


# creating an object that can be accessed from the graphql endpoint
# the node classes are equivalent to the serializers in REST framework
class CategoryNode(DjangoObjectType):
    class Meta:
        model = Category
        interfaces = (Node,)
        # can do read_only fields, exclude_fields,and so on
        filter_fields = {'category_name': ['icontains']}


class FoodNode(DjangoObjectType):
    class Meta:
        model = Food
        interfaces = (Node,)
        # a query can be made and filtered using this field
        filter_fields = {'food_name': ['icontains']}


class OrderNode(DjangoObjectType):
    class Meta:
        model = Order
        interfaces = (Node,)


class CartNode(DjangoObjectType):
    class Meta:
        model = Cart
        interfaces = (Node,)


class ProfileNode(DjangoObjectType):
    class Meta:
        model = Customer
        interfaces = (Node,)
        # a query can be made and filtered using this field
        filter_fields = {'email': ['exact'], 'reg_no': ['exact']}


class AccountNode(DjangoObjectType):
    class Meta:
        model = Accounts
        interfaces = (Node,)
        # can do read_only fields, exclude_fields,and so on
        filter_fields = {
            'cart_number': ['exact'],
            'user': ['exact'],
            'account_number': ['icontains', 'exact']}


# -----------------------QUERIES------------------------retrieve data from db via api

class FoodQuery(ObjectType):
    # abstract so that they can be inherited in the root schema
    single_food = Node.Field(FoodNode)
    food = DjangoFilterConnectionField(FoodNode)
    all_foods = DjangoFilterConnectionField(FoodNode)


class OrderQuery(ObjectType):
    single_order = Node.Field(OrderNode)  # used when querying for a
    #  specific item using an ID
    all_orders = DjangoFilterConnectionField(OrderNode)  # used when you are retrieving all items
    # without using filters


class CategoryQuery(ObjectType):
    single_category = Node.Field(CategoryNode)  # used when querying for a
    #  specific item using an ID
    categories = DjangoFilterConnectionField(CategoryNode)  # used when retrieving some items with filters
    all_categories = DjangoFilterConnectionField(CategoryNode)


class CartQuery(ObjectType):
    single_cart = Node.Field(CartNode)
    all_carts = DjangoFilterConnectionField(CartNode)


class ProfileQuery(ObjectType):
    single_customer = Node.Field(ProfileNode)  # used when querying for a
    #  specific item using an ID
    customer_node = DjangoFilterConnectionField(ProfileNode)
    # used when you are retrieving all items without using filters
    all_customers = DjangoFilterConnectionField(ProfileNode)


class AccountQuery(ObjectType):
    # abstract so that they can be inherited in the root schema
    single_account = Node.Field(AccountNode)
    account_node = DjangoFilterConnectionField(AccountNode)
    all_accounts = DjangoFilterConnectionField(AccountNode)


# --------------------MUTATIONS------------ To add data to the db via the api
# the only records being added are cart and order records
class NewCart(ClientIDMutation):
    Cart_node = Field(CartNode)  # the node that will be holding the data

    class Input:  # appears as suggestions in the graphiQl interface in the input set
        Cart_no = String()

    # noinspection PyUnusedLocal
    @classmethod
    def mutate_and_get_payload(cls, context, info, **entries):
        temp = Cart(  # model name
            cart_No=entries.get('Cart_no'),  # from the input set, derive the
            # value assigned to cart_no and assign to cart_No
            # ( actual naming in the model)

        )
        temp.save()
        return NewCart(Pnode=temp)  # return an object of type NewCart which is a node


class NewOrder(ClientIDMutation):
    order_node = Field(OrderNode)

    class Input:
        name = String()
        client_description = String()
        email = String()
        product = String()

    # noinspection PyUnusedLocal,PyShadowingBuiltins
    @classmethod
    def mutate_and_get_payload(cls, context, info, **entries):
        temp = Order(
            ORD_No=entries.get('no'),
            food_id=entries.get('id'),
            ordered_by=entries.get('client'),
            quantiy=entries.get('qty'),
            destination_addr=entries.get('addr'),

        )
        temp.save()
        return NewOrder(Pnode=temp)


class NewCustomer(ClientIDMutation):
    customer_node = Field(ProfileNode)

    class Input:  # appears as suggestions in the graphiQl interface in the input set
        last_name = String()
        first_name = String()
        email = String()
        location = String()
        mobile_contact = String()
        profile_picture = String()
        description = String()

    # noinspection PyUnusedLocal
    @classmethod
    def mutate_and_get_payload(cls, context, info, **entries):
        user_ = entries.get('first_name').lower() + "_" + entries.get('last_name').lower()
        users = User.objects.all().filter(username=user_)
        if users:
            user_ = user_ + '_0'
        temp = Customer(
            last_name=entries.get('last_name'),
            first_name=entries.get('first_name'),
            email=entries.get('email'),
            username=User.objects.create(id=str(User.objects.count() + 1), username=user_),
            location=entries.get('location'),
            reg_no=(Customer.get_total_number_of_customers() + 1),
            mobile_contact=entries.get('mobile_contact'),
            profile_pic=entries.get('profile_picture'),
            description=entries.get('description'),
        )
        temp.save()
        return NewCustomer(customer_node=temp)  # return an object of type NewCart which is a node


class NewAccount(ClientIDMutation):
    account_node = Field(AccountNode)

    class Input:
        account_number = String()
        email = String()
        cart_no = String()

    # noinspection PyUnusedLocal
    @classmethod
    def mutate_and_get_payload(cls, context, info, **entries):
        account = Accounts(
            user=Customer.objects.get(email=entries.get('email')),
            sacco_string=Cart.objects.get(cart_No=entries.get('cart_no')),
            account_number=entries.get('sacco_string')
        )
        account.save()
        return NewAccount(account_node=account)


class CartMutation(ObjectType):
    new_client = NewCart.Field()


class OrderMutation(ObjectType):
    new_product = NewOrder.Field()


class CustomerMutation(ObjectType):
    new_customer = NewCustomer.Field()


class AccountMutation(ObjectType):
    new_account = NewAccount.Field()

from graphene import ObjectType, Field, Node, String, ClientIDMutation
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType
from .models import *
import os


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
        filter_fields = []


class CartNode(DjangoObjectType):
    class Meta:
        model = Cart
        interfaces = (Node,)
        filter_fields = []


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


def decode_image(data, name):
    """
    Function to decode byte string to image
    Base64 module function b64decode will decode the byte string into bytes
    and these bytes will then be written into a file whose name is the user's name
    :param data: Byte string of the image
    :param name: Name of user to be used as file name
    :return: Image file name of the user
    """
    # get encoded version of the byte string
    img_data = data.encode('UTF-8', 'strict')
    import base64
    directory = os.getcwd() + '/media/profile_pictures/'
    if not os.path.isdir(directory):
        os.makedirs(directory)
    # create file name
    pic_name = directory + name.replace(' ', '_') + ".jpg"
    # decode image string and write into file
    with open(pic_name, 'wb') as fh:
        fh.write(base64.b64decode(img_data))
    # return file name without directory path
    pics = pic_name.split('/')
    return pics[-3] + '/' + pics[-2] + '/' + pics[-1]


def compress_image(filename):
    """
    Function to resize(compress) image to a given size
    :param filename: Image to resize
    :return: None
    """
    from PIL import Image  # library for compressing images
    # open file to be compressed
    img = Image.open(filename)
    # compress the image accordingly
    foo = img.resize((200, 200), Image.ANTIALIAS)
    # save the downsized image
    foo.save(filename, optimize=True, quality=100)


def upload_photo(name, picture, url=""):
    filename = decode_image(picture, name)
    try:
        compress_image(filename)
    except Exception as err:
        print("Something went wrong: {}".format(err))
    if url.endswith('/'):
        return "".join([url, filename])
    else:
        return "/".join([url, filename])


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
        url = String()

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
            profile_picture=upload_photo(entries.get('first_name') + " " + entries.get('last_name'),
                                         entries.get('profile_picture'), entries.get('url')),
            description=entries.get('description'),
        )
        temp.save()
        return NewCustomer(customer_node=temp)  # return an object of type NewCart which is a node


class UpdateCustomerPicture(ClientIDMutation):
    customer_node = Field(ProfileNode)

    class Input:
        email = String()
        profile_picture = String()
        url = String()

    # noinspection PyUnusedLocal
    @classmethod
    def mutate_and_get_payload(cls, context, info, **entries):
        user = Customer.objects.get(email=entries.get('email'))
        user.profile_picture = upload_photo(user.first_name + " " + user.last_name,
                                            entries.get('profile_picture'), entries.get('url'))
        user.save()
        return UpdateCustomerPicture(customer_node=user)


class DeleteCustomer(ClientIDMutation):
    customer_node = Field(ProfileNode)

    class Input:
        email = String()

    # noinspection PyUnusedLocal
    @classmethod
    def mutate_and_get_payload(cls, context, info, **entries):
        user = Customer.objects.get(email=entries.get('email'))
        username = user.username
        users = User.objects.all().filter(username=username)
        if users:
            for user_ in users:
                user_.delete()
        user.delete()
        return DeleteCustomer(customer_node=user)


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
    new_cart = NewCart.Field()


class OrderMutation(ObjectType):
    new_order = NewOrder.Field()


class CustomerMutation(ObjectType):
    new_customer = NewCustomer.Field()


class AccountMutation(ObjectType):
    new_account = NewAccount.Field()


class DeleteCustomerMutation(ObjectType):
    delete_customer = DeleteCustomer.Field()


class UpdateCustomerPictureMutation(ObjectType):
    update_customer_picture = UpdateCustomerPicture.Field()

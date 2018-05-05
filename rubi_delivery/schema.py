# ROOT SCHEMA
import os
import json
from rubi_food.schema import *


# root query----inherit all the queries in the application and bundle them into one major query congolomerate
class RootQuery(FoodQuery, OrderQuery, CartQuery, CategoryQuery, ProfileQuery, AccountQuery, graphene.ObjectType):
    pass


# same purpose as root query
class RootMutation(CartMutation, OrderMutation, CustomerMutation, AccountMutation, DeleteCustomerMutation,
                   UpdateCustomerPictureMutation, graphene.ObjectType):
    pass


# root schema defines the query and mutation which is the roots defined above
schema = graphene.Schema(query=RootQuery, mutation=RootMutation)

# get dictionary defining the schema
introspection_dict = schema.introspect()

# Save the schema into some file
with open(os.getcwd() + '/schema.json', 'w') as fp:
    json.dump(introspection_dict, fp)

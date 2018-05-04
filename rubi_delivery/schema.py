# ROOT SCHEMA
import graphene
import os
import json
from rubi_food.schema import *


# root query----inherit all the queries in the application and bundle them into one major query congolomerate
class RootQuery(FoodQuery, OrderQuery, CartQuery, CategoryQuery, graphene.ObjectType, ProfileQuery, AccountQuery, ):
    pass


# same purpose as root query
class RootMutation(CartMutation, OrderMutation, graphene.ObjectType, CustomerMutation, AccountMutation, ):
    pass


# root schema defines the query and mutation which is the roots defined above
schema = graphene.Schema(query=RootQuery, mutation=RootMutation)

# get dictionary defining the schema
introspection_dict = schema.introspect()

# Save the schema into some file
with open(os.getcwd() + '/schema.json', 'w') as fp:
    json.dump(introspection_dict, fp)

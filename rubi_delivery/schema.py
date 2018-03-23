#ROOT SCHEMA
import graphene
from rubi_food.schema import *
# root query----inherit all the queries in the application and bundle them into one major query
#congolomerate
class RootQuery(FoodQuery,OrderQuery,CartQuery,CategoryQuery,graphene.ObjectType):
    pass
# same purpose as root query
class RootMutation(CartMutation,OrderMutation,graphene.ObjectType):
    pass
# root schema defines the query and mutation which is the roots defined above
schema=graphene.Schema(query=RootQuery,mutation=RootMutation)
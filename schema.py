import graphene

import gql.schema


class Query(gql.schema.Query, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass


schema = graphene.Schema(
    query=Query,
    mutation=gql.schema.MyMutations
)

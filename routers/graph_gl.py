import strawberry
from strawberry.fastapi import GraphQLRouter


@strawberry.type
class Query:
    #  https://strawberry.rocks/docs/integrations/fastapi
    @strawberry.field
    async def hello(self) -> str:
        return "Hello World"

    @strawberry.field
    async def world(self, x: int) -> str:
        return f"world {x}"


schema = strawberry.Schema(Query)
graphql_app = GraphQLRouter(schema)

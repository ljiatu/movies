from ariadne import QueryType, make_executable_schema, ObjectType, load_schema_from_path
from graphql import GraphQLResolveInfo

type_defs = load_schema_from_path("../graphql/")

query = QueryType()
user = ObjectType("User")


@query.field("hello")
def resolve_hello(_, info: GraphQLResolveInfo):
    request = info.context["request"]
    user_agent = request.headers.get("user-agent", "guest")
    return f"Hello, {user_agent}"


@user.field("username")
def resolve_username(obj, _):
    return f"{obj.first_name} {obj.last_name}"


schema = make_executable_schema(type_defs, query, user)

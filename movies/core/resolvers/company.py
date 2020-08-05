from ariadne import ObjectType
from graphql import GraphQLResolveInfo

from movies.core.dataloaders.company_loader import CompanyLoader
from movies.core.entities.company import Company

companies = ObjectType("Companies")

URL_PATH = "company"


@companies.field("company")
async def resolve_company(_, info: GraphQLResolveInfo, id: int) -> Company:
    company_loader = CompanyLoader.for_context(info.context)
    company = await company_loader.load(id)
    return company

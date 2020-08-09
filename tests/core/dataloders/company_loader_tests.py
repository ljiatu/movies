from typing import Any, Dict, List

import pytest
from aresponses import ResponsesMockServer

from movies.core.dataloaders.company_loader import CompanyLoader, URL_PATH
from movies.core.entities.company import Company
from movies.settings import TMDB_API_HOST, TMDB_API_VERSION


@pytest.fixture
def context() -> Dict[str, Any]:
    return {}


@pytest.fixture
def json_companies() -> List[Dict[str, Any]]:
    return [
        {
            "id": 1,
            "description": "A good company",
            "name": "Any Financials Holdings Inc.",
            "parent_company": {"id": 2, "name": "Alibaba Inc."},
        },
        {"id": 2, "description": "A gooder company", "name": "Alibaba Inc."},
        {
            "id": 3,
            "description": "A bad company",
            "name": "Imaginary Bad Company Inc.",
        },
    ]


@pytest.fixture
def company_keys(json_companies: List[Dict[str, Any]]) -> List[int]:
    return list(map(lambda jc: jc["id"], json_companies))


@pytest.fixture
def query_paths(company_keys: List[int]) -> List[str]:
    return [f"/{TMDB_API_VERSION}/{URL_PATH}/{k}" for k in company_keys]


@pytest.mark.asyncio
async def test_batch_get_success(
    aresponses: ResponsesMockServer,
    context: Dict[str, Any],
    query_paths: List[str],
    json_companies: List[Dict[str, Any]],
    company_keys: List[int],
):
    for path, json_company in zip(query_paths, json_companies):
        aresponses.add(TMDB_API_HOST, path, "GET", response=json_company)

    company_loader = CompanyLoader.for_context(context)
    companies = await company_loader.load_many(company_keys)
    assert companies == [Company(**jc) for jc in json_companies]

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_batch_get_partial_failure(
    aresponses: ResponsesMockServer,
    context: Dict[str, Any],
    query_paths: List[str],
    json_companies: List[Dict[str, Any]],
    company_keys: List[int],
):
    # The request for company_id=2 will fail with a 500.
    aresponses.add(TMDB_API_HOST, query_paths[0], "GET", response=json_companies[0])
    aresponses.add(
        TMDB_API_HOST, query_paths[1], "GET", aresponses.Response(status=500)
    )
    aresponses.add(TMDB_API_HOST, query_paths[2], "GET", response=json_companies[2])

    company_loader = CompanyLoader.for_context(context)
    companies = await company_loader.load_many(company_keys)
    assert companies == [
        Company(**json_companies[0]),
        None,
        Company(**json_companies[2]),
    ]

    aresponses.assert_plan_strictly_followed()

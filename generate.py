from datetime import datetime
from typing import cast, TypedDict, Iterator
import json, sys, jinja2, os
import urllib.request as request

class Repository(TypedDict):
    name: str
    url: str
    description: str
    languages: list[str]

if os.path.exists(path := os.path.join(os.getcwd(), ".env")):
    with open(path, "r") as env:
        for key, value in map(lambda x: x.strip().split("="), env.readlines()):
            os.environ[key] = value

GRAPHQL_GITHUB_TOKEN = os.getenv("GRAPHQL_GITHUB_TOKEN")

QUERY = """
query {
    user(login: "lycuid") {
        pinnedItems(first: 100, types: REPOSITORY) {
            nodes {
                ... on Repository {
                    ... RepositoryData
                }
            }
        }
    }
}
fragment RepositoryData on Repository {
    name
    url
    description
    languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
        nodes {
            name
        }
    }
}
"""

def fetch_repositories() -> Iterator[Repository]:
    req         = request.Request("https://api.github.com/graphql")
    req.data    = json.dumps({"query": QUERY}).encode("utf-8")
    req.method  = "POST"
    req.headers = {
        "Authorization": f"Bearer {GRAPHQL_GITHUB_TOKEN}",
        "Content-Type": "application/json",
    }
    data = json.loads(request.urlopen(req).read())["data"]["user"]

    repositories = map(lambda repo: cast(Repository, repo),
        map(lambda repo: {
                **repo,
                "languages": list(map(lambda n: n["name"], repo["languages"]["nodes"])),
            },
            data["pinnedItems"]["nodes"]))
    return repositories

with open(sys.argv[1], "r") as html:
    template = jinja2.Template(html.read())
    print (template.render({"repositories": fetch_repositories() }), flush=True)
    print (f"[DEBUG({datetime.now()})]:\tTemplate successfully rendered -> '{sys.argv[1]}'", file=sys.stderr, flush=True)

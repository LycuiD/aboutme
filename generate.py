from datetime import datetime
from typing import cast, TypedDict, Iterator
import json, sys, jinja2, os
import urllib.request as request

class Repository(TypedDict):
    name: str
    url: str
    description: str
    languages: Iterator[str]

if os.path.exists(path := os.path.join(os.getcwd(), ".env")):
    with open(path, "r") as env:
        for key, value in map(lambda x: x.strip().split("="), env.readlines()):
            os.environ[key] = value

GRAPHQL_GITHUB_TOKEN = os.getenv("GRAPHQL_GITHUB_TOKEN")

GITHUB_USERNAME = "lycuid"

GRAPHQL_QUERY = """
query {
    user(login: "%s") {
        pinnedItems(first: 4, types: REPOSITORY) {
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
""" % (GITHUB_USERNAME)

def fetch_pinned_repositories() -> Iterator[Repository]:
    req         = request.Request("https://api.github.com/graphql")
    req.data    = json.dumps({"query": GRAPHQL_QUERY}).encode("utf-8")
    req.method  = "POST"
    req.headers = {
        "Authorization": f"Bearer {GRAPHQL_GITHUB_TOKEN}",
        "Content-Type": "application/json",
    }
    data = json.loads(request.urlopen(req).read())["data"]["user"]

    repositories = cast(Iterator[Repository],
        map(lambda repo: {
                **repo,
                "languages": map(lambda n: n["name"], repo["languages"]["nodes"]),
            }, data["pinnedItems"]["nodes"]))
    return repositories

with open(sys.argv[1], "r") as html:
    html = jinja2 \
            .Template(html.read()) \
            .render({ "repositories": fetch_pinned_repositories() })
    print ("".join(map(lambda line: line.strip(), html.split("\n"))), flush=True)
    print (f"[DEBUG({datetime.now()})]:\tTemplate successfully rendered -> '{sys.argv[1]}'", file=sys.stderr, flush=True)

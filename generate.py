#!/usr/bin/env python

import urllib.request as request
import os, json
from datetime import datetime

from typing import TypedDict, Optional, cast

class Repository(TypedDict):
    name: str
    url: str
    description: str
    languages: list[str]

def dbg(*args, **kwargs):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now}][DEBUG]", *args, **kwargs)

FILE = os.path.join("public", "index.html")
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

class RepoData(object):
    CACHE_FILE = "cache.json"
    def __init__(self):
        if not (repos := self.CachedData()):
            dbg("Making HTTP request.")
            data = json.dumps(self.RequestData())
            with open(self.CACHE_FILE, "w+") as cache:
                dbg("Writing to cache file.")
                cache.write(data)
                cache.flush()
            repos = self.CachedData() or []
        self.data = "".join(map(self.repo_template, repos))

    @staticmethod
    def repo_template(repo: Repository) -> str:
        return f"""
        <span style="display:flex;justify-content:space-between;">
            <span><u><i>{repo["name"]}</i></u>: <small>{repo["description"]}</small></span>
            <small style="width:150px;overflow:hidden;white-space:nowrap;text-overflow:ellipsis;">
            {", ".join(repo["languages"])}
            </small>
        </span>
        """

    # make http request to get repository data from github.
    def RequestData(self) -> list[Repository]:
        req         = request.Request("https://api.github.com/graphql")
        req.data    = json.dumps({"query": QUERY}).encode("utf-8")
        req.method  = "POST"
        req.headers = {
            "Authorization": f"Bearer {os.environ.get('GRAPHQL_GITHUB_TOKEN')}",
            "Content-Type": "application/json",
        }
        data = json.loads(request.urlopen(req).read())["data"]["user"]
        repositories = list(
            map(
                lambda repo: cast(Repository, repo),
                map(
                    lambda repo: {
                        **repo,
                        "languages": list(map(lambda n: n["name"], repo["languages"]["nodes"])),
                    },
                    data["pinnedItems"]["nodes"]
                )
            )
        )
        return repositories

    # return github repository data if already saved in the cache file.
    def CachedData(self) -> Optional[list[Repository]]:
        if os.path.exists(self.CACHE_FILE):
            dbg("template cache file found.")
            with open(self.CACHE_FILE, "r") as cache:
                dbg("reading from template cache file.")
                return json.loads(cache.read())
        dbg("template cache file not found.")

def A(link: str, text: Optional[str] = None) -> str:
    return f"""<a target="_blank" href="{link}">{text or link}</a>"""

def Section(title, children):
    return f"""
    <fieldset id={"-".join(title.lower().split())}>
        <legend><h3><u>{title}</u></h3></legend>
        {children}
    </fieldset>
    """

def Info(label: str, link: str, text: Optional[str] = None):
  return f"""<div>{label}: """+A(link, text)+"""</div>"""

if __name__ == "__main__":
    if not os.path.exists(os.path.dirname(FILE)):
        os.mkdir(os.path.dirname(FILE))
    repo = RepoData()
    with open(FILE, "w+") as file:
        html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <title>Abhishek Kadam</title>
      <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      <meta charset="UTF-8" />
      <link rel="icon" href="data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2020%2020%22%3E%3Ccircle%20cx%3D%2210%22%20cy%3D%2210%22%20r%3D%2210%22%20fill%3D%22white%22%20stroke%3D%22none%22%2F%3E%3Ctext%20fill%3D%22black%22%20x%3D%226%22%20y%3D%2215%22%3E%CE%BB%3C%2Ftext%3E%3C%2Fsvg%3E" />
        <style>
        :root {
            --color-primary: #393939;
            --color-secondary: #dedede;
        }
        html {
            background-color: white;
            color: var(--color-primary);
        }
        @media (min-width: 857px) {
            body {
                max-width: 65%;
                margin-left: auto;
                margin-right: auto;
            }
        }
        *, ::after, ::before {
            box-sizing: border-box;
            font-family: 'Arial';
        }
        ul { margin: .5em 0; }
        hr { background-color: white; }
        fieldset { border-color: white; }
        a {
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
        a:visited {
            color: blue;
        }
        .page {
            height:960px;
            overflow:hidden;
        }
        .padded {
            font-size: smaller;
            padding-left: 5em;
            width: 100%;
        }
        .bordered {
            margin: 10px 0;
            padding: 1em .5em;
            border: 1px solid var(--color-secondary);
        }
        fieldset > legend {
            text-decoration: underline;
        }
        </style>
    </head>
    <body>
        <header class="page">
            <h2>Abhishek Kadam</h2>
            <section id="info" class="bordered">
                """+Info("email", "mailto:abhishekk19@gmail.com", "abhishekk19@gmail.com")+"""
                """+Info("github", "https://github.com/lycuid")+"""
                """+Info("linkedin", "https://linkedin.com/in/abhishek-kadam-26a06170")+"""
                """+Info("personal", "https://lycuid.github.io")+"""
            </section>
            <br />

            <i><strong><u>Worthy&nbsp;Mention:</u>&nbsp;</strong>
            Cleared the hiring '<u>foobar</u>' challenge (2018) by
            &nbsp;
            <strong>
                <span style="color: #427FE8;">G</span><span style="color: #EB2041;">O</span><span style="color: #FBC145;">O</span><span style="color: #427FE8;">G</span><span style="color: #00BE61;">L</span><span style="color: #EB2041;">E</span>
            </strong>
            ,&nbsp;
            twice (2021), unfortunately, never led to any interview opportunity.
            </i>
            <br />
            <section id="software-interests-experience">
                <h3><u>Software Interests/Experience</u></h3>
                <ul>
                    <li>System software and writing general purpose tools (GNU/linux).</li>
                    <li>Web development (Full stack).</li>
                    <li>Compilers and programming language design/paradigm.</li>
                    <li>Programming puzzles, competitive programming.</li>
                </ul>
            </section>

            """+Section("Few Hobby Projects", """
                """+repo.data+"""
                <br />
                <small>All the projects (including the above) can be found on github.</small>
            """)+"""

            """+Section("Technologies I use", """
                <div><u>Regularly</u>: C, Golang, Haskell, Python, Typescript, Javascript.</div>
                <div><u>Frequently</u>: Rust, Guile Scheme, C++</div>
                <div><u>Occasionally</u>: Erlang, Common lisp, Racket Scheme.</div>
            """)+"""

            <fieldset id="education">
                <legend><h3><u>Education</u></h3></legend>
                <div><u>School</u>: <small>Grade: A (score: 85%)</small></div>
                <div>S.T.E.S's Sinhagad Public School (2010)</div>
                <div><u>Higher Secondary School</u>: <small>(class 11<sup>th</sup>, 12<sup>th</sup>) Grade: A (score: 72%)</small></div>
                <div>S.T.E.S's Sinhagad Public School (Computer Science, Mathematics) (2012)</div>
                <div><u>College</u>: <code>Grade: --</code> <small>(Dropped out 2<sup>nd</sup> year).</small></div>
                <div>S.I.E.S Graduate School of Technology (Engineering - Computer Science)
            </fieldset>
        </header>
        <main class="page">
        """+Section("Employment", """
            <section>
                <strong><u>Care24 (Aegis Care Advisors Pvt. Ltd.)</u></strong>&nbsp;|&nbsp;
                Sep 17 - Oct 19 (~2 years)<br />
                <br />
                <u>Full-Stack Web Developer</u> <small>(~1.5 months)</small>
                <br />
                <u><small>[TEAM]</SMALL></U>
                <ul>
                    <li>Maintaining the legacy code</li>
                    <li>refactoring, testing etc (python, js).</li>
                    <li>Creating REST APIs</li>
                </ul>
                <u><small>[INDEPENDENT]</small></u>
                <ul>
                    <li><span>Business Metric visualization tool (<u><i>used by operation and marketing team</i></u>).</span></li>
                    <li><span>A <i>Simple</i> general purpose tabular report generation tool (<u><i><b>the most used</b></u> app by every team</i>).</span></li>
                    <li><span>Web interface that automated about 40% work, while adding a better structure (<u><i>used by finance team</i></u>).</span></li>
                </ul>
                <div class="padded">
                    <u>Front-end</u>: <span>Reactjs | AngularJs | JQuery | Javascript.</span><br />
                    <u>Back-end</u>: <span>Django 1.8 | Python 2 | Django REST Framework.</span><br />
                    <u>Other</u>: <span>Postgresql.</span><br />
                </div>
                <br />
                <u>Senior Software Engineer</u> (2 years)
                <br />
                <u><small>[TEAM]</small></u>
                <ul>
                    <li>A Grading system which led to automating comsumer bookings (python, reactjs).</li>
                    <li>Managing two small teams (project management, code reviews).</li>
                    <li>Mentoring developers and interns.</li>
                </ul>
                <u><small>[INDEPENDENT]</small></u>
                <ul>
                    <li><span>Optimizing primary VPS leading to monthly cost reduction upto <strong><i><u>60%</u></i></strong> (AWS).</span></li>
                    <li>Complete devops and backend dev for 2 indepedently launched apps (AWS, python).</li>
                    <li>Deployment pipeline revamp for primary app (AWS, Bitbucket).</li>
                    <li>Email, SMS, IVR Automation (python, js, third party integrations).</li>
                    <li>Brand Payment gateway (python, third party integration).</li>
                    <li>Verification and Background check Tool (\\w third party integration).</li>
                    <li>In-house email management tool (GSuite, Gmail API).</li>
                    <li>Automating tickets using the in-house email management tool.</li>
                </ul>
                <div class="padded">
                    <u>Front-end</u>: <span>Reactjs | Typescript | AngularJs | Angular 8.</span><br />
                    <u>Back-end</u>: <span>Django 1.8/2.2 | Python 2/3 | Django REST Framework.</span><br />
                    <u>Other</u>: <span>AWS | Apollo2/GraphQL | Redis | RabbitMQ | Postgresql.</span><br />
                </div>
            </section>
            <hr />

            <section>
                <strong><u>Freelancer / Self employed (while in college).</u></strong>&nbsp;|&nbsp;
                Mar 12 - Sep 17 (&gt; 5 years)<br /><br />
                <u>Script Writer and Web/Desktop App Developer</u>
                <ul>
                    <li>Landing pages for events by various local communities.</li>
                    <li>Website with voting mechanism for various festivals (local).</li>
                    <li>Desktop GUI application for some local businesses.</li>
                    <li>Landing page with Custom CMS dashboard from ground up, for a brand new startup (https://k3technologies.co.in).</li>
                </ul>
                <div class="padded">
                    <u>Languages used</u>: <span>PHP | Javascript | JQuery | Python 2 | Tcl/Tk (Tkinter with python).</span>
                </div>
            </section>
        """)+"""
        </main>
    </body>
    </html>
        """
        file.write("".join(map(lambda s: s.strip(), html.strip().split("\n"))))
        file.flush()
        dbg("Done!.")

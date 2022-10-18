#!/usr/bin/env python

import urllib.request as request
import os, json
from datetime import datetime

def DEBUG(*args, **kwargs):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now}][DEBUG]", *args, **kwargs)

FILE = os.path.join("public", "index.html")
QUERY = """
query {
    user(login: "lycuid") {
        pinnedItems(first: 100, types: REPOSITORY) {
            nodes {
                ... on Repository {
                    name
                    url
                    description
                    languages(first: 1, orderBy: { field: SIZE, direction: DESC }) {
                        nodes {
                            name
                        }
                    }
                }
            }
        }
    }
}
"""

class RepoData(object):
    CACHE_FILE = "cache.json"
    def __init__(self):
        repos = self.CachedData()
        if not repos:
            DEBUG("Making HTTP request.")
            with open(self.CACHE_FILE, "w+") as cache:
                DEBUG("Writing to cache file.")
                cache.write(json.dumps(self.RequestData()))
                cache.flush()
            repos = self.CachedData()
        self.data = "".join(map(self.repo_template, repos or []))

    def dump(self):
        return self.data

    @staticmethod
    def repo_template(repo):
        return f"""
        <fieldset>
            <legend>{repo["name"]}</legend>
            <div class="main">
                {repo["description"]}<br /><br />
            </div>
            <div class="footer">
                <small>
                    <a target="_blank" href="{repo["url"]}">{repo["url"]}</a>
                </small>
                <code>Written&nbsp;in:&nbsp;{repo["language"]}</code>
            </div>
        </fieldset>
        """

    def RequestData(self):
        req         = request.Request("https://api.github.com/graphql")
        req.data    = json.dumps({"query": QUERY}).encode("utf-8")
        req.method  = "POST"
        req.headers = {
            "Authorization": f"Bearer {os.environ.get('GRAPHQL_GITHUB_TOKEN')}",
            "Content-Type": "application/json",
        }
        repos = json.loads(request.urlopen(req).read())["data"]["user"]["pinnedItems"]["nodes"]
        repos = map(lambda repo: {**repo, "language": repo["languages"]["nodes"][0]["name"]}, repos)
        return list(repos)


    def CachedData(self):
        if os.path.exists(self.CACHE_FILE):
            DEBUG("template cache file found.")
            with open(self.CACHE_FILE, "r") as cache:
                DEBUG("reading from template cache file.")
                return json.loads(cache.read())
        DEBUG("template cache file not found.")

def Section(title, children):
    return f"""
    <section id={"-".join(title.lower().split())}>
        <h3><u>{title}</u></h3>
        {children}
    </section>
    """

def Info(label, link, text):
  return f"""<div>{label}: <a target="_blank" href="{link}">{text}</a></div>"""

if __name__ == "__main__":
    if not os.path.exists(os.path.dirname(FILE)):
        os.mkdir(os.path.dirname(FILE))
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
            --color-secondary: #131313;
        }
        *, ::after, ::before {
            box-sizing: border-box;
        }
        a {
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
        a:visited {
            color: blue;
        }
        html {
            background-color: white;
            color: var(--color-primary);
        }
        .padded {
            padding-left: 5em;
            margin-top: .5em;
            margin-bottom: .5em;
            width: 100%;
        }
        .bordered {
            margin: 10px 0;
            padding: 25px 15px;
            border: 1px solid var(--color-primary);
        }
        fieldset > legend {
            text-decoration: underline;
        }
        #hobby-projects .project-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            grid-gap: 15px;
        }
        #hobby-projects .project-container fieldset {
            display: grid;
            grid-template-rows: 1fr auto;
        }
        #hobby-projects .project-container fieldset .main {
            font-style: italic;
        }
        #hobby-projects .project-container fieldset .footer {
            display: flex;
            flex-direction: column;
        }
        </style>
    </head>
    <body>
        <header><h2>Abhishek Kadam</h2></header>
        <main>

        <section id="info" class="bordered">
            """+Info("email", "mailto:abhishekk19@gmail.com", "abhishekk19@gmail.com")+"""
            """+Info("github", "https://github.com/lycuid", "https://github.com/lycuid")+"""
            """+Info("linkedin", "https://linkedin.com/in/abhishek-kadam-26a06170", "https://linkedin.com/in/abhishek-kadam-26a06170")+"""
            """+Info("personal", "https://lycuid.github.io", "https://lycuid.github.io")+"""
        </section>

        <i><strong><u>Worthy&nbsp;Mention:</u>&nbsp;</strong>Being approached by&nbsp;
            <strong>
                <span style="color: #427FE8;">G</span><span style="color: #EB2041;">O</span><span style="color: #FBC145;">O</span><span style="color: #427FE8;">G</span><span style="color: #00BE61;">L</span><span style="color: #EB2041;">E</span>
            </strong>
            &nbsp;for an opportunity to interview (2018), twice (2021), based on my compettive programming performance/history (Never actually led to an official interview though).</i>

        """+Section("Summary", """
            <ul>
                <li>Software Engineer, opinionated polyglot developer and a minimalist (of sorts).</li>
                <li>Enthusiastic and comfortable with daily driving *nix system.</li>
                <li>Writing software as a hobby (mostly tools for linux), for day-to-day use.</li>
                <li>
                    <div>Software Interests:
                    <ul>
                        <li>General purpose tools, parsing tools.</li>
                        <li>Experimenting with different (paradigms/design) programming languages.</li>
                        <li>System Programming, solving puzzles.</li>
                        <li><span>Building <i>new</i> things.</span></li>
                    </ul>
                    </div>
                </li>
                <li>Dropped out of college 2nd year, Computer Science (B. Tech).</li>
            </ul>
        """)+"""
        <hr />

        """+Section("Hobby Projects", '<div class="project-container">'+RepoData().dump()+'</div>')+"""

        """+Section("Technologies I use", """
            <div><u>Regularly</u>: C, Golang, Haskell, Rust, Python, Typescript, Javascript.</div>
            <div><u>Frequently</u>: C++, Guile Scheme</div>
            <div><u>Occasionally</u>: Erlang, Common lisp, Racket Scheme.</div>
        """)+"""

        """+Section("Employment", """
            <fieldset>
                <legend>Care24 (Aegis Care Advisors Pvt. Ltd.)</legend>
                <small>Sep 17 - Oct 19 (~2 years)</small><br />
                <br />
                <strong>Full-Stack Web Developer</strong> (~1.5 months)
                <br />
                <u>Team projects</u>
                <ul>
                    <li>Maintaining the legacy code</li>
                    <li>refactoring, testing etc (python, js).</li>
                    <li>Creating REST APIs</li>
                </ul>
                <u>Individual Projects</u>
                <ul>
                    <li><span>Business Metric visualization tool (<u><i>used by operation and marketing team</i></u>).</span></li>
                    <li><span>A <i>Simple</i> general purpose tabular report generation tool (<u><i>the <b>most used</b> app by <b>every single</b> team</i></u>).</span></li>
                    <li><span>Web interface that automated about 40% work, while adding a better structure (<u><i>used by finance team</i></u>).</span></li>
                </ul>
                <div class="padded">
                    <u>Front-end Tech</u>:<br />
                    Reactjs | AngularJs | JQuery | vanilla javascript.<br />
                    <u>Back-end Tech</u>:<br />
                    Django 1.8 | Python 2 | Django REST Framework<br />
                    <u>Other</u>:<br />
                    Postgresql<br />
                </div>
                <br />
                <strong>Senior Full-Stack Engineer</strong> (2 years)
                <br />
                <u>Team Projects</u>
                <ul>
                    <li>A Grading system which led to automating comsumer bookings (python, reactjs).</li>
                    <li><span>Optimizing primary VPS leading to monthly cost reduction upto <strong><i><u>60%</u></i></strong> (AWS).</span></li>
                </ul>
                <u>Individual Projects</u>
                <ul>
                    <li>Complete devops and backend dev for 2 indepedently launched apps (AWS, python, shell).</li>
                    <li>Deployment pipeline revamp for primary app (shell, AWS, Bitbucket).</li>
                    <li>Email, SMS, IVR Automation (python, js, third party integrations).</li>
                    <li>New Payment gateway Integration (python).</li>
                    <li>Verification and Background check Tool (\\w third party integration).</li>
                    <li>In-house email management tool (GSuite, Gmail API).</li>
                    <li>Automating tickets using the in-house email management tool.</li>
                </ul>
                <div class="padded">
                    <u>Front-end Tech</u>:<br />
                    Reactjs | Typescript | AngularJs | Angular 8<br />
                    <u>Back-end Tech</u>:<br />
                    Django 1.8/2.2 | Python 2/3 | Shell | Django REST Framework<br />
                    <u>Other</u>:<br />
                    AWS | Apollo2/GraphQL | Redis | RabbitMQ | Postgresql<br />
                </div>
            </fieldset>
            <br />

            <fieldset>
                <legend>Freelancer / Self employed (while in college).</legend>
                <small>Mar 12 - Sep 17 (&gt; 5 years)</small><br />
                <strong>Script Writer and Web/Desktop App Developer</strong>
                <div class="padded">
                    <u>Languages used</u>:<br />
                    PHP | Python 2/3 | C
                </div>
            </fieldset>
        """)+"""
        <br />
        </main>

        <footer>
            <section id="education">
                <h3><u>Education Summary</u></h3>
                <div><u>School</u>: <code>Grade: A (score: 85%)</code></div>
                <div>S.T.E.S's Sinhagad Public School (2010)</div>
                <div><u>Higher Secondary School</u>: (class 11<sup>th</sup>, 12<sup>th</sup>) <code>Grade: A (score: 72%)</code></div>
                <div>S.T.E.S's Sinhagad Public School (Computer Science, Mathematics) (2012)</div>
                <div><u>College</u>: <code>Grade: --</code></div>
                <div>S.I.E.S Graduate School of Technology (Engineering - Computer Science) (Dropped out 2<sup>nd</sup> year).</div>
            </section>
        </footer>
    </body>
    </html>
        """
        file.write("".join(map(lambda s: s.strip(), html.strip().split("\n"))))
        file.flush()

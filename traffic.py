import json
import os
from urllib import request


def record_custom_event(event):
    headers = {
        "X-Insert-Key": os.getenv("NEW_RELIC_INSERT_KEY"),
    }
    req = request.Request(
        "https://insights-collector.newrelic.com/v1/accounts/%s/events"
        % os.getenv("NEW_RELIC_ACCOUNT_ID"),
        headers=headers,
        data=json.dumps(event).encode("utf-8"),
    )
    resp = request.urlopen(req)
    print(resp.read())


def api_req(request_url):
    req = request.Request(
        request_url, headers={"Authorization": "token %s" % os.getenv("GITHUB_TOKEN")}
    )
    response = request.urlopen(req)
    return json.load(response)


def lambda_handler(event, context):
    base_url = "https://api.github.com"
    user = os.getenv("GITHUB_USERNAME")
    print("Getting repositories for %s" % user)
    req = api_req("%s/users/%s/repos" % (base_url, user))

    ur = [(r["name"]) for r in req]
    print("Found %s repositories" % len(ur))

    print(" ")

    for repo_name in ur:

        print("Getting referral data for %s" % repo_name)
        referrals = api_req(
            "%s/repos/%s/%s/traffic/popular/referrers" % (base_url, user, repo_name)
        )
        if len(referrals) > 0:
            for ref in referrals:
                referred = {
                    "eventType": "Referral",
                    "repo_name": repo_name,
                    "referrer": ref["referrer"],
                    "count": ref["count"],
                    "uniques": ref["uniques"],
                }
                print(referred)
                record_custom_event(referred)

        print("Getting top referral path data for %s" % repo_name)

        paths = api_req(
            "%s/repos/%s/%s/traffic/popular/paths" % (base_url, user, repo_name)
        )
        if len(paths) > 0:
            for ref in paths:
                paths = {
                    "eventType": "ReferralPath",
                    "repo_name": repo_name,
                    "path": ref["path"],
                    "title": ref["title"],
                    "count": ref["count"],
                    "uniques": ref["uniques"],
                }
                print(paths)
                record_custom_event(paths)

        print("Getting views for %s" % repo_name)
        req = api_req("%s/repos/%s/%s/traffic/views" % (base_url, user, repo_name))
        if req["count"] > 0 or req["uniques"] > 0:
            viewed = {
                "eventType": "View",
                "repo_name": repo_name,
                "count": req["count"],
                "uniques": req["uniques"],
            }
            print(viewed)
            record_custom_event(viewed)

        print("Getting clones for %s" % repo_name)
        req = api_req("%s/repos/%s/%s/traffic/clones" % (base_url, user, repo_name))
        if req["count"] > 0 or req["uniques"] > 0:
            cloned = {
                "eventType": "Clone",
                "repo_name": repo_name,
                "count": req["count"],
                "uniques": req["uniques"],
            }
            record_custom_event(cloned)
        print(" ")

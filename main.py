import os
import requests
from dotenv import load_dotenv, dotenv_values
from requests_oauthlib import OAuth2Session


def write_token(access_token: str):
    with open(".token", "w") as file:
        file.write(access_token)


headers = {"Authorization": "Bearer {}".format(os.getenv("ACCESS_TOKEN"))}

query = """
{
    reportData {
        reports(guildID: 478831) {
            data {
                startTime
                endTime
                code
                title
            }
        }
    }
}
"""


def run_query(query):
    request = requests.post(
        "https://classic.warcraftlogs.com/api/v2/client",
        json={"query": query},
        headers=headers,
    )
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Request error {}.".format(request.status_code))


def main():
    load_dotenv()

    if os.getenv("ACCESS_TOKEN") is None:
        client_id = os.environ["CLIENT_ID"]
        client_secret = os.environ["CLIENT_SECRET"]
        auth_base_url = "https://www.warcraftlogs.com/oauth/authorize"
        token_url = "https://www.warcraftlogs.com/oauth/token"

        oauth = OAuth2Session(client_id)
        auth_url = oauth.authorization_url(auth_base_url)
        print("Auth at: {}".format(auth_url))

        redirect_response = input("Paste redirect URL:")

        token = oauth.fetch_token(
            token_url,
            client_secret=client_secret,
            authorization_response=redirect_response,
        )

        # Append into env file
        with open(".env", "a") as env_file:
            env_file.write("ACCESS_TOKEN={}\n".format(token["access_token"]))
        load_dotenv()

    response = run_query(query)

    print(response)


if __name__ == "__main__":
    main()
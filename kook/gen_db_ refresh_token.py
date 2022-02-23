import os
from dotenv import load_dotenv
import dropbox
from dropbox import DropboxOAuth2FlowNoRedirect
from lib import get_project_kook

def main():
    """
    Populate your app key in order to run this locally
    """
    APP_KEY = os.getenv("APP_KEY")
    auth_flow = DropboxOAuth2FlowNoRedirect(
        APP_KEY, use_pkce=True, token_access_type="offline"
    )

    authorize_url = auth_flow.start()
    print("1. Go to: " + authorize_url)
    print('2. Click "Allow" (you might have to log in first).')
    print("3. Copy the authorization code.")
    auth_code = input("Enter the authorization code here: ").strip()

    try:
        oauth_result = auth_flow.finish(auth_code)
        refresh_token = oauth_result.refresh_token
        print(f"Refresh Token = {refresh_token}")

        proj_kook_dir = get_project_kook()
        with open(f"{proj_kook_dir}/.env", "r") as f:
            env_file = f.read()
        env_file = "\n".join(
            list(
                map(
                    lambda x: f"REFRESH_TOKEN={refresh_token}"
                    if x.startswith("REFRESH_TOKEN")
                    else x,
                    env_file.split("\n"),
                )
            )
        )
        with open(f"{proj_kook_dir}/.env", "w") as f:
            f.write(env_file)
        

    except Exception as e:
        print("Error: %s" % (e,))
        exit(1)

    with dropbox.Dropbox(
        oauth2_refresh_token=oauth_result.refresh_token, app_key=APP_KEY
    ) as dbx:
        dbx.users_get_current_account()
        print("Successfully set up client!")


if __name__ == "__main__":
    load_dotenv()
    main()

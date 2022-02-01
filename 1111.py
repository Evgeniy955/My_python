import boto3
import requests

ENV = 'STAGE'

ADMIN_REST_URL = {'DEV': 'https://d-alfa-mb-1.zysbox.dev',
                  'STAGE': 'https://s-alfa-mb-1.zysbox.dev',
                  'QA': 'https://q-alfa-mb-1.zysbox.dev'
                  }.get(ENV)

# ADMIN_USERNAME = 'akim.tonkonozhenko+qa@zytara.com'
# ADMIN_USERNAME = 'nikita.diakov+qa@zytara.com'

# ADMIN_PASSWORD = '9KT73tWbM?'
# ADMIN_PASSWORD = '`MFrnp,j4d'
ADMIN_USERNAME = 'nikita.diakov+1@zytara.com'

ADMIN_PASSWORD = 'BRJ9SLhkyrD_10'

COGNITO_POOL = {
    'DEV': 'us-east-1_syKqUhcap',
    'STAGE': 'us-east-1_W5x0I1sPb',
    'QA': 'us-east-1_SSeTT2NdE'
}.get(ENV)

COGNITO_CLIENT = {
    'DEV': '40a7kenn23o8ed3k3dtnj0tk7e',
    'STAGE': '2g7gva7gv25b9vdv4nehs5d9ic',
    'QA': '5rprab571n7kegrsnclbg6529'
}.get(ENV)

ADMIN_COGNITO_CLIENT = {
    'DEV': '6c7j6348tao87t8nnl0qpdcqjo',
    'STAGE': '2eppdas6hea0tkhgi5nsmd9mqi',
    'QA': '6fl26k1gmddm1ignutluggfmft'
}.get(ENV)

ADMIN_COGNITO_POOL = {
    'DEV': 'us-east-1_hIE6BXcdn',
    'STAGE': 'us-east-1_S3XQGZU6m',
    'QA': 'us-east-1_T9BIYI8vm'
}.get(ENV)


class CognitoUtil:

    def __init__(self, is_admin=False):
        self.is_admin = is_admin
        self.pool_id = COGNITO_POOL
        self.app_client_id = COGNITO_CLIENT
        self.admin_pool_id = ADMIN_COGNITO_POOL
        self.admin_client_id = ADMIN_COGNITO_CLIENT
        self.region = "us-east-1"
        self.client = boto3.client('cognito-idp', region_name=self.region,
                                   endpoint_url='https://d59meaoe6qmph.cloudfront.net'
                                   if ENV == 'QA' and not self.is_admin else None)

    def get_token(self, username: str, password: str, is_access_token=False, is_admin=False):
        res = self.client.initiate_auth(
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={'USERNAME': username.replace('@', '#'), 'PASSWORD': password},
            ClientId=self.admin_client_id if is_admin else self.app_client_id,
        )
        tokens = res.get('AuthenticationResult')
        return tokens.get('AccessToken') if is_access_token else f"{tokens.get('TokenType')} {tokens.get('IdToken')}"


def get_users_id(json_data):
    id_list = []
    for user_data in json_data.get('content'):
        user_id = user_data.get('userId')
        if user_id:
            id_list.append(user_id)
    return id_list


def get_cookies_and_xsrf_token(token) -> tuple:
    res = requests.get(f'{ADMIN_REST_URL}/api/admin/users', params={'sort': 'EMAIL'}, headers={'Authorization': token})
    if res.status_code != 200:
        raise Exception(f'Request to getting deep link return: {res.content}, with status code: {res.status_code}')
    return res.cookies, res.cookies.get('XSRF-TOKEN')


def get_users(token, email, xsrf_token, cookies):
    res = requests.post(f'{ADMIN_REST_URL}/api/admin/waitlist?size=2000',
                        headers={'Authorization': token, 'X-XSRF-TOKEN': xsrf_token},
                        cookies=cookies, json={
            "email": email,
            "fromDate": "12-12-2020",
            "toDate": "12-21-2022"
        })
    if res.status_code != 200:
        raise Exception(f'Request to getting deep link return: {res.content}, with status code: {res.status_code}')
    return res.json()


def remove_users_from_wait_list(token, users_id):
    res = requests.delete(f'{ADMIN_REST_URL}/api/admin/waitlist', headers={'Authorization': token}, json=users_id)
    if res.status_code != 200:
        raise Exception(f'Request to getting deep link return: {res.content}, with status code: {res.status_code}')


def add_email_to_wait_list(token, email, xsrf_token, cookies):
    res = requests.post(f'{ADMIN_REST_URL}/api/admin/waitlist/upload',
                        headers={'Authorization': token, 'X-XSRF-TOKEN': xsrf_token},
                        cookies=cookies, json={"emails": [
            email
        ],
            "marketingProgramDto": {
                "expireDate": "12-12-2022",
                "startDate": "12-12-2020"
            }})
    if res.status_code != 200:
        raise Exception(f'Request to getting deep link return: {res.content}, with status code: {res.status_code}')
    return res


def get_deep_link(token, mail, cookies, xsrf_token):
    body = [{
        "email": mail,
    }]
    res = requests.post(f'{ADMIN_REST_URL}/api/admin/waitlist/generate',
                        headers={'Authorization': token, 'X-XSRF-TOKEN': xsrf_token},
                        cookies=cookies, json=body)
    if res.status_code != 200:
        raise Exception(f'Request to getting deep link return: {res.content}, with status code: {res.status_code}')
    deep_link = [i.get('deeplinkUrl') for i in res.json()][0]
    return deep_link


def complete_deep_link(email):
    token = CognitoUtil().get_token(username=ADMIN_USERNAME, password=ADMIN_PASSWORD, is_admin=True)
    cookies, xsrf_token = get_cookies_and_xsrf_token(token)
    add_email_to_wait_list(token=token, email=email, cookies=cookies, xsrf_token=xsrf_token)
    dp = get_deep_link(token=token, mail=email, cookies=cookies, xsrf_token=xsrf_token)
    return dp, email


def complete_cleanup(email):
    token = CognitoUtil().get_token(username=ADMIN_USERNAME, password=ADMIN_PASSWORD, is_admin=True)
    cookies, xsrf_token = get_cookies_and_xsrf_token(token)
    json_data = get_users(token, email, cookies=cookies, xsrf_token=xsrf_token)
    users_id = get_users_id(json_data)
    remove_users_from_wait_list(token, users_id)


def get_users_quantity_from_waitlist(email):
    token = CognitoUtil().get_token(username=ADMIN_USERNAME, password=ADMIN_PASSWORD, is_admin=True)
    cookies, xsrf_token = get_cookies_and_xsrf_token(token)
    json_data = get_users(token=token, email=email, cookies=cookies, xsrf_token=xsrf_token)
    users_id = get_users_id(json_data)
    return len(users_id)

if __name__ == '__main__':
    # for i in range(1000, 1021):
    #     mail = f'akim.tonkonozhenko+{i}@zytara.com'
    #     print(complete_deep_link(mail))
    l = [complete_deep_link(f'akim.tonkonozhenko+{i}@zytara.com') for i in range(1024, 1025)]
    print(l)


import json
import requests
import argparse
from validate_email import validate_email
import validators

COMMAND_PING = "ping"
COMMAND_SYS_VER = "system_version"
COMMAND_STORAGE_INFO = "storage_info"
COMMAND_CREATE_USER = "create_user"
COMMAND_DELETE_USER = "delete_user"
PARAM_BASE_URL = "base_url"
PARAM_API_KEY = "api_key"


def parse_args():
    parser = argparse.ArgumentParser(prog='articli', description='Arifactory CLI tool.')
    parser.add_argument('--version', action='version', version='%(prog)s 0.0.1')
    required_named = parser.add_argument_group('Required parameters')
    required_named.add_argument('-k', '--' + PARAM_API_KEY, required=True,
                                help='A key for artifactory API athentication.')
    required_named.add_argument('-l', '--' + PARAM_BASE_URL, required=True, help='A base URL to artifactory API.')
    command_group = parser.add_argument_group('Available commands')
    command_group.add_argument('--' + COMMAND_PING, action='store_true', help='Sends a ping request')
    command_group.add_argument('--' + COMMAND_SYS_VER, action='store_true',
                               help='Retrieve information about the current Artifactory version, revision, and currently installed Add-ons')
    command_group.add_argument('--' + COMMAND_STORAGE_INFO, action='store_true',
                               help='Returns storage summary information regarding binaries, file store and repositories.')
    command_group.add_argument('--' + COMMAND_CREATE_USER, nargs=3, metavar="",
                               help='Creates a new user in Artifactory or replaces an existing user. Expected: username, password and email')
    command_group.add_argument('--' + COMMAND_DELETE_USER, nargs=1, metavar="",
                               help='Removes an Artifactory user. Expected: username to delete')
    return parser.parse_args()

#TODO add additional validations
def validate_global_params(args):
    if not validators.url(args.get(PARAM_BASE_URL)):
        print("Base URL is not valid")
        exit(-1)
    if not args.get(PARAM_API_KEY).strip():
        print("API key should not be empty")
        exit(-1)


def create_auth_header(api_key):
    headers = {'Content-Type': 'application/json',
               'X-JFrog-Art-Api': '{0}'.format(api_key)}
    return headers


def invoke_command(args):
    if args.get(COMMAND_PING) == True:
        return exec_ping(args.get(PARAM_BASE_URL), args.get(PARAM_API_KEY))
    elif args.get(COMMAND_SYS_VER) == True:
        return exec_get_sys_version(args.get(PARAM_BASE_URL), args.get(PARAM_API_KEY))
    elif args.get(COMMAND_STORAGE_INFO) == True:
        return exec_get_storage_info(args.get(PARAM_BASE_URL), args.get(PARAM_API_KEY))
    elif args.get(COMMAND_CREATE_USER) is not None:
        return exec_create_user(args.get(PARAM_BASE_URL), args.get(PARAM_API_KEY), args.get(COMMAND_CREATE_USER))
    elif args.get(COMMAND_DELETE_USER) is not None:
        return exec_delete_user(args.get(PARAM_BASE_URL), args.get(PARAM_API_KEY), args.get(COMMAND_DELETE_USER))
    else:
        return "Command argument is needed. \nRun 'articli -h' for a list of available commands"


def exec_ping(base_url, api_key):
    url = f'{base_url}/api/system/ping'
    api_url = '{}'.format(url)
    auth_headers = create_auth_header(api_key)
    response = requests.get(api_url, headers=auth_headers)
    return handle_response(response)


def exec_get_sys_version(base_url, api_key):
    url = f'{base_url}/api/system/version'
    api_url = '{}'.format(url)
    auth_headers = create_auth_header(api_key)
    response = requests.get(api_url, headers=auth_headers)
    content = handle_response(response)
    return pretty_response(content)


def exec_get_storage_info(base_url, api_key):
    url = f'{base_url}/api/storageinfo'
    api_url = '{}'.format(url)
    auth_headers = create_auth_header(api_key)
    response = requests.get(api_url, headers=auth_headers)
    content = handle_response(response)
    return pretty_response(content)


def exec_create_user(base_url, api_key, user_data):
    url = f'{base_url}/api/security/users/{user_data[0]}'
    api_url = '{}'.format(url)
    auth_headers = create_auth_header(api_key)
    email = user_data[2]
    if not validate_email(email):
        print("Provided email is not valid")
        exit(-1)
    data = {'email': f'{user_data[2]}',
            'password': f'{user_data[1]}'}
    response = requests.put(api_url, data=json.dumps(data), headers=auth_headers)
    handle_response(response)
    return "OK"


def exec_delete_user(base_url, api_key, user_data):
    url = f'{base_url}/api/security/users/{user_data[0]}'
    api_url = '{}'.format(url)
    auth_headers = create_auth_header(api_key)
    response = requests.delete(api_url, headers=auth_headers)
    return handle_response(response)


def handle_response(response):
    if 200 <= response.status_code < 300:
        return response.content.decode('utf-8')
    else:
        print('[!] HTTP {0}  with content {1}'.format(response.status_code, pretty_response(response.content)))
        exit(-1)


def pretty_response(content):
    parsed = json.loads(content)
    return json.dumps(parsed, indent=4, sort_keys=True)


def main():
    try:
        args = vars(parse_args())
        validate_global_params(args)
        print(invoke_command(args))
    except Exception as e:
        print (e)


if __name__ == '__main__':
    main()

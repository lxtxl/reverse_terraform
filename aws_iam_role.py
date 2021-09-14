import sys
from iam_module.iam_role import IamRole
from config import Config
import json

profile_name = Config().get_profile_name()

def print_roles():
    iam_role = IamRole(profile_name)
    print(iam_role.list_roles())

def make_role(role_name):
    iam_role = IamRole(profile_name)
    iam_role.make_role(role_name)

def print_role(role_name):
    iam_role = IamRole(profile_name)
    print(json.dumps(iam_role.get_role(role_name), default=str, sort_keys=True, indent=4))

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print_roles()
    elif len(sys.argv) == 2:
        make_role(sys.argv[1])

import sys
from codecommit_module.codecommit import CodeCommit
from config import Config
import json

profile_name = Config().get_profile_name()

def print_repositories():
    codecommit = CodeCommit(profile_name)
    print(codecommit.list_repositories())

def make_repository(repository_name):
    codecommit = CodeCommit(profile_name)
    codecommit.make_repository(repository_name)

def print_repository(role_name):
    pass
    # codecommit = CodeCommit(profile_name)
    # print(json.dumps(codecommit.get_role(role_name), default=str, sort_keys=True, indent=4))

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print_repositories()
    elif len(sys.argv) == 2:
        make_repository(sys.argv[1])

import sys
# from codepipeline_module.codepipeline import CodePipeline
from kms_module.kms import Kms
from config import Config
import json

profile_name = Config().get_profile_name()

def print_kms_key_list():
    kms = Kms(profile_name)
    kms_list = kms.list_keys()
    for kms_data in kms_list:
        print(kms_data['key_id'], ":", kms_data['key_arn'])

def make_kms_key(key_id):
    kms = Kms(profile_name)
    kms.make_key(key_id)

def print_kms_key(key_id):
    kms = Kms(profile_name)
    print(json.dumps(kms.get_key(key_id), sort_keys=True, indent=4))

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print_kms_key_list()
    elif len(sys.argv) == 2:
        make_kms_key(sys.argv[1])

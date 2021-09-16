import sys
# from codepipeline_module.codepipeline import CodePipeline
from aws_kms_key import make_kms_key
from aws_kms_alias import make_kms_alias
from config import Config
import json

profile_name = Config().get_profile_name()

if __name__ == '__main__':
    if len(sys.argv) == 2:
        make_kms_key(sys.argv[1])
        make_kms_alias(sys.argv[1])


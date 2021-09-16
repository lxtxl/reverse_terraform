import boto3
from common_module.string_util import camelToSnake
from common_module.save_file import save_file
import sys

class CodeCommit:

    def __init__(self, profile_name):
        session = boto3.Session(profile_name=profile_name)
        self.client = session.client('codecommit')

    def list_repositories(self):
        objects = self.client.list_repositories()
        list = []
        for object in objects['repositories']:
            list.append(object['repositoryName'])
        return list

    def get_repository(self, repository_name):
        objects = self.client.get_repository(repositoryName=repository_name)
        object = objects['repositoryMetadata']
        return object

    def make_repository(self, repository_name):
        object = self.get_repository(repository_name)
        print(object)

        hcl_code_list = []
        hcl_code_list.append("resource \"aws_codecommit_repository\" \"{}\" {".format(repository_name))
        hcl_code_list.append("  repository_name = \"{}\"".format(repository_name))
        hcl_code_list.append("  description     = \"{}\"".format(object['repositoryDescription']))
        hcl_code_list.append("}")

        save_file(f"aws_codecommit_repository_{repository_name}.tf", "\n".join(hcl_code_list))
        return "\n".join(hcl_code_list)

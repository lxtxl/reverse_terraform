import boto3
from common_module.string_util import camelToSnake
from common_module.save_file import save_file
import sys

class IamRole:

    def __init__(self, profile_name):
        session = boto3.Session(profile_name=profile_name)
        self.client = session.client('iam')

    def list_roles(self):
        objects = self.client.list_roles()
        list = []
        for object in objects['Roles']:
            list.append(object['RoleName'])
        return list

    def get_role(self, role_name):
        objects = self.client.get_role(RoleName=role_name)
        object = objects['Role']
        print(object)
        return object

    def make_role(self, role_name):
        objects = self.client.get_role(RoleName=role_name)
        object = objects['Role']
        print(object)

        hcl_code_list = []
        hcl_code_list.append("resource \"aws_iam_role\" \"%s\" {" % (object['RoleName'],))
        hcl_code_list.append(f"  name = \"{object['RoleName']}\"")
        hcl_code_list.append(f"")
        hcl_code_list.append("  assume_role_policy = jsonencode(%s" % (object['AssumeRolePolicyDocument'],))
        hcl_code_list.append(f"  )")
        hcl_code_list.append(f"")
        if "Tags" in object:
            hcl_code_list.append("  tags = {")
            for tag in object['Tags']:
                hcl_code_list.append("    %s = \"%s\"" % (tag['Key'], tag['Value']))
            hcl_code_list.append("  }")
        hcl_code_list.append("}")

        save_file(f"aws_iam_role_{role_name}.tf", "\n".join(hcl_code_list))
        return "\n".join(hcl_code_list)

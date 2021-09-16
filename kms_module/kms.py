import boto3
from common_module.string_util import camelToSnake
from common_module.save_file import save_file
import sys

class Kms:

    def __init__(self, profile_name):
        session = boto3.Session(profile_name=profile_name)
        self.client = session.client('kms')

    def list_keys(self):
        objects = self.client.list_keys()
        list = []
        for object in objects['Keys']:
            save_object = {}
            save_object['key_id'] = object['KeyId']
            save_object['key_arn'] = object['KeyArn']
            list.append(save_object)
        return list

    def get_key(self, key_id):
        objects = self.client.describe_key(KeyId=key_id)
        object = objects['KeyMetadata']
        return object

    def get_alias(self, key_id):
        objects = self.client.list_aliases(KeyId=key_id)
        object_list = objects['Aliases']
        object = object_list[0]
        return object

    def get_alias_name(self, key_id):
        object = self.get_alias(key_id)
        name = object['AliasName'].replace("alias/", "")
        return name

    def make_key(self, key_id):
        object = self.get_key(key_id)

        aliase_name = self.get_alias_name(key_id)
        print(aliase_name)
        hcl_code_list = []

        hcl_code_list.append("data \"aws_iam_policy_document\" \"%s-doc\" {" % (aliase_name,))
        hcl_code_list.append("  statement {")
        hcl_code_list.append("    sid = \"Enable IAM User Permissions\"")
        hcl_code_list.append("")
        hcl_code_list.append("    actions = [")
        hcl_code_list.append("      \"kms:*\",")
        hcl_code_list.append("    ]")
        hcl_code_list.append("")
        hcl_code_list.append("    principals {")
        hcl_code_list.append("      type = \"AWS\"")
        hcl_code_list.append("      identifiers = [\"arn:aws:iam::${my_account}:root\"]")
        hcl_code_list.append("    }")
        hcl_code_list.append("    resources = [")
        hcl_code_list.append("      \"*\",")
        hcl_code_list.append("    ]")
        hcl_code_list.append("  }")
        hcl_code_list.append("")
        hcl_code_list.append("  statement {")
        hcl_code_list.append("    sid = \"Allow access for Key Administrators\"")
        hcl_code_list.append("")
        hcl_code_list.append("    actions = [")
        hcl_code_list.append("      \"kms:Create*\", ")
        hcl_code_list.append("      \"kms:Describe*\", ")
        hcl_code_list.append("      \"kms:Enable*\", ")
        hcl_code_list.append("      \"kms:List*\", ")
        hcl_code_list.append("      \"kms:Put*\", ")
        hcl_code_list.append("      \"kms:Update*\", ")
        hcl_code_list.append("      \"kms:Revoke*\", ")
        hcl_code_list.append("      \"kms:Disable*\", ")
        hcl_code_list.append("      \"kms:Get*\", ")
        hcl_code_list.append("      \"kms:Delete*\", ")
        hcl_code_list.append("      \"kms:TagResource\", ")
        hcl_code_list.append("      \"kms:UntagResource\", ")
        hcl_code_list.append("      \"kms:ScheduleKeyDeletion\", ")
        hcl_code_list.append("      \"kms:CancelKeyDeletion\"")
        hcl_code_list.append("    ]")
        hcl_code_list.append("")
        hcl_code_list.append("    principals {")
        hcl_code_list.append("      type = \"AWS\"")
        hcl_code_list.append("      identifiers = [\"arn:aws:iam::${my_account}:root\"]")
        hcl_code_list.append("    }")
        hcl_code_list.append("    resources = [")
        hcl_code_list.append("      \"*\",")
        hcl_code_list.append("    ]")
        hcl_code_list.append("  }")
        hcl_code_list.append("")
        hcl_code_list.append("  statement {")
        hcl_code_list.append("    sid = \"Allow use of the key\"")
        hcl_code_list.append("")
        hcl_code_list.append("    actions = [")
        hcl_code_list.append("      \"kms:Encrypt\", ")
        hcl_code_list.append("      \"kms:Decrypt\", ")
        hcl_code_list.append("      \"kms:ReEncrypt*\", ")
        hcl_code_list.append("      \"kms:DescribeKey\", ")
        hcl_code_list.append("      \"kms:GetPublicKey\"")
        hcl_code_list.append("    ]")
        hcl_code_list.append("")
        hcl_code_list.append("    principals {")
        hcl_code_list.append("      type = \"AWS\"")
        hcl_code_list.append("      identifiers = [")
        hcl_code_list.append("      \"arn:aws:iam::${my_account}:root\", ")
        hcl_code_list.append("      \"arn:aws:iam::{my_account}:role/${var.instance_profile_role_name}\"]")
        hcl_code_list.append("    }")
        hcl_code_list.append("    resources = [")
        hcl_code_list.append("      \"*\",")
        hcl_code_list.append("    ]")
        hcl_code_list.append("  }")
        hcl_code_list.append("")
        hcl_code_list.append("  statement {")
        hcl_code_list.append("    sid = \"Allow attachment of persistent resources\"")
        hcl_code_list.append("")
        hcl_code_list.append("    actions = [")
        hcl_code_list.append("      \"kms:CreateGrant\", \"kms:ListGrants\", \"kms:RevokeGrant\"")
        hcl_code_list.append("    ]")
        hcl_code_list.append("")
        hcl_code_list.append("    principals {")
        hcl_code_list.append("      type = \"AWS\"")
        hcl_code_list.append("      identifiers = [\"arn:aws:iam::${my_account}:root\"]")
        hcl_code_list.append("    }")
        hcl_code_list.append("    resources = [")
        hcl_code_list.append("      \"*\",")
        hcl_code_list.append("    ]")
        hcl_code_list.append("")
        hcl_code_list.append("    condition {")
        hcl_code_list.append("      test = \"Bool\"")
        hcl_code_list.append("      variable = \"kms:GrantIsForAWSResource\"")
        hcl_code_list.append("      variables = [\"true\"]")
        hcl_code_list.append("    }")
        hcl_code_list.append("  }")
        hcl_code_list.append("}")
        hcl_code_list.append("")
        hcl_code_list.append("resource \"aws_kms_key\" \"%s\" {" % (aliase_name,))
        hcl_code_list.append("    description             = \"%s\"" % (aliase_name,))
        hcl_code_list.append("    key_usage               = \"ENCRYPT_DECRYPT\"")
        hcl_code_list.append("    is_enabled              = true")
        hcl_code_list.append("    enable_key_rotation     = false")
        hcl_code_list.append("")
        hcl_code_list.append("    policy = data.aws_iam_policy_document.%s-doc.json"% (aliase_name,))
        hcl_code_list.append("}")
        save_file(f"aws_kms_key_{aliase_name}.tf", "\n".join(hcl_code_list))
        return "\n".join(hcl_code_list)

    def make_alias(self, key_id):
        print("make alias ==>")
        object = self.get_key(key_id)

        alias_name = self.get_alias_name(key_id)
        alias = self.get_alias(key_id)

        hcl_code_list = []

        hcl_code_list.append("data \"aws_iam_policy_document\" \"%s-doc\" {" % (alias_name,))
        hcl_code_list.append("resource \"aws_kms_alias\" \"%s\" {" % (alias_name,))
        hcl_code_list.append("    name          = \"alias/%s\"" % (alias_name,))
        hcl_code_list.append("    target_key_id = \"%s\"" %(alias['TargetKeyId'],))
        hcl_code_list.append("}")

        save_file(f"aws_kms_alias_{alias_name}.tf", "\n".join(hcl_code_list))
        return "\n".join(hcl_code_list)

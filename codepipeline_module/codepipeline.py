import boto3
from common_module.string_util import camelToSnake
from common_module.save_file import save_file
import sys

class CodePipeline:

    def __init__(self, profile_name):
        session = boto3.Session(profile_name=profile_name)
        self.client = session.client('codepipeline')

    def list_pipelines(self):
        objects = self.client.list_pipelines()
        list = []
        for object in objects['pipelines']:
            list.append(object['name'])
        return list

    def get_pipeline(self, pipeline_name):
        objects = self.client.get_pipeline(name=pipeline_name)
        object = objects['pipeline']
        return object

    def make_pipeline(self, pipeline_name):
        objects = self.client.get_pipeline(name=pipeline_name)
        object = objects['pipeline']
        print(object)
        # argument_list = ['roleArn', 'artifactStore', 'stages']
        # result = {}
        #
        # result['name'] = pipeline_name
        # for argument_string in argument_list:
        #     snake_string = camelToSnake(argument_string)
        #     result[snake_string] = object[argument_string]

        hcl_code_list = []
        hcl_code_list.append("resource \"aws_codepipeline\" \"%s\" {" % (object['name'],))
        hcl_code_list.append(f"  name     = \"{object['name']}\"")
        hcl_code_list.append(f"  role_arn = \"{object['roleArn']}\"")
        hcl_code_list.append(f"")
        hcl_code_list.append("  artifact_store {")
        hcl_code_list.append(f"    location = \"{object['artifactStore']['location']}\"")
        hcl_code_list.append(f"    type     = \"{object['artifactStore']['type']}\"")
        hcl_code_list.append(f"")
        if "encryption_key" in object['artifactStore']:
            hcl_code_list.append("    encryption_key {")
            hcl_code_list.append(f"      id   = data.aws_kms_alias.s3kmskey.arn")
            hcl_code_list.append(f"      type = \"KMS\"")
            hcl_code_list.append("    }")
        hcl_code_list.append("  }")
        hcl_code_list.append("")
        source_object = None
        build_object = None
        deploy_object = None
        for stage in object['stages']:
            if stage['name'] == "Source":
                source_object = stage
            elif stage['name'] == "Build":
                build_object = stage
            elif stage['name'] == "Deploy":
                deploy_object = stage

        hcl_code_list.append("  stage {")
        hcl_code_list.append(f"    name = \"{source_object['name']}\"")
        hcl_code_list.append(f"")
        for action in source_object['actions']:
            hcl_code_list.append("    action {")
            hcl_code_list.append(f"      name             = \"{action['name']}\"")
            hcl_code_list.append(f"      namespace        = \"{action['namespace']}\"")
            hcl_code_list.append(f"      category         = \"{action['actionTypeId']['category']}\"")
            hcl_code_list.append(f"      owner            = \"{action['actionTypeId']['owner']}\"")
            hcl_code_list.append(f"      provider         = \"{action['actionTypeId']['provider']}\"")
            hcl_code_list.append(f"      version          = \"{action['actionTypeId']['version']}\"")
            if len(action['outputArtifacts']) == 1:
                hcl_code_list.append(f"      output_artifacts = [\"{action['outputArtifacts'][0]['name']}\"]")
            else:
                print("output_artifacts 는 한개만 세팅되게 되어 있다.")
                sys.exit(1)
            hcl_code_list.append(f"")
            hcl_code_list.append("      configuration = {")
            hcl_code_list.append(f"        BranchName    = \"{action['configuration']['BranchName']}\"")
            hcl_code_list.append(f"        OutputArtifactFormat = \"{action['configuration']['OutputArtifactFormat']}\"")
            hcl_code_list.append(f"        PollForSourceChanges       = \"{action['configuration']['PollForSourceChanges']}\"")
            hcl_code_list.append(f"        RepositoryName       = \"{action['configuration']['RepositoryName']}\"")
            hcl_code_list.append("      }")
            hcl_code_list.append("    }")
            hcl_code_list.append("  }")
        hcl_code_list.append(f"")

        hcl_code_list.append("  stage {")
        hcl_code_list.append(f"    name = \"{build_object['name']}\"")
        hcl_code_list.append("")
        for action in build_object['actions']:
            hcl_code_list.append("    action {")
            hcl_code_list.append(f"      name             = \"{action['name']}\"")
            if "namespace" in action:
                hcl_code_list.append(f"      namespace        = \"{action['namespace']}\"")
            hcl_code_list.append(f"      category         = \"{action['actionTypeId']['category']}\"")
            hcl_code_list.append(f"      owner            = \"{action['actionTypeId']['owner']}\"")
            hcl_code_list.append(f"      provider         = \"{action['actionTypeId']['provider']}\"")
            if len(action['inputArtifacts']) == 1:
                hcl_code_list.append(f"      input_artifacts  = [\"{action['inputArtifacts'][0]['name']}\"]")
            else:
                print("input_artifacts 는 한개만 세팅되게 되어 있다.")
                sys.exit(1)
            if len(action['outputArtifacts']) == 1:
                hcl_code_list.append(f"      output_artifacts = [\"{action['outputArtifacts'][0]['name']}\"]")
            else:
                print("input_artifacts 는 한개만 세팅되게 되어 있다.")
                sys.exit(1)
            hcl_code_list.append(f"      version          = \"{action['actionTypeId']['version']}\"")
            hcl_code_list.append(f"")
            hcl_code_list.append("      configuration = {")
            hcl_code_list.append(f"        ProjectName = \"{action['configuration']['ProjectName']}\"")
            hcl_code_list.append("      }")
            hcl_code_list.append("    }")
        hcl_code_list.append("  }")
        hcl_code_list.append("")
        hcl_code_list.append("  stage {")
        hcl_code_list.append(f"    name = \"{deploy_object['name']}\"")
        hcl_code_list.append(f"")
        for action in deploy_object['actions']:
            hcl_code_list.append("    action {")
            hcl_code_list.append(f"      name            = \"{action['name']}\"")
            hcl_code_list.append(f"      category        = \"{action['actionTypeId']['category']}\"")
            hcl_code_list.append(f"      owner           = \"{action['actionTypeId']['owner']}\"")
            hcl_code_list.append(f"      provider        = \"{action['actionTypeId']['provider']}\"")
            if len(action['inputArtifacts']) == 1:
                hcl_code_list.append(f"      input_artifacts = [\"{action['inputArtifacts'][0]['name']}\"]")
            else:
                print("input_artifacts 는 한개만 세팅되게 되어 있다.")
                sys.exit(1)
            hcl_code_list.append(f"      version         = \"{action['actionTypeId']['version']}\"")
            hcl_code_list.append(f"")
            hcl_code_list.append("      configuration = {")
            hcl_code_list.append(f"        ApplicationName     = \"{action['configuration']['ApplicationName']}\"")
            hcl_code_list.append(f"        DeploymentGroupName   = \"{action['configuration']['DeploymentGroupName']}\"")
            hcl_code_list.append("      }")
            hcl_code_list.append("    }")
            hcl_code_list.append("  }")
        hcl_code_list.append("}")

        save_file(f"aws_codepipeline_{pipeline_name}.tf", "\n".join(hcl_code_list))
        return "\n".join(hcl_code_list)

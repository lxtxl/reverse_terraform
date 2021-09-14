import sys
from codepipeline_module.codepipeline import CodePipeline
from config import Config
import json

profile_name = Config().get_profile_name()

def print_pipelines():
    codepipeline = CodePipeline(profile_name)
    print(codepipeline.list_pipelines())

def make_pipeline(pipeline_name):
    codepipeline = CodePipeline(profile_name)
    codepipeline.make_pipeline(pipeline_name)

def print_pipeline(pipeline_name):
    codepipeline = CodePipeline(profile_name)
    print(json.dumps(codepipeline.get_pipeline(pipeline_name), sort_keys=True, indent=4))

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print_pipelines()
    elif len(sys.argv) == 2:
        make_pipeline(sys.argv[1])

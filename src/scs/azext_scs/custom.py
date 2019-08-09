# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
import os
import tarfile
import urllib.request
from knack.util import CLIError
from .vendored_sdks.microservices4spring import models
from ._client_factory import cf_scs
from urllib.parse import urlparse
from azure.storage.file import FileService

DEFAULT_DEPLOYMENT_URL='https://cbd7548b9d7e43ecae3990a0.blob.core.windows.net/hellowrold/helloworld.jar'
DEFAULT_DEPLOYMENT_FILE="helloworld.jar"
DEFAULT_DEPLOYMENT_NAME = "default"
TEMP_TAR="temp.tar"

def scs_create(cmd,
               resource_group,
               name,
               location=None):
    scf = cf_scs(cmd.cli_ctx).app_clusters
    resource = None
    if location is not None:
        resource = models.AppClusterResource(location=location)
    
    return scf.create_or_update(resource_group,
                                name,
                                resource)

def scs_delete(cmd,
               resource_group,
               name):
    scf = cf_scs(cmd.cli_ctx).app_clusters
    return scf.delete(resource_group, name)        

def scs_list(cmd,
             resource_group=None):
    scf = cf_scs(cmd.cli_ctx).app_clusters
    if resource_group is None:
        return scf.list_by_subscription()
    else:
        return scf.list(resource_group)  

def scs_get(cmd,
            resource_group,
            name):
    scf = cf_scs(cmd.cli_ctx).app_clusters
    return scf.get(resource_group, name)  

def app_create(cmd,
               resource_group,
               app_cluster,
               name,
               is_public=False,
               runtime_version=None,
               jvm_options=None,
               vcpu=None,
               memory=None,
               instance_count=None,
               env=None,
               tags=None):
    scf = cf_scs(cmd.cli_ctx)       
    apps = _get_all_apps(scf, resource_group, app_cluster)
    if name in apps:
        raise CLIError("App " + name + "already exists.")

    properties = models.AppResourceProperties(public=is_public)
    scf.apps.create_or_update(resource_group, app_cluster, name, properties)

    # download default hellowrold if not set jar path or target_module
    with open(DEFAULT_DEPLOYMENT_FILE, "w") as f:
        f.write("123")

    # create default deployment
    try:
        deseralized = _app_deploy(scf,
                                  resource_group,
                                  app_cluster,
                                  name,
                                  DEFAULT_DEPLOYMENT_NAME,
                                  DEFAULT_DEPLOYMENT_FILE,
                                  runtime_version,
                                  jvm_options,
                                  vcpu,
                                  memory,
                                  instance_count,
                                  env,
                                  tags)
        print(deseralized)
        properties = models.AppResourceProperties(active_deployment_name=DEFAULT_DEPLOYMENT_NAME)
        return scf.apps.update(resource_group, app_cluster, name, properties)
    except:
        scf.apps.delete(resource_group, app_cluster, name)
        raise CLIError("Create default deployment failed, deleting app...")

def app_update(cmd,
               resource_group,
               app_cluster,
               name,
               is_public=None,
               runtime_version=None,
               jvm_options=None,
               vcpu=None,
               memory=None,
               instance_count=None,
               env=None,
               tags=None):
    scf = cf_scs(cmd.cli_ctx)
    if is_public is not None:
        properties = models.AppResourceProperties(public=is_public)
        app_updated = scf.apps.update(resource_group, app_cluster, name, properties)
        print(app_updated)
    active_deployment = scf.apps.get(resource_group, app_cluster, name).properties.active_deployment_name
    if active_deployment is None:
        return

    deployment_settings = models.DeploymentSettings(
                                cpu=vcpu,
                                memory_in_gb=memory,
                                environment_variables=env,
                                jvm_options=jvm_options,
                                runtime_version=runtime_version,
                                instance_count=instance_count,)
    properties = models.DeploymentResourceProperties(deployment_settings=deployment_settings)
    return scf.deployments.update(resource_group, app_cluster, name, active_deployment, properties)

def app_delete(cmd,
              resource_group,
              app_cluster,
              name):
    scf = cf_scs(cmd.cli_ctx).apps
    return scf.delete(resource_group, app_cluster, name)

def app_start(cmd,
              resource_group,
              app_cluster,
              name):
    scf = cf_scs(cmd.cli_ctx)
    active_deployment = scf.apps.get(resource_group, app_cluster, name).properties.active_deployment_name
    if active_deployment is None:
        raise CLIError("No active deployment found, can't start app")
    return  scf.deployments.start(resource_group, app_cluster, name, active_deployment)

def app_stop(cmd,
             resource_group,
             app_cluster,
             name):
    scf = cf_scs(cmd.cli_ctx)
    active_deployment = scf.apps.get(resource_group, app_cluster, name).properties.active_deployment_name
    if active_deployment is None:
        raise CLIError("No active deployment found, can't stop app")
    return  scf.deployments.stop(resource_group, app_cluster, name, active_deployment)

def app_restart(cmd,
                resource_group,
                app_cluster,
                name):
    scf = cf_scs(cmd.cli_ctx)
    active_deployment = scf.apps.get(resource_group, app_cluster, name).properties.active_deployment_name
    if active_deployment is None:
        raise CLIError("No active deployment found, can't stop app")
    return  scf.deployments.restart(resource_group, app_cluster, name, active_deployment)

def app_list(cmd,
               resource_group,
               app_cluster):
    scf = cf_scs(cmd.cli_ctx).apps
    return scf.list(resource_group, app_cluster)

def app_get(cmd,
            resource_group,
            app_cluster,
            name):
    scf = cf_scs(cmd.cli_ctx).apps
    return scf.get(resource_group, app_cluster, name, True)

def app_deploy(cmd,
               resource_group,
               app_cluster,
               name,
               deployment =None,
               jar_path=None,
               target_module=None,
               runtime_version=None,
               jvm_options=None,
               vcpu=None,
               memory=None,
               instance_count=None,
               env=None,
               tags=None
               ):
    scf = cf_scs(cmd.cli_ctx)
    if deployment is None:
        deployment = scf.apps.get(resource_group, app_cluster, name).properties.active_deployment_name
        if deployment is None:
            raise CLIError("No active deployment found, please specify a deployment name")
    else:
        deployments = _get_all_deployments(scf, resource_group, app_cluster, name)
        if deployment not in deployments:
            raise CLIError("deployment" + deployment + " not found, please use 'az scs app deploy create' to create a new deployment")

    # get file path
    path = jar_path
    if path is None:
        path = os.getcwd()
        _make_targz(TEMP_TAR, path)
        path = TEMP_TAR
    
    # get file type
    file_type = "tar" if jar_path is None else "jar"

    return _app_deploy(scf,
                       resource_group,
                       app_cluster,
                       name,
                       deployment,
                       path,
                       runtime_version,
                       jvm_options,
                       vcpu,
                       memory,
                       instance_count,
                       env,
                       tags,
                       file_type)   

def deployment_create(cmd,
                      resource_group,
                      app_cluster,
                      app,
                      name,
                      jar_path=None,
                      target_module=None,
                      runtime_version=None,
                      jvm_options=None,
                      vcpu=None,
                      memory=None,
                      instance_count=None,
                      env=None,
                      tags=None
                      ):
    scf = cf_scs(cmd.cli_ctx)
    deployments = _get_all_deployments(scf, resource_group, app_cluster, app)
    if name in deployments:
        raise CLIError("deployment " + name + " already exists")

    # get file path
    path = jar_path
    if path is None:
        path = os.getcwd()
        _make_targz(TEMP_TAR, path)
        path = TEMP_TAR
    
    # get file type
    file_type = "tar" if jar_path is None else "jar"
    return _app_deploy(scf,
                       resource_group,
                       app_cluster,
                       app,
                       name,
                       path,
                       runtime_version,
                       jvm_options,
                       vcpu,
                       memory,
                       instance_count,
                       env,
                       tags,
                       file_type) 

def deployment_activate(cmd,
                        resource_group,
                        app_cluster,
                        app,
                        name):
    scf = cf_scs(cmd.cli_ctx)
    deployments = _get_all_deployments(scf, resource_group, app_cluster, app)
    active_deployment = scf.apps.get(resource_group, app_cluster, app).properties.active_deployment_name
    if name == active_deployment:
        raise CLIError("deployment '" + name + "' is alredy the active deployment")
    if name not in deployments:
        raise CLIError("deployment '" + name + "' not found, please use 'az scs app deploy create' to create new deployment first")  
    properties = models.AppResourceProperties(active_deployment_name=name)
    return scf.apps.update(resource_group, app_cluster, app, properties)

def deployment_list(cmd,
                    resource_group,
                    app_cluster,
                    app):
    scf = cf_scs(cmd.cli_ctx).deployments
    return scf.list(resource_group, app_cluster, app)

def deployment_get(cmd,
                   resource_group,
                   app_cluster,
                   app,
                   name):
    scf = cf_scs(cmd.cli_ctx).deployments
    return scf.get(resource_group, app_cluster, app, name)

def deployment_delete(cmd,
                      resource_group,
                      app_cluster,
                      app,
                      name):
    scf = cf_scs(cmd.cli_ctx).deployments
    return scf.delete(resource_group, app_cluster, app, name)

def _make_targz(output_filename, source_dir):
    with tarfile.open(output_filename, "w:") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))

def _get_all_deployments(client, resource_group, app_cluster, app):
    deployments = []
    deployments_resource = client.deployments.list(resource_group, app_cluster, app)
    # iterate deployments until end of page
    try:
        while True:
            deployment = deployments_resource.__next__()
            deployments.append(deployment.name)
    except StopIteration:
        pass
    return deployments

def _get_all_apps(client, resource_group, app_cluster):
    apps = []
    apps_resource = client.apps.list(resource_group, app_cluster)
    # iterate deployments until end of page
    try:
        while True:
            app = apps_resource.__next__()
            apps.append(app.name)
    except StopIteration:
        pass
    return apps

def _app_deploy(client,
               resource_group,
               app_cluster,
               app,
               name,
               path,
               runtime_version,
               jvm_options,
               vcpu,
               memory,
               instance_count,
               env,
               tags,
               file_type="jar",
               ):
    response = client.apps.get_resource_upload_url(resource_group,
                                                   app_cluster,
                                                   name,
                                                   None,
                                                   None)
    upload_url = response.upload_url
    relative_path = response.upload_url.split('?')[0]
    prase_result = urlparse(upload_url)
    storage_name = prase_result.netloc.split('.')[0]
    split_path = prase_result.path.split('/')[1:3]
    share_name, file_name = split_path[0], split_path[1]
    sas_token = "?" + prase_result.query
    deployment_settings = models.DeploymentSettings(
                                    cpu=vcpu,
                                    memory_in_gb=memory,
                                    environment_variables=env,
                                    jvm_options=jvm_options,
                                    runtime_version=runtime_version,
                                    instance_count=instance_count,)
    artifactInfo = models.ArtifactInfo(relative_path=relative_path, resource_type=file_type)
    properties = models.DeploymentResourceProperties(
                            deployment_settings=deployment_settings,
                            artifact=artifactInfo)

    #upload file 
    file_service = FileService(storage_name, sas_token=sas_token)
    file_service.create_file_from_path(share_name, None, file_name, path)
    
    #create deployment
    return client.deployments.create_or_update(resource_group,
                                        app_cluster,
                                        app,
                                        name,
                                        properties)


def _download_file(url, file):
    with urllib.request.urlopen(url) as response, open(file, 'wb') as out_file:
        data = response.read()
        out_file.write(data)
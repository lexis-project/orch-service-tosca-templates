# Template of a service provided by a private Docker container on a Cloud instance

Template of a LEXIS workflow allowing to transfer a dataset from DDI to a Cloud
Compute instance on which a on which a service will be launched by a Docker container created from a private image archive stored in DDI:

The Run workflow is:
* getting details on the input dataset (size, locations)
* asking the Dynamic Allocation Module (DAM) to select the best Cloud infrastructure to compute these input data
* transferring the input dataset from DDI to the selected Cloud Staging Area
* transferring the private docker image archive dataset from DDI to the selected Cloud Staging Area
* creating a Cloud Compute instance
* installating and starting Docker
* SSHFS-mounting the staging area directory where the input dataset was staged on this compute instance
* SSHFS-mounting the staging area directory where the private docker image archive dataset was staged on this compute instance
* loading the private docker image from the archive
* running the Docker container in detached mode

The service provided by the container will then be available, until the user decides to delete the workflow execution.

## Input properties

The template expects the following input properties (mandatory inputs in **bold**):
*  **token**: OpenID Connect access token
* **project_id**: LEXIS project identifier
* **computation_dataset_path_input_path**: Dataset containing input data
* **computation_dataset_path_docker_image_path**: Docker image tar archive path in DDI
* **computation_docker_image_name**: Name of docker image to load (name:tag)
* computation_decrypt_dataset_input: Should the input dataset be decrypted
  * default: `false`
* computation_uncompress_dataset_input: the input dataset be uncompressed
  * default: `false`
* computation_mount_point_input_dataset: Directory on the compute instance where to mount the dataset
  * default: `/mnt/lexis_input`
* computation_container_env_vars: Computation container environment variables
  * Example:
    * `INPUT_DIR: "/input_dataset"`
* computation_container_volumes: List of volumes to mount within the computation container (Use docker CLI-style syntax: /host:/container[:mode])
  * default:
    * `/mnt/lexis_input:/input_dataset`
* computation_container_published_ports: List of ports to publish from the container to the host. Use docker CLI syntax: 8000, 9000:8000, or 0.0.0.0:9000:8000, where 8000 is a container port, 9000 is a host port, and 0.0.0.0 is a host interface.
* computation_expose_url_in_outputs: Expose a URL in workflow outputs
  * default: true
* computation_exposed_url_port: Port to use in exposed URL
  * default: ""
* computation_exposed_url_protocol: Protocol to use in exposed URL
  * default: "https"

## Ouput attribute

The following output attribute is provided:
* attribute `url` of component `ComputeExternalAccess`: the URL to access the service, when applicable

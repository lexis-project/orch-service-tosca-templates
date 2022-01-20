# Template of a Cloud Computation using a private Docker container

Template of a LEXIS Cloud Computation using a private container that doesn't need inputs or outputs in DDI.

The Run workflow is:
* getting details on the input dataset containing the docker image (size, locations)
* asking the Dynamic Allocation Module (DAM) to select the best Cloud infrastructure for this input dataset
* transferring the private docker image archive dataset from DDI to the selected Cloud Staging Area
* creating a Cloud Compute instance
* installating and starting Docker
* SSHFS-mounting the staging area directory where the private docker image archive dataset was staged on this compute instance
* loading the private docker image from the archive
* executing the Docker container performing a computation
* cleaning up the cloud staging area and releasing the cloud compute instance

## Input properties

The template expects the following input properties (mandatory inputs in **bold**):
*  **token**: OpenID Connect access token
* **project_id**: LEXIS project identifier
* **computation_dataset_path_docker_image_path**: Docker image tar archive path in DDI
* **computation_docker_image_name**: Name of docker image to load (name:tag)
* computation_container_env_vars: Computation container environment variables
  * Example:
    * `INPUT_DIR: "/input_dataset"`
    * `RESULT_DIR: "/output"`
    * `RESULT_FILE_NAME: "computation_result.txt"`
* computation_container_published_ports: List of ports to publish from the container to the host. Use docker CLI syntax: 8000, 9000:8000, or 0.0.0.0:9000:8000, where 8000 is a container port, 9000 is a host port, and 0.0.0.0 is a host interface.

## Ouput attribute

No output attribute


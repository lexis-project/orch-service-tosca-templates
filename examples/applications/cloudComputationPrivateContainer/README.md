# Template of a Cloud Computation using a private Docker container

Template of a LEXIS workflow allowing to transfer a dataset from DDI to a Cloud
Compute instance on which a computation will be done by a Docker container created from a private image archive stored in DDI:

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
* executing the Docker container performing a computation on these inputs
* copying computation results to the cloud staging area
* transferring of these results from the cloud staging area to DDI
* replicating these results to other sites if specified
* cleaning up the cloud staging area and releasing the cloud compute instance

## Input properties

The template expects the following input properties (mandatory inputs in **bold**):
*  **token**: OpenID Connect access token
* **project_id**: LEXIS project identifier
* **computation_dataset_path_input_path**: Dataset containing input data
* **computation_dataset_path_docker_image_path**: Docker image tar archive path in DDI
* **computation_container_volumes**: List of volumes to mount within the computation container. Use docker CLI-style syntax: /host:/container[:mode]
  * Example: map of environment variables expected by the container:
    * `/mnt/lexis_input:/input_dataset`
    * `/lexis/output:/output`
* **computation_docker_image_name**: Name of docker image to load (name:tag)
* **computation_ddi_project_path**: Path where to transfer the computation results in DDI
* computation_decrypt_dataset_input: Should the input dataset be decrypted
  * default: `false`
* computation_uncompress_dataset_input: the input dataset be uncompressed
  * default: `false`
* computation_mount_point_input_dataset: Directory on the compute instance where to mount the dataset
  * default: `/mnt/lexis_input`
* computation_container_env_vars: Computation container environment variables
  * Example:
    * `INPUT_DIR: "/input_dataset"`
    * `RESULT_DIR: "/output"`
    * `RESULT_FILE_NAME: "computation_result.txt"`
* computation_container_published_ports:List of ports to publish from the container to the host. Use docker CLI syntax: 8000, 9000:8000, or 0.0.0.0:9000:8000, where 8000 is a container port, 9000 is a host port, and 0.0.0.0 is a host interface.
* computation_output_directory: Computation output directory
  * default: `/lexis/output`
* computation_metadata_dataset_result: Metadata for the computation results dataset to create in DDI
  * default:
    * creator:
      * `Cloud Computation Private Container worflow`
    * contributor:
      * `Cloud Computation Private Container worflow`
    * publisher:
      * `Cloud Computation Private Container worflow`
    * resourceType: `Dataset`
    * title: `LEXIS Cloud Computation Private Container workflow results`
* computation_encrypt_dataset_result: Encrypt the result dataset
  * default: `false`
* computation_compress_dataset_result: Compress the result dataset
  * default: `false`
* computation_result_dataset_replication_sites: List of sites where the result dataset should be available - WARNING: a replicated dataset can't be deleted - (example of values: it4i, lrz)
  * default: []

## Ouput attribute

The following output attribute is provided:
* attribute `destination_path` of component `CloudToDDIJob`: the path to the result dataset in DDI

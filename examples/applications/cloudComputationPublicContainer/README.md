# Template of a Cloud Computation using a public Docker container

Template of a LEXIS workflow allowing to transfer a dataset from DDI to a Cloud
Compute instance on which a computation will be done by a Docker container:

The Run workflow is:
* getting details on the input dataset (size, locations)
* asking the Dynamic Allocation Module (DAM) to select the best Cloud infrastructure to compute these input data
* transferring the input dataset from DDI to the selected Cloud Staging Area
* creating a Cloud Compute instance
* installating and starting Docker
* SSHFS-mounting the staging area on this compute instance
* executing a Docker container performing a computation on these inputs
* copying computation results to the cloud staging area
* transferring of these results from the cloud staging area to DDI
* replicating these results to other sites if specified
* cleaning up the cloud staging area and releasing the cloud compute instance

## Input properties

The template expects the following input properties (mandatory inputs in **bold**):
*  **token**: OpenID Connect access token
* **project_id**: LEXIS project identifier
* **computation_dataset_path_input_path**: Dataset containing input data
* **computation_container_image**: Computation container repository path
  * for example: `laurentg/lexistest:1.2` (see corresponding [Dockerfile](../cloudHPCComputation/Dockerfile))
* **computation_ddi_project_path**: Path where to transfer the computation results in DDI
* computation_decrypt_dataset_input: Should the input dataset be decrypted
  * default: `false`
* computation_uncompress_dataset_input: the input dataset be uncompressed
  * default: `false`
* computation_mount_point_input_dataset: Directory on the compute instance where to mount the dataset
  * default: `/mnt/lexis_input`
* computation_container_env_vars: Computation container environment variables
  * default: map of environment variables expected by the container:
    * `INPUT_DIR: "/input_dataset"`
    * `RESULT_DIR: "/output"`
    * `RESULT_FILE_NAME: "computation_result.txt"`
* computation_container_volumes: List of volumes to mount within the computation container (Use docker CLI-style syntax: /host:/container[:mode])
  * default:
    * `/mnt/lexis_input:/input_dataset`
    * `/lexis/output:/output`
* computation_output_directory: Computation output directory
  * default: `/lexis/output`
* computation_metadata_dataset_result: Metadata for the computation results dataset to create in DDI
  * default:
    * creator:
      * `Cloud Computation Container worflow`
    * contributor:
      * `Cloud Computation Container worflow`
    * publisher:
      * `Cloud Computation Container worflow`
    * resourceType: `Dataset`
    * title: `LEXIS Cloud Computation Container workflow results`
* computation_encrypt_dataset_result: Encrypt the result dataset
  * default: `false`
* computation_compress_dataset_result: Compress the result dataset
  * default: `false`
* computation_result_dataset_replication_sites: List of sites where the result dataset should be available (example: it4i, lrz)
  * default: []

## Ouput attribute

The following output attribute is provided:
* attribute `destination_path` of component `CloudToDDIJob`: the path to the result dataset in DDI

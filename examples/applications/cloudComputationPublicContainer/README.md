# Template of a Cloud Computation using a public Docker container

Template of a LEXIS workflow allowing to transfer a dataset from DDI to a Cloud
Compute instance on which a computation will be done by a Docker container:

The Run workflow is doing:
* the transfer of an input dataset from DDI to a Cloud Staging Area
* the allocation of a Cloud Compute instance
* the installation and startup of Docker
* the SSHFS mount of the staging area on this compute instance
* the execution of a Docker container performing a computation on these inputs
* the copy of computation results to the cloud staging area
* the transfer of these results from the cloud staging area to DDI
* the cleanup of cloud staging area and release of the cloud compute instance

## Input properties

The template expects the following input properties (mandatory inputs in **bold**):
*  **token**: OpenID Connect access token
* **project_id**: LEXIS project identifier
* computation_dataset_input_path: Dataset containing input data
  * default: a dataset in project demoproject `project/proj812b07ed780274387d12c665fa3a4f7f/03ecd6a8-b8c7-11eb-885c-0050568fcecc`
* computation_decrypt_input_dataset: Should the input dataset be decrypted
  * default: `false`
* computation_uncompress_input_dataset: the input dataset be uncompressed
  * default: `false`
* computation_mount_point_input_dataset: Directory on the compute instance where to mount the dataset
  * default: `/mnt/lexis_input`
* computation_container_image: Computation container repository path
  * default: `laurentg/lexistest:1.2` (see corresponding [Dockerfile](../cloudHPCComputation/Dockerfile))
* computation_container_env_vars: Computation container environment variables
  * default: map of environment variables expected by the container:
    * `INPUT_DIR: "/input_dataset"`
    * `RESULT_DIR: "/output"`
    * `RESULT_FILE_NAME: "computation_result.txt"`
* computation_container_volumes: List of volumes to mount within the computation container (Use docker CLI-style syntax: /host:/container[:mode])
  * default:
    * `/mnt/lexis_input:/input_dataset`
    * `lexis/output:/output`
* computation_output_directory: Computation output directory
  * default: `/lexis/output`
  * computation_ddi_project_path: Path where to transfer the computation results in DDI
    * default: demoproject path, `project/proj812b07ed780274387d12c665fa3a4f7f`
* computation_metadata_dataset_result: Metadata for the computation results dataset to create in DDI
  * default:
    * creator:
      * `LEXIS Cloud Computation worflow`
    * contributor:
      * `LEXIS Cloud Computation worflow`
    * publisher:
      * `LEXIS Cloud Computation worflow`
    * resourceType: `Workflow result`
    * title: `LEXIS Cloud Computation workflow results`
* computation_encrypt_dataset_result: Encrypt the result dataset
  * default: `false`
* computation_compress_dataset_result: Compress the result dataset
  * default: `false`

## Ouput properties

The following output attribute is provided:
* attribute `destination_path` of component `CloudToDDIJob`: the path to the result dataset in DDI

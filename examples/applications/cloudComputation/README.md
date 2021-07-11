# Template of a Cloud Computation

Template of a LEXIS workflow allowing to transfer a dataset from DDI to a Cloud
Compute instance on which a computation will be done by running a script provided by the user:

The Run workflow is:
* getting details on the input dataset (size, locations)
* asking the Dynamic Allocation Module (DAM) to select the best Cloud infrastructure to compute these input data
* transferring the input dataset from DDI to the selected Cloud Staging Area
* creating a Cloud Compute instance
* SSHFS-mounting the staging area on this compute instance (accessible to root only)
* Copying the content of this mounted filesystem on the local filesystem accessible as non-root, by default `/lexis_input/`
* running the user-provided script to perform a computation on these inputs
* copying computation results to the cloud staging area
* transferring of these results from the cloud staging area to DDI
* cleaning up the cloud staging area and releasing the cloud compute instance

## Input properties

The template expects the following input properties (mandatory inputs in **bold**):
*  **token**: OpenID Connect access token
* **project_id**: LEXIS project identifier
* **computation_dataset_input_path**: Dataset containing input data
* **computation_script_content**: Content of the script to execute
* **computation_output_directory**: Path of the directory of results on the Compute Instance to store to DDI
* **computation_ddi_project_path**: Path where to transfer the computation results in DDI
* computation_environment_variables: Environment variables for the script
    * default: `{}`
* computation_input_directory: Local directory on the compute instance where the input dataset is accessible to non-root user
    * default: `/lexis_input`
* computation_compute_instance_image_name: Name of the Openstack image for the Compute Instance to create
    * default: `Ubuntu-18.04`
* computation_compute_instance_user: User used to connect to the compute instance
    * default: `ubuntu`
* computation_mount_point_input_dataset: Directory on the compute instance where to mount the dataset
    * default: `/mnt/lexis_input`
* computation_decrypt_input_dataset: Should the input dataset be decrypted
  * default: `false`
* computation_uncompress_input_dataset: the input dataset be uncompressed
  * default: `false`
* computation_mount_point_input_dataset: Directory on the compute instance where to mount the dataset (accessible to root only)
  * default: `/mnt/lexis_input`
* computation_output_directory: Computation output directory
  * default: `/lexis/output`
* computation_metadata_dataset_result: Metadata for the computation results dataset to create in DDI
  * default:
    * creator:
      * `LEXIS Cloud Computation worflow`
    * contributor:
      * `LEXIS Cloud Computation worflow`
    * publisher:
      * `LEXIS Cloud Computation worflow`
    * resourceType: `Dataset`
    * title: `LEXIS Cloud Computation workflow results`
* computation_encrypt_dataset_result: Encrypt the result dataset
  * default: `false`
* computation_compress_dataset_result: Compress the result dataset
  * default: `false`

## Ouput attribute

The following output attribute is provided:
* attribute `destination_path` of component `CloudToDDIJob`: the path to the result dataset in DDI
* attribute `stdout` of component `ExecScript`: script stdout
* attribute `stderr` of component `ExecScript`: script stderr

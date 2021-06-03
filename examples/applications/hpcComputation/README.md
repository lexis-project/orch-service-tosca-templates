# HPC Computation template

Template of a LEXIS workflow allowing to transfer a dataset from DDI to a HEAppE Job.

The Run workflow is:
* getting details on the input dataset (size, locations)
* asking the Dynamic Allocation Module (DAM) to select the best HPC infrastructure to compute these input data
* creating a HEAppE job on this HPC infrastructure
* transferring the input dataset from DDI to the HEAppE job input directory on the HPC cluster
* submitting the HEAppE job and monitoring its execution until it ends
* transferring the HEAppE job results from the HPC cluster to DDI
* deleting the HEAppE job

## Input properties

The template expects the following input properties (mandatory inputs in **bold**):
*  **token**: OpenID Connect access token
* **project_id**: LEXIS project identifier
* **computation_dataset_input_path**: Dataset containing input data
* **computation_ddi_project_path**: Path where to transfer the computation results in DDI
* **computation_heappe_command_template_name**: HEAppE Command Template Name
* **computation_heappe_walltime_limit**: Maximum time for the HEAppE Command Template to run (in seconds)
* **computation_heappe_number_of_cores**: Number of cores required
* computation_heappe_parameter_name: HEAppE Command Template parameter name
  * default: `""`
* computation_heappe_parameter_value: HEAppE Command Template parameter value
  * default: `""`
* computation_decrypt_input_dataset: Should the input dataset be decrypted
  * default: `false`
* computation_uncompress_input_dataset: the input dataset be uncompressed
  * default: `false`
* computation_metadata_dataset_result: Metadata for the computation results dataset to create in DDI
  * default:
    * creator:
      * `LEXIS HPC Computation worflow`
    * contributor:
      * `LEXIS HPC Computation worflow`
    * publisher:
      * `LEXIS HPC Computation worflow`
    * resourceType: `Workflow result`
    * title: `LEXIS HPC Computation workflow results`
* computation_encrypt_dataset_result: Encrypt the result dataset
  * default: `false`
* computation_compress_dataset_result: Compress the result dataset
  * default: `false`

## Ouput attribute

The following output attribute is provided:
* attribute `destination_path` of component `HPCToDDIJob`: the path to the result dataset in DDI

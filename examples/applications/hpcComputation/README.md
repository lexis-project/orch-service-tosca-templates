# HPC Computation template

Template of a LEXIS workflow allowing to transfer a dataset from DDI to a HEAppE Job.

The Run workflow is:
* getting details on the input dataset (size, locations)
* asking the Dynamic Allocation Module (DAM) to select the best HPC infrastructure to compute these input data
* creating a HEAppE job on this HPC infrastructure
* transferring the input dataset from DDI to the HEAppE job input directory on the HPC cluster
* submitting the HEAppE job and monitoring its execution until it ends
* transferring the HEAppE job results from the HPC cluster to DDI
* replicating these results to other sites if specified
* deleting the HEAppE job

## Input properties

The template expects the following input properties (mandatory inputs in **bold**):
*  **token**: OpenID Connect access token
* **project_id**: LEXIS project identifier
* **computation_dataset_path_input_path**: Dataset containing input data
* **computation_ddi_project_path**: Path where to transfer the computation results in DDI
* **computation_heappe_command_template_name**: HEAppE Command Template Name
* computation_heappe_command_template_name: HEAppE Command Template Name
  * default: `GenericCommandTemplate`
* computation_heappe_job: Description of the HEAppE job/tasks
  * default:
    * Name: `GenericJob`
    * Project: `Set by orchestrator`
    * ClusterId: `1`
    * Tasks:
      * Name: `GenericCommandTemplate`
      * ClusterNodeTypeId: `1`
      * CommandTemplateId: `1`
      * TemplateParameterValues:
        * CommandParameterIdentifier: `userScriptPath`
          ParameterValue: ``
      * WalltimeLimit: `3600`
      * MinCores: `1`
      * MaxCores: `1`
      * Priority: `4`
      * StandardOutputFile: `stdout`
      * StandardErrorFile: `stderr`
      * ProgressFile: `stdprog`
      * LogFile: `stdlog`
* computation_hpc_subdirectory_to_stage: Relative path to a subddirectoy on the HPC job cluster file system, to stage
  * default: `""`
* computation_decrypt_dataset_input: Should the input dataset be decrypted
  * default: `false`
* computation_uncompress_dataset_input: the input dataset be uncompressed
  * default: `false`
* computation_metadata_dataset_result: Metadata for the computation results dataset to create in DDI
  * default:
    * creator:
      * `HPC Computation worflow`
    * contributor:
      * `HPC Computation worflow`
    * publisher:
      * `HPC Computation worflow`
    * resourceType: `Dataset`
    * title: `HPC Computation workflow results`
* computation_encrypt_dataset_result: Encrypt the result dataset
  * default: `false`
* computation_compress_dataset_result: Compress the result dataset
  * default: `false`
* computation_result_dataset_replication_sites: List of sites where the result dataset should be available - WARNING: a replicated dataset can't be deleted - (example of values: it4i, lrz)
  * default: []

## Ouput attribute

The following output attribute is provided:
* attribute `destination_path` of component `HPCToDDIJob`: the path to the result dataset in DDI

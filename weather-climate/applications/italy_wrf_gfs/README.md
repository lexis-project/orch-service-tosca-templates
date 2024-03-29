# WRF GFS computation over Italy Template

The Run workflow for the WRF GFS computation over Italy template is executing the following steps:
* getting details on the input dataset (size, locations) in DDI containing static geographical data
* asking the Dynamic Allocation Module (DAM) to select the best Cloud infrastructure where to transfer these input data
* transferring the geographical static data input dataset from DDI to the selected Cloud Staging Area
* creating a Cloud Compute instance
* then, in parallel:
  * waiting for the end of geographical static data input dataset transfer on cloud staging area and SSHFS-mounting the cloud staging area
  * installing and starting Docker on the compute instance
  * downloading Global Forecast System (GFS) data:
    * from https://nomads.ncep.noaa.gov for recent dates (less than 10 days ago)
    * from https://rda.ucar.edu for historical data (more than 10 days ago)
* once Docker is installed and started, a [container downloading observations data](https://github.com/meteocima/lexis-download-docker) proivded by CIMA is executed
* once the GFS data is downloaded, docker started, and the geographica input data filesystem mounted, the [WPS GFS docker container](https://github.com/meteocima/wps-da.gfs) provided by CIMA is executed
* once the preprocessing is done, the size of results is computed, and the 
Dynamic Allocation Module (DAM) is asked to select the best HPC infrastructure where to create a WRF computation job
* a WRF HEAppE job is created on the selected HPC infrastructure
* pre-processing results are transferred to this WRF job
* the job is then submitted, and the orchestrator monitors its execution until it ends
* once the job is done, WRF results are compressed and stored in DDI
* WRF results are also transferred to the compute instance
* If a Dewetra SFTP server was specified by the user, the results will be uploaded to Dewetra SFTP server
* finally, the cloud staging area is cleaned and the cloud compute instance is released

## Input properties

The template expects the following input properties (mandatory inputs in **bold**):
*  **token**: OpenID Connect access token
* **project_id**: LEXIS project identifier
* **preprocessing_start_date**: Start date of the simulation, format YYYYMMDDHH
* preprocessing_docker_image_gfs: Pre-processing container repository path
  * default: `cimafoundation/wps-da.gfs:v2.0.3`
* preprocessing_docker_image_observation_data: Repository path of container downloading observation data
  * default: `cimafoundation/lexis-download-docker:v1.2.5`
* preprocessing_dataset_path_geographical_data_path: Dataset containing geographical data
  * default: `project/proj2bdfd9ccf5a78c3ec68ee9e1d90d2c1c/055b25ea-ba60-11eb-a44e-0050568fc9b5/static_geog_data.tar.gz`
* preprocessing_decrypt_dataset_geographical_data: Should the input dataset be decrypted
  * default: `false`
* preprocessing_uncompress_dataset_geographical_data: Should the input dataset be uncompressed
  * default: `true`
* computation_heappe_command_template_name: HEAppE Command Template Name
  * default: `WRF Generic`
* computation_email_for_HEAppE_notifications: E-mail where to receive notifications from HEAppE about the computation job (default, no email)
  * default: `""`
* postprocessing_ddi_project_path: Path where to transfer the post-processing results in DDI
  * default: `project/proj2bdfd9ccf5a78c3ec68ee9e1d90d2c1c`
* postprocessing_encrypt_dataset_result: Encrypt the result dataset
  * default: `false`
* postprocessing_compress_dataset_result: Compress the result dataset
  * default: `true`
* postprocessing_dewetra_sftp_server_ip: IP address of a Dewetra SPTP server where to store results (default, no sftp server upload)

## Ouput attribute

The following output attribute is provided:
* attribute `destination_path` of component `HPCToDDIJob`: DDI path to Continuum WRF results

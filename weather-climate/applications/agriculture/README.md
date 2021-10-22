# Agriculture Template - Agricultural impact models

Template of LEXIS workflow for Agricultural impacts.

The Run workflow for the Agricultural impact template is executing the following steps:
* getting details on the input dataset (size, locations) in DDI containing static geographical data
* asking the Dynamic Allocation Module (DAM) to select the best Cloud infrastructure where to transfer these input data
* transferring the geographical static data input dataset from DDI to the selected Cloud Staging Area
* creating a Cloud Compute instance
* then, in parallel:
  * downloading ECMWF data needed for the preprocessing
  * installing and starting Docker on the compute instance
  * wait for the end of geographical static data input dataset transfer on cloud staging area and SSHFS-mount the cloud staging area
* once Docker is installed and started, a [container downloading observations data](https://github.com/meteocima/lexis-download-docker) provided by CIMA is executed
* once the ECMWF data is downloaded, docker started, and the geographica input data filesystem mounted, the [WPS IFS docker container](https://github.com/meteocima/wps-da.ifs) provided by CIMA is executed
* once the preprocessing is done, the size of results is computed, and the 
Dynamic Allocation Module (DAM) is asked to select the best HPC infrastructure where to create a WRF computation job
* a WRF HEAppE job is created on the selected HPC infrastructure
* pre-processing results are transferred to this WRF job
* a DDI dataset containing weather radar reflectivity over France is transferred to this WRF job too
* the job is then submitted, and the orchestrator monitors its execution until it ends
* once the job is done, WRF results are compressed and stored in DDI
* if a SFTP server was specified by the user, these results will also be uploaded to the SFTP server
* finally, the cloud staging area is cleaned and the cloud compute instance is released.

### Agriculture template input properties

The template expects the following input properties (mandatory inputs in **bold**):
*  **token**: OpenID Connect access token
* **project_id**: LEXIS project identifier
* **preprocessing_start_date**: Start date of the simulation, format YYYYMMDDHH
* **computation_dataset_path_radar_observations_data_path**: Dataset containing radar observations data over France for the selected date. Select one of the following datasets containing compressed weather radar reflectivity over France for the month corresponding to the date you specified:
  * for workflow simulation start dates from 2018060100 to 2018003000: `project/proj2bdfd9ccf5a78c3ec68ee9e1d90d2c1c/fce2102e-cdb3-11eb-b462-0050568fc9b5/observations.tar.gz`
  * for workflow simulation start dates from 2018070200 to 20180073100: `project/proj2bdfd9ccf5a78c3ec68ee9e1d90d2c1c/76ab841a-cdb6-11eb-afa8-0050568fc9b5/observations.tar.gz`
  * for workflow simulation start dates from 2018080200 to 2018083100: `project/proj2bdfd9ccf5a78c3ec68ee9e1d90d2c1c/8e7646f4-cdb9-11eb-b462-0050568fc9b5/observations.tar.gz`
  * for workflow simulation start dates from 2018090100 to 2018093000: `project/proj2bdfd9ccf5a78c3ec68ee9e1d90d2c1c/a3c8b5f8-327e-11ec-bfe5-0050568fc9b5/observations.tar.gz`
  * for workflow simulation start dates from 2018100200 to 2018103100: `project/proj2bdfd9ccf5a78c3ec68ee9e1d90d2c1c/c270eaa6-cdbc-11eb-b462-0050568fc9b5/observations.tar.gz`
  * for workflow simulation start dates from 2018110200 to 2018113000: `project/proj2bdfd9ccf5a78c3ec68ee9e1d90d2c1c/99774a7e-cdc0-11eb-afa8-0050568fc9b5/observations.tar.gz`
* postprocessing_agriculture_sftp_server_ip: IP address of a SPTP server where to store results (default, no sftp server upload)
* postprocessing_agriculture_sftp_port: Port of the SFTP server
  * default: `22`
* postprocessing_agriculture_sftp_server_directory: Absolute path to directory on SPTP server where to store results
  * default: `/limagrain`
* postprocessing_dewetra_sftp_server_ip: IP address of a Dewetra SPTP server where to store results (default, no sftp server upload)
* preprocessing_docker_image_ifs: Pre-processing container repository path
  * default: `cimafoundation/wps-da.ifs:v2.0.3`
* preprocessing_docker_image_observation_data: Repository path of container downloading observation data
  * default: `cimafoundation/lexis-download-docker:v1.2.5`
* preprocessing_dataset_path_geographical_data_path: Dataset containing compressed geographical data
  * default: `project/proj2bdfd9ccf5a78c3ec68ee9e1d90d2c1c/055b25ea-ba60-11eb-a44e-0050568fc9b5/static_geog_data.tar.gz`
* preprocessing_decrypt_dataset_geographical_data: Should the input dataset be decrypted
  * default: `false`
* preprocessing_uncompress_dataset_geographical_data: Should the input dataset be uncompressed
  * default: `true`
* computation_decrypt_dataset_radar_observations_data: Should the radar observations data dataset be decrypted
  * default: `false`
* computation_uncompress_dataset_radar_observations_data: Should the radar observations data dataset be uncompressed
  * default: `true`
* postprocessing_ddi_project_path: Path of the project where to transfer the post-processing results in DDI
  * default: `project/proj2bdfd9ccf5a78c3ec68ee9e1d90d2c1c`
* postprocessing_encrypt_wrf_dataset_result: Encrypt the WRF result dataset
  * default: `false`
* postprocessing_compress_wrf_dataset_result: Compress the WRF result dataset
  * default: `true`

### Agriculture template ouput attribute

The following output attribute is provided:
* attribute `destination_path` of component `HPCToDDIJob`: the path to compressed WRF results in DDI

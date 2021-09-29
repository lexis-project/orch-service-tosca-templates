# ADMS Templates - Air quality

Templates of LEXIS workflow for Air quality.
The [ADMS template](adms_template.yaml) provides a full worklow, while the [ADMS post-processing template](adms_postprocessing_template.yaml)
provides a workflow using alreay computed WRF results available as a dataset in LEXIS DDI (Distributed Data Ifrastructure).

## ADMS template

The Run workflow for the ADMS template is executing the following steps:
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
* WRF results are also transferred to the compute instance for post-processing
* a private docker docker image used for post-processing is transferred from DDI to the cloud staging area
* this private docker image is then loaded by docker
* a NCL script available in a DDI dataset and needed by this post-processing container is transferred from DDI to the cloud staging area
* The post-processing container is then run on WRF results to produce MET files
* These MET files are then transferre to DDI
* finally for the final step of the post-processing, the Dynamic Allocation Module (DAM)
is asked to select the best Cloud infrastructure where to create a Windows compute instance
* a windows compute instance is created the selected location
* The orchestrator executes then a powershell script on this Windows instance to generate ADMS results from MET results
and store these ADMS results in DDI
* if a SFTP server was specified by the user, these results will also be uploaded to the SFTP server
* if a Dewetra SFTP server was specified by the user, the results will also be uploaded to Dewetra SFTP server
* finally, the cloud staging area is cleaned and the cloud compute instances are released

### ADMS template input properties

The template expects the following input properties (mandatory inputs in **bold**):
*  **token**: OpenID Connect access token
* **project_id**: LEXIS project identifier
* **preprocessing_start_date**: Start date of the simulation, format YYYYMMDDHH
* **computation_dataset_radar_observations_data_path**: Dataset containing radar observations data over France for the selected date. Select one of the following datasets containing compressed weather radar reflectivity over France for the month corresponding to the date you specified:
  * for workflow simulation start dates from 2018060200 to 2018007100: `project/proj2bdfd9ccf5a78c3ec68ee9e1d90d2c1c/fce2102e-cdb3-11eb-b462-0050568fc9b5/observations.tar.gz`
  * for workflow simulation start dates from 2018070200 to 2018080100: `project/proj2bdfd9ccf5a78c3ec68ee9e1d90d2c1c/76ab841a-cdb6-11eb-afa8-0050568fc9b5/observations.tar.gz`
  * for workflow simulation start dates from 2018080200 to 2018090100: `project/proj2bdfd9ccf5a78c3ec68ee9e1d90d2c1c/8e7646f4-cdb9-11eb-b462-0050568fc9b5/observations.tar.gz`
  * for workflow simulation start dates from 2018090200 to 2018100100: `project/proj2bdfd9ccf5a78c3ec68ee9e1d90d2c1c/f7b2d0aa-cdba-11eb-afa8-0050568fc9b5/observations.tar.gz`
  * for workflow simulation start dates from 2018100200 to 2018110100: `project/proj2bdfd9ccf5a78c3ec68ee9e1d90d2c1c/c270eaa6-cdbc-11eb-b462-0050568fc9b5/observations.tar.gz`
  * for workflow simulation start dates from 2018110200 to 2018120100: `project/proj2bdfd9ccf5a78c3ec68ee9e1d90d2c1c/99774a7e-cdc0-11eb-afa8-0050568fc9b5/observations.tar.gz`
* **postprocessing_adms_type**: type of ADMS simulation executed, `urban` or `industrial`
* **postprocessing_adms_latitude**: latitude (example 47.31322 for the industrial case, 48.8157 for the urban case)
* **postprocessing_adms_longitude**: longitude (example -2.063825 for the industrial case, 2.32126 for the urban case)
* postprocessing_adms_sftp_server_ip: IP address of a SPTP server where to store results (default, no sftp server upload)
* postprocessing_adms_sftp_port: Port of the SFTP server
  * default: `22`
* postprocessing_dewetra_sftp_server_ip: IP address of a Dewetra SPTP server where to store results (default, no sftp server upload)
* preprocessing_docker_image_ifs: Pre-processing container repository path
  * default: `cimafoundation/wps-da.ifs:v2.0.3`
* preprocessing_docker_image_observation_data: Repository path of container downloading observation data
  * default: `cimafoundation/lexis-download-docker:v1.2.5`
* preprocessing_dataset_geographical_data_path: Dataset containing compressed geographical data
  * default: `project/proj2bdfd9ccf5a78c3ec68ee9e1d90d2c1c/055b25ea-ba60-11eb-a44e-0050568fc9b5/static_geog_data.tar.gz`
* preprocessing_decrypt_dataset_geographical_data: Should the input dataset be decrypted
  * default: `false`
* preprocessing_uncompress_dataset_geographical_data: Should the input dataset be uncompressed
  * default: `true`
* computation_decrypt_dataset_radar_observations_data: Should the radar observations data dataset be decrypted
  * default: `false`
* computation_uncompress_dataset_radar_observations_data: Should the radar observations data dataset be uncompressed
  * default: `true`
* postprocessing_adms_sftp_industrial_dir: SFTP destination directory for the industrial case
  * default: `/adms5`
* postprocessing_adms_sftp_urban_dir: SFTP destination directory for the urban case
  * default: `/admsurban`
* postprocessing_title_dataset_MET_results: Title of the MET processing results dataset to create in DDI (will be suffixed by the start data)
  * default: `MET processing results`
* postprocessing_title_dataset_adms_result: Which will be the title of the dataset containing ADMS results (will be suffixed by the start data)
  * default: `ADMS results`
* postprocessing_docker_image: Post-processing docker image name:tag
  * default: `adms/ncl:1.0.0`
* postprocessing_dataset_docker_image_path: Post-processing docker image tar archive path in DDI
  * default: `project/proj2bdfd9ccf5a78c3ec68ee9e1d90d2c1c/263a6916-f506-11eb-8bc2-0050568fc9b5`
* postprocessing_dataset_ncl_script_path: Post-processing NCL script dataset path in DDI
  * default: project/proj2bdfd9ccf5a78c3ec68ee9e1d90d2c1c/6fb84668-f50a-11eb-8bc2-0050568fc9b5
* postprocessing_ddi_project_path: Path of the project where to transfer the post-processing results in DDI
  * default: `project/proj2bdfd9ccf5a78c3ec68ee9e1d90d2c1c`
* postprocessing_dataset_id_adms_urban_app: ID of the dataset containing the ADMSUrban.exe and corresponding files. The DDI dataset has to contain single file called adms_urban.zip
  * default: `f284db6c-2588-11eb-bbae-0050568fcecc`
* postprocessing_dataset_id_adms_urban_static_data: ID of the dataset containing the static data for ADMSUrban
  * default: `f1275722-25b5-11eb-bbae-0050568fcecc`
* postprocessing_dataset_id_adms_industrial_app: ID of the dataset containing the ADMSIndustrial.exe and corresponding files. The DDI dataset has to contain single file called adms_industrial.zip
  * default: `ab773490-544a-11eb-b72c-0050568fcecc`
* `postprocessing_dataset_id_adms_industrial_static_data`: ID of the dataset containing the static data for ADMSIndustrial
  * default: `b6e09a96-25ac-11eb-bbae-0050568fcecc`
* postprocessing_encrypt_wrf_dataset_result: Encrypt the WRF result dataset
  * default: `false`
* postprocessing_compress_wrf_dataset_result: Compress the WRF result dataset
  * default: `true`

### ADMS template ouput attributes

The following output attribute is provided:
* attribute `destination_path` of component `CloudToDDIWRFJob`: the path to compressed WRF results in DDI
* attribute `destination_path` of component `METResultsToDDIJob`: the path to ADMS MET results in DDI
* attribute `dataset_id_result` of component `ADMS`: the ID of the DDI dataset where ADMS post-process results are stored

## ADMS post-processing template

The ADMS post-processing template is only performing the post-processing, taking
in input a WRF results dataset that was stored in DDI by a previous ADMS template workfolow execution.

This workflow is executing the following steps:
* getting details on the WRF results input dataset (size, locations) in DDI
* asking the Dynamic Allocation Module (DAM) to select the best Cloud infrastructure where to transfer these input data
* transferring the WRF results input dataset from DDI to the selected Cloud Staging Area
* creating a Cloud Compute instance
* a private docker docker image used for post-processing is transferred from DDI to the cloud staging area
* this private docker image is then loaded by docker
* a NCL script available in a DDI dataset and needed by this post-processing container is transferred from DDI to the cloud staging area
* The post-processing container is then run on WRF results to produce MET files
* These MET files are then transferre to DDI
* finally for the final step of the post-processing, the Dynamic Allocation Module (DAM)
is asked to select the best Cloud infrastructure where to create a Windows compute instance
* A windows compute instance is created the selected location
* The orchestrator executes then a powershell script on this Windows instance to generate ADMS results from MET results
and store these ADMS results in DDI
* If a SFTP server was specified by the user, these results will also be uploaded to the SFTP server. 

### ADMS post-processing template input properties

The template expects the following input properties (mandatory inputs in **bold**):
*  **token**: OpenID Connect access token
* **project_id**: LEXIS project identifier
* **postprocessing_dataset_wrf_results_path**: WRF results dataset path in DDI
* **postprocessing_adms_type**: Type of ADMS simulation executed, `urban` or `industrial`
* **preprocessing_start_date**: Start date of the simulation, format YYYYMMDDHH
* **postprocessing_title_dataset_MET_results**: Title of the MET processing results dataset to create in DDI
* **postprocessing_title_dataset_adms_result**: Title of the ADMS results dataset to create in DDI
* postprocessing_adms_sftp_server_ip: IP address of a SPTP server where to store results (default, no sftp server upload)
* postprocessing_adms_sftp_port: Port of the SFTP server
  * default: `22`
* postprocessing_adms_sftp_industrial_dir: SFTP destination directory for the industrial case
  * default: `/adms5`
* postprocessing_adms_sftp_urban_dir: SFTP destination directory for the urban case
  * default: `/admsurban`
* postprocessing_docker_image: Post-processing docker image name:tag
  * default: `adms/ncl:1.0.0`
* postprocessing_dataset_docker_image_path: Post-processing docker image tar archive path in DDI
  * default: `project/proj2bdfd9ccf5a78c3ec68ee9e1d90d2c1c/263a6916-f506-11eb-8bc2-0050568fc9b5`
* postprocessing_dataset_ncl_script_path: Post-processing NCL script dataset path in DDI
  * default: project/proj2bdfd9ccf5a78c3ec68ee9e1d90d2c1c/6fb84668-f50a-11eb-8bc2-0050568fc9b5
* postprocessing_ddi_project_path: Path of the project where to transfer the post-processing results in DDI
  * default: `project/proj2bdfd9ccf5a78c3ec68ee9e1d90d2c1c`
* postprocessing_dataset_id_adms_urban_app: ID of the dataset containing the ADMSUrban.exe and corresponding files. The DDI dataset has to contain single file called adms_urban.zip
  * default: `f284db6c-2588-11eb-bbae-0050568fcecc`
* postprocessing_dataset_id_adms_urban_static_data: ID of the dataset containing the static data for ADMSUrban
  * default: `f1275722-25b5-11eb-bbae-0050568fcecc`
* postprocessing_dataset_id_adms_industrial_app: ID of the dataset containing the ADMSIndustrial.exe and corresponding files. The DDI dataset has to contain single file called adms_industrial.zip
  * default: `ab773490-544a-11eb-b72c-0050568fcecc`
* `postprocessing_dataset_id_adms_industrial_static_data`: ID of the dataset containing the static data for ADMSIndustrial
  * default: `b6e09a96-25ac-11eb-bbae-0050568fcecc`

### ADMS post-processing template ouput attributes

The following output attribute is provided:
* attribute `destination_path` of component `HPCToDDIJob`: DDI path to ADMS WRF results
* attribute `destination_path` of component `METResultsToDDIJob`: the path to ADMS MET results in DDI
* attribute `dataset_id_result` of component `ADMS`: the ID of the DDI dataset where ADMS post-process results are stored

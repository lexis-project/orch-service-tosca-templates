# Application Template sample

Example of template of a generic LEXIS workflow implementation performing:
* the transfer of an input dataset from DDI to a Cloud Staging Area
* the preprocessing of these data, running a docker container on a cloud compute instance created on demand
* the transfer of preprocessing results to a HEAppE job that will perform a computation on a HPC cluster
* the transfer of HPC computation results to DDI
* the transfer of HPC computation results to the cloud compute instance local storage
* the postprocessing of these computation results, running a postprocessing docker container
* the transfer of postprocessing results from the cloud instance local storage to the Cloud Staging Area
* the transfer of postprocessing results from the Cloud Staging Area to DDI

A graphical view of the template topology shows:

![App template](images/apptemplate.png)

This application template is providing a `Run` workflow, which is by convention in LEXIS,
the workflow that will be executed by LEXIS Portal.

A graphical view of this workflow shows:

![Run workflow](images/runworkflow.png)

Zooming on each sequence of this workflow, it first starts by creating a cloud
compute instance, and transferring an input dataset from DDI to make it available to this cloud compute instance:

![Run workflow](images/workflow1_mount_input_dataset.png)


This TOSCA application template is using TOSCA components provided by the Yorc 
HEAppE plugin (components of type org.heappe.*).
It is also using Docker and container components provided by the Ystia forge at
https://github.com/ystia/forge/tree/develop/org/ystia/docker

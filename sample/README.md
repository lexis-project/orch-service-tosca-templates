# LEXIS Template

Template of a generic LEXIS workflow, performing:
* the transfer of an input dataset from DDI to a Cloud Staging Area
* the pre-processing of these data, running a docker container on a cloud compute instance created on demand
* the transfer of pre-processing results to a HEAppE job that will perform a computation on a HPC cluster
* the transfer of HPC computation results to DDI
* the transfer of HPC computation results to the cloud compute instance local storage
* the post-processing of these computation results, running a post-processing docker container
* the transfer of post-processing results from the cloud instance local storage to the Cloud Staging Area
* the transfer of post-processing results from the Cloud Staging Area to DDI

See TOSCA code in [lexis_template.yaml](lexis_template.yaml).

A graphical view of the template topology shows:
* a Compute Instance hosting software that will perform the pre-processing and
  post-processing computation
* DDI jobs that will perform the necessary data transfers between the infrastructures
* a HPC Job that will perform the computation on the HPC infrastructure 
* Dynamic orchestration components computing the best infrastructure to use

![App template](images/apptemplate.png)

This application template is providing a `Run` workflow, which is by convention in LEXIS,
the workflow that will be executed by LEXIS Portal.

A graphical view of this workflow shows:

![Run workflow](images/runworkflow.png)

Zooming on each sequence of this workflow, it first starts by gathering info on the
input dataset available in DDI: its size, in which locations it is available (LRZ, IT4I, or both locations),
needed to evaluate the cost of a data transfer.
Then, submits the job `FindCloudLocationJob` seen above in the template topology,
that will compute the best Cloud location taking into account:
* info on this input dataset to transfer to a Cloud staging area
* the requirements of the Cloud Compute instance associated to the component FindCloudLocationJob
* the availability of Computing resources on the different LEXIS Cloud locations.

![Run workflow](images/find_cloud_location.png)


Then, the workflow creates a Cloud compute instance on the selected location, and transfers
the input dataset from DDI to make it available to this cloud compute instance:

![Run workflow](images/workflow1_mount_input_dataset.png)

Then the docker service is installed and started, and the pre-processing container is run:

![Docker and container](images/workflow2_preprocessing.png)

Once the container has run and produced results, a component `GetPreprocessDatasetInfo` is
started to provide details on these pre-processing results (size, number of files...),
needed to evaluate the cost of a data transfer.
And the job `FindHPCLocationJob` is submitted to find the best HPC location where to
run next HPC computation job:

![Find HPC location](images/find_hpc_location.png)


Then, a HEAppE job is first created on the selected HPC location, and File transfers
are then enabled on it, so that the next step can copy pre-processing results to
the HEAppE job task.
The orchestrator submits then the HEAppE job and waits for its end.

![HEAppE job](images/workflow3_computation.png)

Once the HEAppE job has been executed, two branches of the workflow are executed in parallel:
* the transfer of HPC job task results to DDI
* the transfer of HPC job task results to the compute instance for post-processing

![HPC results](images/workflow4_hpc_results_transfer.png)

The post-processing container is then run, its results are copied to the Cloud
Staging Area, then staged to DDI:

![post-processing](images/workflow5_postprocessing.png)

The computation is now done, the final phase is a cleanup phase where infrastructure
resources that were allocated for the computation are now released.
Two branches run in parallel on the workflow:
* the branch excuted after the transfer of HPC job results, taking care of deleting the job
* the branch executed after the post-processing, taking care of cleaning up the Cloud Staging area
  and deleting Cloud compute resources.

![cleanup](images/workflow6_cleanup.png)

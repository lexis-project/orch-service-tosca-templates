# Application templates

<a href="https://doi.org/10.5281/zenodo.6080490"><img src="https://zenodo.org/badge/DOI/10.5281/zenodo.6080490.svg" alt="DOI"></a>

Repository of TOSCA components and Application Templates for LEXIS.

## Acknowledgement
This code repository is a result / contains results of the LEXIS project. The project has received funding from the European Union’s Horizon 2020 Research and Innovation programme (2014-2020) under grant agreement No. 825532.

## Contents
* Application templates:
  * Weather and climate:
    * [RISICO](weather-climate/applications/risico/) - Risks of wildlands fires simulations
    * [Continuum](weather-climate/applications/continuum/) - Hydrology simulations
    * [WRF GFS computation over Italy](weather-climate/applications/italy_wrf_gfs/) - similar to Continnum, with just the pre-processing and WRF computation on HPC
    * [ADMS](weather-climate/applications/adms/) - Air quality
    * [Agriculture](weather-climate/applications/agriculture/) - Agricultural impact models
  * Computational Fluid Dynamics:
    * [OpenFOAM](computational-fluid-dynamics/applications/openfoam) workflow
  * Remote visualization:
    * [Xpra](visualization/applications/xpra) - Remote visualization on cloud compute instance with [Xpra](https://xpra.org/)
    * [Xpra service](visualization/applications/service_xpra) - Service providing remote visualization on cloud compute instance with [Xpra](https://xpra.org/), until the user decides to delete the workflow execution
* Examples of generic templates:
  * [LEXIS template](examples/applications/cloudHPCComputation/) - Generic LEXIS application template with:
    * a pre-processing container executed on a Cloud Compute Instance
    * a computation performed on HPC using [HEAppE](https://heappe.eu)
    * data transfers using [LEXIS Data Transfer Infrastructure](https://lexis-project.eu/web/lexis-platform/data-management-layer/) APIs
  * [Cloud Computation running a public Docker container](examples/applications/cloudComputationPublicContainer/) performing:
    * the transfer of a input dataset from DDI
    * a computation done by a Docker Container using these inputs
    * the transfer of result files produced by this container to DDI
  * [Cloud Computation running a private Docker container archive in DDI](examples/applications/cloudComputationPrivateContainer/) performing:
    * the transfer of a input dataset from DDI
    * the transfer of a docker image archive from DDI
    * the docker load of this archive
    * a computation done by a Docker Container using these inputs
    * the transfer of result files produced by this container to DDI
  * [Cloud Computation running a user-defined script](examples/applications/cloudComputation/) performing:
    * the transfer of a input dataset from DDI
    * a computation done by a user-defined script
    * the transfer of result files produced by this script to DDI
  * [HPC Computation using HEAppE](examples/applications/hpcComputation/) performing:
    * the creation of a [HEAppE](https://heappe.eu) job on a HPC cluster
    * the transfer of a input dataset from DDI to this HEAppE job
    * the submission and monitoring of this HEAppE job until it ends
    * the transfer of result files produced by this HEAppE job to DDI
  * [HPC Computation with failover using HEAppE](examples/applications/hpcComputationFailover/) performing:
    * same as above, with the ability to store in DDI checkpoint files produced by the HEAppE during its execution, and failover to another HPC location in case of failure.
  * [Service provided by a public Docker container on a Cloud instance](examples/applications/cloudServicePublicContainer/) performing:
    * the transfer of a input dataset from DDI
    * running in detached mode a Docker container, until the user decides to delete the workflow execution
  * [Service provided by a private Docker container archive in DDI](examples/applications/cloudServicePrivateContainer/) performing:
    * the transfer of a input dataset from DDI
    * the transfer of a docker image archive from DDI
    * running in detached mode the Docker container using this image, until the user decides to delete the workflow execution

# Application templates

Repository of TOSCA components and Application Templates.

## Contents
* Application templates:
  * Weather and climate:
    * [RISICO](weather-climate/applications/risico/) - Risks of wildlands fires simulations
    * [Continuum](weather-climate/applications/continuum/) - Hydrology simulations
    * [ADMS](weather-climate/applications/adms/) - Air quality
    * [Agriculture](weather-climate/applications/agriculture/) - Agricultural impact models
  * Computational Fluid Dynamics:
    * [OpenFOAM](computational-fluid-dynamics/applications/openfoam) workflow
  * Remote visualization:
    * [Xpra](visualization/applications/xpra) Remote visualization on cloud compute instance with [Xpra](https://xpra.org/)
* Examples of generic templates:
  * [LEXIS template](examples/applications/cloudHPCComputation/): generic LEXIS application template with:
    * a pre-processing container executed on a Cloud Compute Instance
    * a computation performed on HPC using [HEAppE](https://heappe.eu)
    * data transfers using [LEXIS Data Transfer Infrastructure](https://lexis-project.eu/web/lexis-platform/data-management-layer/) APIs
  * [Cloud Computation using a public Docker container](examples/applications/cloudComputationPublicContainer/) performing:
    * the transfer of a input dataset from DDI
    * a computation done by a Docker Container using these inputs
    * the transfer of result files produced by this container to DDI
  * [HPC Computation using HEAppE](examples/applications/hpcComputation/) performing:
    * the creation of a [HEAppE](https://heappe.eu) job on a HPC cluster
    * the transfer of a input dataset from DDI to this HEAppE job
    * the submission and monitoring of this HEAppE job until it ends
    * the transfer of result files produced by this HEAppE job to DDI

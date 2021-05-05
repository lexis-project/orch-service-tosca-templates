# Application templates

Repository of TOSCA components and Application Templates.

## Contents
* [LEXIS template](sample/): generic LEXIS application template with:
  * a pre-processing container executed on a Cloud Compute Instance
  * a computation performed on HPC using [HEAppE](https://heappe.eu)
  * data transfers using [LEXIS Data Transfer Infrastructure](https://lexis-project.eu/web/lexis-platform/data-management-layer/) APIs
* Application templates:
  * Weather and climate:
    * [RISICO](weather-climate/applications/risico/) - Risks of wildlands fires simulations
    * [Continuum](weather-climate/applications/continuum/) - Hydrology simulations
    * [ADMS](weather-climate/applications/adms/) - Agricultural impact models
  * Computational Fluid Dynamics:
    * [OpenFOAM](computational-fluid-dynamics/applications/openfoam) workflow
  * Remote visualization:
    * [Xpra](visualization/applications/xpra) Remove visualization on cloud compute instance with [Xpra](https://xpra.org/)

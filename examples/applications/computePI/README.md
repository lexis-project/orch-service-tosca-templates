# Example Template computing PI to a given decimal

Template of LEXIS workflow computing PI.

The Run workflow for this template is executing the following steps:
* asking the Dynamic Allocation Module (DAM) to select the best Cloud infrastructure
* creating a Cloud Compute instance
* running the PI computation to the given decimal on thsi compute instance
* finally, the the cloud compute instance is released.

### Input properties

The template expects the following madatory input properties:
*  **token**: OpenID Connect access token
* **project_id**: LEXIS project identifier
* **preprocessing_decimalsNumber**: Number of decimals to compute

### Ouput attribute

The following output attribute is provided:
* attribute `result` of component `ComputePI`: the value of PI to the given decimal


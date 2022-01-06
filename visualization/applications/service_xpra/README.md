# Service Visualization Template

Template of a LEXIS workflow allowing to transfer a dataset from DDI to a Cloud
Compute instance on which [ParaView](https://www.paraview.org/) is accessible through a [Xpra](https://xpra.org/) remote session,
until the workflow execution is deleted by the user.

The Run workflow is doing:
* the transfer of an input dataset from DDI to a Cloud Staging Area
* the allocation of a Cloud Compute instance
* the SSHFS mount of the staging area on this compute instance
* the copy of data on this cloud staging area locally on the compute instance
* the installation and run of [Xpra](https://xpra.org/) remote display along with [ParaView](https://www.paraview.org/)

The service remote session will then be available, until the user decides to delete the workflow execution.

## Input properties

The template expects the following input properties (mandatory inputs in **bold**):
*  **token**: OpenID Connect access token
* **project_id**: LEXIS project identifier
* **visualization_dataset_path_input_path**: Dataset path in DDI containing visualization data
* visualization_decrypt_input: Should the input dataset be decrypted (default: false)
* visualization_uncompress_input: Should the input dataset be uncompressed (default: false)
* visualization_directory: Directory where visualization data will be accesible on a cloud instance (default: visualization)
* visualization_mount_point: Directory where visualization data will be mounted from Cloud staging area (default: /mnt/visualization)
* visualization_port: Port to use to expose the remote display, should be > 1024 (default: 8080)

## Ouput attribute

The following output attribute is provided:
* attribute `url` of component `XpraService`: the URL of the remote visualization session

# Access to the remote session

Once the `XpraService` component us started, the remote session URL is available in the Application outputs in Alien4Cloud.
Click on it and you will get an access to the remote session with Paraview running.
Select `File`> `Open` in Paraview, and select the data to visualize in the home directory `visualization` (by default).
Click on `Apply` in the `Properties` pane on the left hand side to visualize you data:

![Paraview](../xpra/images/Paraview.png)

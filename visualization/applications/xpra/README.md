# Visualization Template

Template of a LEXIS workflow allowing to transfer a dataset from DDI to a Cloud
Compute instance on which [ParaView](https://www.paraview.org/) is accessible through a [Xpra](https://xpra.org/) remote session:

The Run workflow is doing:
* the transfer of an input dataset from DDI to a Cloud Staging Area
* the allocation of a Cloud Compute instance
* the SSHFS mount of the staging area on this compute instance
* the copy of data on this cloud staging area locally on the compute instance
* the installation and run of [Xpra](https://xpra.org/) remote display along with [ParaView](https://www.paraview.org/)
* the cleanup of resources once the session has expired or was closed by the user

## Input properties

The template expects the following input properties (mandatory inputs in **bold**):
*  **token**: OpenID Connect access token
* **project_id**: LEXIS project identifier
* **visualization_dataset_path_input_path**: Dataset path in DDI containing visualization data
* **visualization_walltime_minutes**: Duration in minutes of the visualization session
* visualization_decrypt_input: Should the input dataset be decrypted (default: false)
* visualization_uncompress_input: Should the input dataset be uncompressed (default: false)
* visualization_directory: Directory where visualization data will be accesible on a cloud instance (default: visualization)
* visualization_mount_point: Directory where visualization data will be mounted from Cloud staging area (default: /mnt/visualization)
* visualization_ca_pem: PEM-encoded certificate authority content. Will be generated if not provided,
but the user will get a warning that he attempts to connect to a server with an invalid certificate authority (as unknown certificate issuer)
* visualization_ca_key: Certificate authority private key content, will be generated if not provided
* visualization_ca_passphrase: Certificate authority private key passphrase
* visualization_port: Port to use to expose the remote display, should be > 1024 (default: 8080)

## Ouput attribute

The following output attribute is provided:
* attribute `url` of component `XpraJob`: the URL of the remote visualization session

# Access to the remote session

Once the `XpraJob` job is running, the remote session URL is available in the Application outputs in Alien4Cloud.
Click on it and you will get an access to the remote session with Paraview running.
Select `File`> `Open` in Paraview, and select the data to visualize in the home directory `visualization` (by default).
Click on `Apply` in the `Properties` pane on the left hand side to visualize you data:

![Paraview](images/Paraview.png)

## Ending the workflow

The remote display session will automatically be stopped atfer the duration 
provided in input property **visualization_walltime_minutes** is elapsed.

But the use can end the session himself clicking on the top left menu of Xpra
and selecting `Server` > `Shutdown Server` and the workflow will then continue with a cleanup step
to release the Cloud compute instance:

![Xpra menu](images/Xpra_menu.png)

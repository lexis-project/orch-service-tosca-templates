# Description of a workflow running several jobs

The RISICO workflow is a hybrid Cloud/HPC workflow that will be used below as an example to describe the structure of a workflow.

This workflow has a preprocessing step run on a cloud instance that will produce
results for 3 dates: a given day D, the previous day D - 1, and the day before D - 2.

One HEAppE job will have to be run for each of these days.
Then a post-processing step will be run taking in input the results of the 3 HEAppE jobs.

The TOSCA application template for RISICO is available at https://github.com/lexis-project/application-templates/blob/master/weather-climate/applications/risico/risico_template.yaml 

It is made of the following sections described in details below:

* [imports](#imports)
* [topology template](#topology_template)
  * [inputs](#inputs)
  * [node templates](#node_templates)
  * [outputs](#outputs)
  * [workflows](#workflows)

Snippets for each section:

```yaml
# Section medata provides the name and version of the template
metadata:
  template_name: RisicoTemplate
  template_version: 0.1.0-SNAPSHOT
  template_author: lexis

description: RISICO template

# Section imports declare which types to import from Alien4Cloud catalog
# so that they can be instantiated in our template
imports:
  - yorc-types:1.1.0
  - heappe-types:1.0.3

# Section topology_template describe the application template:
# input parameters, components and relationships, outputs, workflows
topology_template:
  # Input parameters provided by the user and referenced in node templates below
  inputs:
    token:
      type: string
      required: true
      description: "Access token"
    ...
  # Description of components and relationships between these components
  node_templates:
    # Here a HEAppE job referencing in its properties the token input parameter
    WRF_DAY_1:
      type: org.heappe.nodes.Job
      metadata:
        task: computation
      properties:
        token: { get_input: token }
        JobSpecification:
          Name: WRFJob
          ...
  # Outputs: values of attributes exposed by components described above
  outputs:
    ddi_post_process_results:
      description: DDI path to RISICO post-processing results
      value: { get_attribute: [ CloudToDDIJob, destination_path ] }
    ddi_wrf_results:
      description: DDI path to RISICO WRF results
      value: { get_attribute: [ CloudToDDIWRFJob, destination_path ] }
  # Workflows: sequences of operations on components described above
  workflows:
    Run:
      steps:
        WRF_DAY_1_create:
          target: WRF_DAY_1
          operation_host: ORCHESTRATOR
          activities:
            - call_operation: Standard.create
          on_success:
            - WRF_DAY_1_enable_file_transfer
        ...
```

<a name="imports"></a>
## Section imports

This section allows to import archives from the Alien4Cloud catalog, to add data types and node types definitions that will be used to build the application template.

For example, this import:
```yaml
imports:
  - heappe-types:1.0.3
```

will import from Alien4Cloud the definition of HEAppE data types and node types
that can be found in this TOSCA file: https://github.com/lexis-project/yorc-heappe-plugin/blob/master/src/a4c/heappe-types-a4c.yaml

This file provides definitions of data types and node types needed for HEAppE.
For example a data type `org.heappe.types.JobSpecification` :

```yaml
data_types:
  org.heappe.types.JobSpecification:
    derived_from: tosca.datatypes.Root
    properties:
      Name:
        description: Job name
        type: string
        required: true
      Project:
        description: Accounting project
        type: string
        required: true
      ClusterId :
        description: Cluster ID
        type: integer
        required: true
      Tasks :
        description: Tasks (at leat one task needs to be defined)
        type: list
        entry_schema:
          type: org.heappe.types.TaskSpecification
        required: true
      ...
```

and a node type using this data type as a property:

```yaml
node_types:
  org.heappe.nodes.pub.Job:
    derived_from: tosca.nodes.Root
    abstract: true
    description: >
      HEAppE Job
    # Properties having static values
    properties:
      token:
        description: Access token
        type: string
        required: false
      JobSpecification:
        description: Specification of the job to create
        type: org.heappe.types.JobSpecification
        required: true
    # Attributes, which will take value at runtime.
    attributes:
      job_id:
        type: string
        description: >
          ID of the HEAppE job created
      file_transfer:
        type: org.heappe.types.FileTransfer
        description: >
          File transfer settings
      changed_files:
        type: list
        description: List of files created or changed by the job execution
      tasks_name_id:
        type: map
        description: Map of task name - task ID
    # A capability (which feature this job provides), that other components
    # requiring to be associated to a job, will use as a requirement
    capabilities:
      heappejob:
        type: org.heappe.capabilities.HeappeJob
    # Operations implemented by this component:
    interfaces:
      Standard:
        create:
          ...
        delete:
          ...
      custom:
        enable_file_transfer:
          ...
        disable_file_transfer:
          ...
        list_changed_files:
          ...
      tosca.interfaces.node.lifecycle.Runnable:
        submit:
          ...
        run:
          ...
        cancel:
          ...
```

So here the node type declares :
* properties (token and JobSpecification) whose value are static and must be provided before the deployment
* attributes, whose values are set by the orchestrator at runtime, for example job_id will be set once the operation create has been called
* a capability, ie. a feature provided by this component, here we describe this component is a HEAppE Job, and each component requiring to be associated to a HEAppE job will have to declare in its section `requirements` that it needs to be associated with a component having this capability `org.heappe.capabilities.HeappeJob` described later in the file
* interfaces, ie. operations supported by this component:
  * the section `Standard` describe standard operations defined in the TOSCA specification, here the component supports `create` and `delete`, other standard operations that can be implemented are `start` and `stop`.
  * the section `custom` describe any specific operations the developper needs to defined, here we define operations `enable_file_transfer` and `disable_file_transfer` to enable/disable the ability to transfer files to the job, and `list_changed_files` to list the files that changed during a job execution. When this `list_changed_files` is called, the attribute `changed_files` described above will be set by the orchestrator.
  * the section `tosca.interfaces.node.lifecycle.Runnable` describes an extension to TOSCA that Alien4Cloud/Yorc have defined to support jobs:
    * `submit` to submit a job
    * `run` to monitor a job execution until the job ends
    * `cancel` to cancel a job execution.


The description of these data types and node types will be imported in our template at 
https://github.com/lexis-project/application-templates/blob/master/weather-climate/applications/risico/risico_template.yaml 
thanks to these lines in the import section:

```yaml
# Section imports declare which types to import from Alien4Cloud catalog
# so that they can be instantiated in our template
imports:
  - heappe-types:1.0.3
```

<a name="topology_template"></a>
## Section topology_template

This section describes input parameters, components and relationships, outputs,
and workflows of the application

<a name="inputs"></a>
### subsection inputs

In this subsection you declare input parameters that a user will provide, specifying which input parameters are required and which are not required with a default value that the user can override if needed.

Here is the description on an input parameter `token` marked as required,
so the user will have to provide a value to this input parameter before being able to deploy the application:

```bash
topology_template:
  # Input parameters provided by the user and referenced in node templates below
  inputs:
    token:
      type: string
      required: true
      description: "Access token"
```

These input parameters can be referenced in the next section node_templates in
propertied of node templates, using the TOSCA function `get_input` like below:

```yaml
    WRF_DAY_1:
      type: org.heappe.nodes.Job
      properties:
        token: { get_input: token }
```

<a name="node_templates"></a>
### subsection node_templates

This subsection describes components and relationships between this component.

The Alien4Cloud UI represents this subsection this way:

![App template](images/risico_app.png)

Here the description of a HEappE job:

```yaml
  node_templates:
    # Here a HEAppE job referencing in its properties the token input parameter
    WRF_DAY_1:
      type: org.heappe.nodes.Job
      metadata:
        task: computation
      properties:
        token: { get_input: token }
        JobSpecification:
          Name: WRFJob
          Tasks:
            - Name: WRFTask
              TemplateParameterValues:
                - CommandParameterIdentifier: MPICores
                  ParameterValue: "48"
          ...
```

Then another component having a relationship with this job is described.
This component will copy data to the previous Job task directory.
This relationhip is expressed in the section requirements of the component
description.
Here we see the component requires to be:
* hosted on a Host (the component RisicoVM described before in the file),
* associated to job WRF_DAY_1

```yaml
    CopyDay1DataToJobTask:
      type: org.lexis.datatransfer.nodes.CopySubDirToJobTask
      properties:
        task_name: WRFTask
        parent_directory: /wps_data/output
        subdirectory_index: 0
      requirements:
        - hostedOnVirtualMachineHost:
            type_requirement: host
            node: RisicoVM
            capability: tosca.capabilities.Container
            relationship: tosca.relationships.HostedOn
        - job:
            type_requirement: job
            node: WRF_DAY_1
            capability: org.heappe.capabilities.HeappeJob
            relationship: org.heappe.relationships.SendInputsToJob
```

These requirements are expressed in the type `org.lexis.datatransfer.nodes.CopySubDirToJobTask`
described at https://github.com/lexis-project/application-templates/blob/master/common/datatransfer/types.yaml :

```yaml
  org.lexis.datatransfer.nodes.CopyFromJobTask:
    derived_from: tosca.nodes.SoftwareComponent
    ...
    requirements:
      - job:
          capability: org.heappe.capabilities.HeappeJob
          node: org.heappe.nodes.Job
          relationship: org.heappe.relationships.GetResultsFromJob
          occurrences: [1, 1]
```

We see above that the type describes explicitly the requirement to be associated to a component
with the capability `org.heappe.capabilities.HeappeJob`,
and our component `WRF_DAY_1` of type `org.heappe.nodes.Job` declares this capability,
as described at https://github.com/lexis-project/yorc-heappe-plugin/blob/master/tosca/heappe-types.yaml :

```yaml
node_types:
  org.heappe.nodes.pub.Job:
  ...
    capabilities:
      heappejob:
        type: org.heappe.capabilities.HeappeJob  
  ...
```

An additional requirement needed by the component `CopyDay1DataToJobTask` is that it needs
to be associated to a host.
This requirement comes from the fact that our component is of type `org.lexis.datatransfer.nodes.CopySubDirToJobTask` whose declaration shows this type inherits from a type `tosca.nodes.SoftwareComponent` as can be seen at https://github.com/lexis-project/application-templates/blob/master/common/datatransfer/types.yaml :

```yaml
  org.lexis.datatransfer.nodes.CopyFromJobTask:
    derived_from: tosca.nodes.SoftwareComponent
    ...
```

This TOSCA type `tosca.nodes.SoftwareComponent` is defined by the TOSCA specification, and the orchestrator provides an implementation of this type at https://github.com/ystia/yorc/blob/develop/data/tosca/normative-types.yml :

```yaml
  tosca.nodes.SoftwareComponent:
    derived_from: tosca.nodes.Root
    ...
    requirements:
      - host:
          capability: tosca.capabilities.Container
          node: tosca.nodes.Compute
          relationship: tosca.relationships.HostedOn
```

<a name="outputs"></a>
### subsection outputs

The subection `outputs` references attributes of components described in the section `node_templates`.
The UI will display these outputs.

Here for this application, these are result datasets paths in DDI.

```yaml
  outputs:
    computation_dataset_wrf_result_path:
      description: DDI path to RISICO WRF results
      value: { get_attribute: [ CloudToDDIWRFJob, destination_path ] }
    postprocessing_dataset_result_path:
      description: DDI path to RISICO post-processing results
      value: { get_attribute: [ CloudToDDIJob, destination_path ] }
```

<a name="workflows"></a>
### subsection workflows

The subsection `workflows` describes workflows: sequences of operations on the components described 
in subsection `node_templates`.

The Alien4Cloud UI represents such a workflow this way:

![Workflow ](images/risico_preprocessing.png)

The TOSCA specification describes standard lifecycle operations that a component can implement (it doesn' have to implement all of them if not needed):

* create,
* configure,
* start,
* stop,
* delete.

In addition, Ystia is intorducing lifecyle operations for jobs:

* submit,
* run (ie. monitor a job submitted or running, untils the job ends),
* cancel.

Then any custom operation can be defined by the component developper.
For example, in the case of a HEAppE job, these additional operations are declared in 
https://github.com/lexis-project/yorc-heappe-plugin/blob/master/tosca/heappe-types.yaml :

```yaml
    interfaces:
      ...
      custom:
        enable_file_transfer:
        ...
        disable_file_transfer:
        ...
        list_changed_files:
        ...
```

* enable_file_transfer: allows to perform file transfers to/from the job,
* disable_file_transfer: diables the ability to perform file transfers to/from the job,
* list_changed_files: list all the files that were changed/created during the job execution.

All these sequences of operations will be defined in a workflow.

The following lifecycle workflow can be defined:
* install,
* uninstall.

These lifecycle workflows will be called automatically by the Orchestrator when the application is deployed/undeployed.

Then, the developper can then define any other workflow for his needs.
By convention in LEXIS, the LEXIS Portal will call a workflow named `Run` to start the LEXIS workflow execution.

We see below an excerpt of the workflow dealing with the components we have described above `WRF_DAY_1` and `CopyDay1DataToJobTask`.

The job must first be created, then as the job needs input files to be provided,
the workflow first needs to call the operation `enable_file_transfer` for this job,
and then, we will be able to copy files to the job task, and then we will submit the job.
Then we will cann the run operation.
For jobs, the orchestrator takes care of running the run operation periodically
until the job is done. In which case the operation run is considered as completed,
and the workflow can go on.
Here will we will just change the state of the job to describe it is now in the stated executed.

Which gives this workflow:

```yaml
  workflows:
  ...
  Run:
      steps:
        ...
        # The step named WRF_DAY_1_create create the job:
        # - target is the component descirbed in subestion node_templates above.
        # - operation_host is the host where to execute thos operation. For HEappE jobs,
        #   the host where to execute the operation is the orchestrator host
        #    as the orchestrator takes care of executing a HEAppE REST API request
        # - activities describe which component operation to call, here the standard operation create
        # - on_sucess describes the steps that have to be performed when the operation is successull
        #   here the next step is WRF_DAY_1_enable_file_transfer
        # (you can define as well "on_failure" to describe which steps to execute on failure,
        #  here as no on_failure is specified, in case of operation Standard.create failure,
        # the workflow will just stop here and report the failure)
        WRF_DAY_1_create:
          target: WRF_DAY_1
          operation_host: ORCHESTRATOR
          activities:
            - call_operation: Standard.create
          on_success:
            - WRF_DAY_1_enable_file_transfer
        # Enable file transfers for this job
        WRF_DAY_1_enable_file_transfer:
          target: WRF_DAY_1
          operation_host: ORCHESTRATOR
          activities:
            - call_operation: custom.enable_file_transfer
          on_success:
            - CopyDay1ToJobTask_start
        # Copy input files to this job, ie. run the operation start of 
        # compnent CopyDay1DataToJobTask
        # Here,
        # - target is not the job, but the component CopyDay1DataToJobTask
        # - operation_host is not specified, then it takes the default value TARGET applies,
        #   which means the operation will be executed on the host hosting CopyDay1DataToJobTask,
        #   which is according to the requirement "hostedOnVirtualMachineHost" of CopyDay1DataToJobTask
        #   described in the subsection node_templates, the compute instance component named RisicoVM.
        CopyDay1ToJobTask_start:
          target: CopyDay1DataToJobTask
          activities:
            - call_operation: Standard.start
          on_success:
            - CopyDay1ToJobTask_started
        # Then, once the operation is done, we just update the state of the component
        # to started, using the TOSCA operation set_state this time, and not call_operation
        # like we used above to call a given component operation
        CopyDay1ToJobTask_started:
          target: CopyDay1DataToJobTask
          activities:
            - set_state: started
          on_success:
            - WRF_DAY_1_submit
        # Now that input files were copied, we can submit the job
        WRF_DAY_1_submit:
          target: WRF_DAY_1
          operation_host: ORCHESTRATOR
          activities:
            - call_operation: tosca.interfaces.node.lifecycle.Runnable.submit
          on_success:
            - WRF_DAY_1_submitted
        # The job being submitted, we can change its state
        WRF_DAY_1_submitted:
          target: WRF_DAY_1
          activities:
            - set_state: submitted
          on_success:
            - WRF_DAY_1_run
        # A job operation run is called periodically be the orchestrator to check
        # the job status until the job ends on success or on failure.
        WRF_DAY_1_run:
          target: WRF_DAY_1
          operation_host: ORCHESTRATOR
          activities:
            - call_operation: tosca.interfaces.node.lifecycle.Runnable.run
          on_success:
            - WRF_DAY_1_executed
        # Finally we chnage the state of component WRF_DAY_1 to executed.
        WRF_DAY_1_executed:
          target: WRF_DAY_1
          activities:
            - set_state: executed
```



Go to **Settings > Mail Reply Configurations** and create records according to your needs.

For each record:

- **Model**: Choose a model (required).
- **Parent Field**: Select the field for the parent field ID (e.g., if you select the model as project.task, choose project_id as the parent field). If a parent field is selected, the system will update the reply stage based on the parent (e.g., tasks under the project will use the reply stage of the matched configuration). If this field is left empty, all records without a matching configuration for their project will use the configuration record that does not specify a parent field.
- **Parent Model**: The system will assign this automatically.
- **Parent Field Value**: Set up the name of the parent record (e.g., project name).
- **Parent Stage Field**: Choose the stages field from the parent model to verify that the reply stage is within the parent stages.
- **Reply Stage Field**: Choose the field for the stage that will be automatically updated when a non-internal user sends an update.(required)
- **Reply Stage**: Set the stage value that will be updated.(required)
- **No Reply Stage**: Set the stage value. If the record is in this state, updates from the user will not change the stage of the record.(required)

from galaxy.jobs.mapper import JobMappingException
DEFAULT_ROLE = 'have_license'

def is_user_in_role(user, app, tool):
    # user is a galaxy.model.User object or None
    # app is a galaxy.app.UniverseApplication object
    # tool is a galaxy.tools.Tool object
    if user is None:
        raise JobMappingException('You must login to use this tool!')
    # Determine required_role and final_destination for tool_id tool
    # job_conf.xml syntax:
    # <tool id="tool_id" destination="is_user_in_role" required_role="special_users" final_destination="special_queue"/>
    # Both required_role and final_destination attributes are optional.
    default_destination_id = app.job_config.get_destination(None)
    # Loop across all of the job_tool_configurations which apply to the tool in question
    for jtc in tool.job_tool_configurations:
        # tool.job_tool_configurations is a list of galaxy.jobs.JobToolConfiguration objects
        if not jtc.params:
            # We attempt to extract the required_role and final_destination variables from the <tool> XML element
            required_role = jtc.get('required_role', DEFAULT_ROLE)
            final_destination = jtc.get('final_destination', default_destination_id)
            break
    else:
        required_role = DEFAULT_ROLE
        final_destination = default_destination_id
    # Check that the required_role is in the set of role names associated with the user
    user_roles = user.all_roles() # a list of galaxy.model.Role objects
    user_in_role = required_role in [role.name for role in user_roles]
    if not user_in_role:
        raise JobMappingException("This tool is restricted to users associated with the '%s' role, please contact a site administrator to be authorized!" % required_role)
    else:
        return final_destination

# Plugins

The plugin must follow some conventions

## Basic conventions

1. Must be an pip intalable FastAPI application
2. Plugin name should be prefixed with `openerp_` and suffixed with `_plugin`
3. In the top level of the package, we should be able to import
    - Variables `title`, `description`, `author`, `version`
    - FastAPI app `api_router` which can be mounted in the main app
    - The List of `available_resources`. It will be used by main application for permissions. e.g. `["res_1", "res_2"]`
    - List of requested scopes `data_scopes`. It will determine what data will be available for the plugin

## Advanced conventions

1. These variables will always be available inside `request.state`
    - `user_id` ID of the authenticated user
    - `user_name` Name of the authenticated user
    - `has_permission` function to check if the user has permission
    - `is_superuser` If the user is superuser, if so all permissions will be available
    - `data` Additional data required by the plugin `data_scopes`
2. Permissions
    - For permission, you need to define the resource list first
    - If that resource is not open, `create`, `read`, `update`, `delete` and `all` will be defined automatically
    - If any of the operations are not available, you need to define it as `{'delete': False, 'update': False}`
    - In endpoints, permission needs to be checked to perform the required operation on the resource
    - `has_permission('read', 'res_1')` will return `True` if the user has permission to read `res_1`

**For more information, check example plugin repo**

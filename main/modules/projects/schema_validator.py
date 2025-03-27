from marshmallow import Schema, fields


class AddProjectSchema(Schema):
    """
    Schema to add project to the database.
    """
    project_name = fields.String(required=True)


class UpdateProjectSchema(Schema):
    """
    Schema to update the project.
    """
    project_name = fields.String(required=True)


class AddUserAccessSchema(Schema):
    """
    Schema to add user access for a project.
    """
    email = fields.String(required=True)


class RemoveUserAccessSchema(Schema):
    """
    Schema to add user access for a project.
    """
    access_id = fields.Integer(required=True)

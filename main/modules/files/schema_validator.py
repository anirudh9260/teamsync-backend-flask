from marshmallow import Schema, fields, validates, ValidationError
from marshmallow.validate import OneOf
from main.custom_exceptions import CustomValidationError

class AddFileSchema(Schema):
    """
    Schema to add file to the database.
    """
    file = fields.Raw(type='file', required=True)
    project_id = fields.Integer(required=True)


class AddFileNameSchema(Schema):
    """
    Schema to add file to the database.
    """
    file_name = fields.String(required=True)
    project_id = fields.Integer(required=True)


class UpdateFileSchema(Schema):
    """
    Schema to update the file.
    """
    file_name = fields.String(required=False)
    project_id = fields.Integer(required=False)


class FileConversionSchema(Schema):
    """
    Schema to perform Conversion Operations
    """
    id = fields.Integer(required=True)
    output_file_name = fields.String(required=True)
    from_ext = fields.String(required=True)
    to_ext = fields.String(required=True)


# class DeleteFilesSchema(Schema):
#     """
#     Schema to update the file.
#     """
#     file_ids = fields.Integer(required=True)


class DeleteFilesSchema(Schema):
    file_ids = fields.List(fields.Integer(), required=True)

    @validates('file_ids')
    def validate_length(self, value):
        if len(value) < 1:
            raise CustomValidationError('Quantity must be greater than 0.')
import os
from flask import jsonify, make_response, request
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource
from main.modules.projects.controller import ProjectsController
from main.modules.projects.schema_validator import AddProjectSchema, UpdateProjectSchema,AddUserAccessSchema, RemoveUserAccessSchema
from main.modules.auth.controller import AuthUserController
from main.utils import get_data_from_request_or_raise_validation_error


class ProjectListApi(Resource):
    method_decorators = [jwt_required()]

    def get(self):
        """
        This function is used to get the list of projects.
        :return:
        """
        auth_user = AuthUserController.get_current_auth_user()
        response = ProjectsController.get_projects(auth_user)
        return jsonify(response)

    def post(self):
        """
        This function is used to add new project to the database.
        :return:
        """
        auth_user = AuthUserController.get_current_auth_user()
        data = get_data_from_request_or_raise_validation_error(AddProjectSchema, request.json)
        data.update({"user_id": auth_user.id})
        project_id = ProjectsController.add_project(data)
        response = make_response(
            jsonify({"message": "Project Successfully Added", "id": project_id, "project_name": data["project_name"], "user": auth_user.username}), 201
        )
        response.headers["Location"] = f"/projects/{project_id}"
        return response


class ProjectDetailApi(Resource):
    method_decorators = [jwt_required()]

    @staticmethod
    def get(project_id: int):
        """
        This function is used to get the particular project by project_id
        :param project_id:
        :return:
        """
        auth_user = AuthUserController.get_current_auth_user()
        response = ProjectsController.get_project_by_project_id(project_id, auth_user)
        return jsonify(response)

    @staticmethod
    def put(project_id: int):
        """
        This function is used to update the project by project_id
        :param project_id:
        :return:
        """
        auth_user = AuthUserController.get_current_auth_user()
        data = get_data_from_request_or_raise_validation_error(UpdateProjectSchema, request.json)
        response = ProjectsController.update_project(project_id, data, auth_user)
        return jsonify(response)

    @staticmethod
    def delete(project_id: int):
        """
        This function is used to delete the project by project_id.
        :param project_id:
        :return:
        """
        auth_user = AuthUserController.get_current_auth_user()
        response = ProjectsController.delete_project(project_id, auth_user)
        return jsonify(response)


class ProjectAccessApi(Resource):
    method_decorators = [jwt_required()]

    @staticmethod
    def get(project_id: int):
        """
        This function is used to get the particular project by project_id
        :param project_id:
        :return:
        """
        auth_user = AuthUserController.get_current_auth_user()
        response = ProjectsController.get_users_by_project_id(project_id)
        return jsonify(response)
    

    @staticmethod
    def post(project_id: int):
        """
        This function is used to add new user to the Project Access.
        :return:
        """
        auth_user = AuthUserController.get_current_auth_user()
        data = get_data_from_request_or_raise_validation_error(AddUserAccessSchema, request.json)
        data.update({"project_id": project_id})
        access_id = ProjectsController.add_user_access(data)
        response = make_response(
            jsonify({"message": "User Access added", "access_id": access_id}), 201
        )
        return response
    
    
    @staticmethod
    def delete(project_id: int):
        """
        This function is used to remove a user from Project Access.
        :param project_id:
        :return:
        """
        auth_user = AuthUserController.get_current_auth_user()
        data = get_data_from_request_or_raise_validation_error(RemoveUserAccessSchema, request.json)
        response = ProjectsController.remove_user_access(data)
        return jsonify(response)


project_namespace = Namespace(f'{os.environ.get("BASE_PATH")}/projects', description="Projects Operations")
project_namespace.add_resource(ProjectListApi, "")
project_namespace.add_resource(ProjectDetailApi, "/<int:project_id>")
project_namespace.add_resource(ProjectAccessApi, "/<int:project_id>/access")

from main.db import db
from main.utils import get_query_including_filters
from main.custom_exceptions import EntityNotFoundError, UnauthorizedUserError, EntityAlreadyExistsError, CustomValidationError
from main.modules.projects.model import Projects, ProjectAccess
from main.modules.auth.controller import AuthUserController
from main.modules.user.controller import UserController
from main.modules.auth.model import AuthUser


class ProjectsController:
    """
    This is the controller class which is used to handle all the logical and CURD operations.
    """

    @classmethod
    def add_project(cls, project_data: dict):
        """
        This function is used to add new project.
        :param project_data:
        :return int:
        """
        if cls.get_project_by_project_name(project_data.get("project_name")):
            raise EntityAlreadyExistsError("A project with similar name already exists. Please specify a different name")
        project = Projects.create(project_data)
        return project.id


    @classmethod
    def get_projects(cls, auth_user: AuthUser) -> list[dict]:
        """
        This function is used to get the list of projects of logged-in auth_user. If auth_user is Admin
        then this function will return all projects.
        :param auth_user:
        :return list[Projects]:
        """
        if auth_user.role == AuthUserController.ROLES.ADMIN.value:
            projects = Projects.query.all()
            return [project.serialize() for project in projects]
        else:
            projects = Projects.query.filter_by(user_id=auth_user.id)
            assigned_projects = ProjectAccess.query.filter_by(email = auth_user.email)
            assigned_project_ids = [project.project_id for project in assigned_projects]
            assigned_projects = get_query_including_filters(db, Projects, {"op_in": {"id": assigned_project_ids}})
            # assigned_projects = Projects.query.filter(Projects.id.in_(assigned_project_ids)).all()
        return [project.serialize() for project in projects] + [project.serialize() for project in assigned_projects]


    @classmethod
    def get_project_by_project_id(cls, project_id: int, auth_user: AuthUser) -> dict:
        """
        This function is used to get an project by project_id.
        :param project_id:
        :param auth_user:
        :return dict:
        """
        project = Projects.query.filter_by(id=project_id).first()
        # cls.required_checks(auth_user, project)
        return project.serialize()
    

    @classmethod
    def get_project_by_project_name(cls, project_name: str) -> dict:
        """
        This function is used to get an project by project_name.
        :param project_id:
        :param auth_user:
        :return dict:
        """
        projects = Projects.query.filter_by(project_name=project_name)
        return [project.serialize() for project in projects]
    

    @classmethod
    def update_project(cls, project_id: int, updated_project: dict, auth_user: AuthUser) -> dict:
        """
        This function is used to update the project. It required a valid project_id.
        :param project_id:
        :param updated_project:
        :param auth_user:
        :return dict:
        """
        project = Projects.query.filter_by(id=project_id).first()
        cls.required_checks(auth_user, project)
        project.update(updated_project)
        return {"msg": "success"}


    @classmethod
    def delete_project(cls, project_id, auth_user):
        """
        This function is used to delete a project by project_id.
        :param project_id:
        :param auth_user:
        :return dict:
        """
        project = Projects.query.filter_by(id=project_id).first()
        cls.required_checks(auth_user, project)
        try:
            Projects.delete(id=project_id)
        except:
            raise CustomValidationError("Empty Project Files and User Access before Deleting Project")
        return {"msg": "success"}
    

    @classmethod
    def get_users_by_project_id(cls, project_id: int):
        """
        This function is used to get users with access to project.
        :param project_id:
        :param auth_user:
        :return dict:
        """
        users = ProjectAccess.query.filter_by(project_id=project_id)
        return [user.serialize() for user in users]


    @classmethod
    def add_user_access(cls, data):
        if data.get("email") not in UserController.get_all_users():
            raise EntityNotFoundError("User not found.")
        users = cls.get_users_by_project_id(data.get("project_id"))
        emails = [user.get("email") for user in users]
        if data.get("email") in emails:
            raise EntityAlreadyExistsError("User already has access to project.")
        access = ProjectAccess.create(data)
        return access.id
    

    @classmethod
    def remove_user_access(cls, data):
        ProjectAccess.delete(id=data.get('access_id'))
        return {"message": "Success"}



    @classmethod
    def required_checks(cls, auth_user: AuthUser, project: Projects):
        """
        This function is used to check the required checks and raise a custom exception if any
        check failed. On custom exception server will return a response with defined error msg
        and status code.
        :param auth_user:
        :param project:
        :return:
        """
        if not project:
            raise EntityNotFoundError("Project Not Found!!!")
        if auth_user.role != AuthUserController.ROLES.ADMIN.value and project.user_id != auth_user.id:
            raise UnauthorizedUserError

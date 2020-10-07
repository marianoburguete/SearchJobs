from flask import Flask, jsonify
from flask_restful import Api
from flask_cors import CORS

from app.common.error_handling import ObjectNotFound, AppErrorBaseClass, Forbidden, Unauthorized, BadRequest
from app.database.db import db
from app.resources.usersResources import users_bp
from app.resources.authResources import auth_bp
from app.resources.jobsResources import jobs_bp
from app.resources.interviewsResources import interviews_bp
from .ext import ma, migrate

#MODELOS PARA REGISTRARLOS EN LA BASE
from app.database.UserModel import User
from app.database.CurriculumModel import Curriculum
from app.database.CompanyModel import Company
from app.database.JobModel import Job
from app.database.RequirementModel import Requirement
from app.database.InterviewModel import Interview
from app.database.ApplicationModel import Application
from app.database.MessageModel import Message
from app.database.NotificationModel import Notification
from app.database.RatingModel import Rating

def create_app(settings_module):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(settings_module)


    # Inicializa las extensiones
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    # Captura todos los errores 404
    Api(app, catch_all_404s=True)

    # Deshabilita el modo estricto de acabado de una URL con /
    app.url_map.strict_slashes = False

    # Registra los blueprints
    app.register_blueprint(users_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(jobs_bp)
    app.register_blueprint(interviews_bp)

    # Registra manejadores de errores personalizados
    register_error_handlers(app)

    return app


def register_error_handlers(app):
    @app.errorhandler(Exception)
    def handle_exception_error(e):
        return jsonify({'msg': 'Internal server error',
        'Error': e}), 500

    @app.errorhandler(405)
    def handle_405_error(e):
        return jsonify({'msg': 'Method not allowed'}), 405

    @app.errorhandler(403)
    def handle_403_error(e):
        return jsonify({'msg': 'Forbidden error'}), 403

    @app.errorhandler(404)
    def handle_404_error(e):
        return jsonify({'msg': 'Not Found error'}), 404

    @app.errorhandler(AppErrorBaseClass)
    def handle_app_base_error(e):
        return jsonify({'msg': str(e)}), 500

    @app.errorhandler(ObjectNotFound)
    def handle_object_not_found_error(e):
        return jsonify({'msg': str(e)}), 404

    @app.errorhandler(Forbidden)
    def handle_forbidden_error(e):
        return jsonify({'msg': str(e)}), 403

    @app.errorhandler(Unauthorized)
    def handle_unauthorized_error(e):
        return jsonify({'msg': str(e)}), 401
    
    @app.errorhandler(BadRequest)
    def handle_bad_request_error(e):
        return jsonify({'msg': str(e)}), 400
from flask import request, Blueprint, jsonify, make_response
from flask_restful import Api, Resource
import json
import requests

from ..common.Schemas.JobSchema import JobSchema, JobSearchResultsSchema, JobDetailsSchema, JobsByTitleSchema
from ..common.Schemas.UserSchema import UserByEmailSchema
from ..database.JobModel import Job
from ..database.CompanyModel import Company
from ..database.RequirementModel import Requirement
from ..database.ApplicationModel import Application
from ..database.CategoryModel import Category
from ..database.SubcategoryModel import Subcategory
from ..database.SearchModel import Search
from ..database.CurriculumModel import Curriculum
from ..database.UserModel import User

from ..common.error_handling import ObjectNotFound, BadRequest
from ..common.token_helper import validateToken
from ..common.pagination_helper import makePagResponse

import json
import re

jobs_bp = Blueprint('jobs_bp', __name__)

job_schema = JobSchema()

api = Api(jobs_bp)


class JobR(Resource):
    def get(self, id):
        j = Job.get_by_id(id)
        if j is not None:
            res = {
                'msg': 'Ok',
                'results': JobDetailsSchema().dump(j)
            }
            return make_response(jsonify(res), 200)
        raise ObjectNotFound('No existe un trabajo para el Id dado.')


class JobsSearchR(Resource):
    def post(self):
        data = request.get_json()
        if data is None:
            raise BadRequest('No se encontraron los filtros.')
        pagResult = Job.get_pag(data)
        s = Search(data['search'], None)
        s.save()
        return makePagResponse(pagResult, JobSearchResultsSchema())

class JobsCompany(Resource):
    def post(self):
        data = request.get_json()
        if data is None:
            raise BadRequest('No se encontraron los filtros.')
        pagResult = Job.get_pag_company(data)
        return makePagResponse(pagResult, JobSearchResultsSchema())
        
api.add_resource(JobR, '/api/jobs/<int:id>')
api.add_resource(JobsSearchR, '/api/jobs/search')
api.add_resource(JobsCompany, '/api/jobs/company')


# ADMIN ENDPOINTS


class JobsCompuTrabajoRA(Resource):
    def post(self):
        user_id = validateToken(request, 'funcionario')
        data = request.get_json()
        if 'Scrapy' in request.headers:
            data = json.loads(data)
        activeJobs = []
        for job in data:
            jobExists = Job.search_by_url(job['url'])
            if jobExists is None:
                j = Job(job['url'], job['title'])
                last_id = j.get_id()[0]['setval']
                if last_id is not None:
                    j.id = j.get_id()[0]['setval']+1
                else:
                    j.id = 1
                if job['workday'] == 'Desde Casa':
                    j.location = 'remote'
                    j.workday = 'notspecified'
                else:
                    j.location = job['location']
                    if job['workday'] == 'Tiempo Completo':
                        j.workday = 'fulltime'
                    elif job['workday'] == 'Medio Tiempo':
                        j.workday = 'parttime'
                    else:
                        j.workday = 'notspecified'
                if job['contract_type'] == 'Contrato por tiempo indefinido':
                    j.contract_type = 'undefined'
                elif job['contract_type'] == 'Contrato por tiempo determinado':
                    j.contract_type = 'defined'
                else:
                    j.contract_type = 'other'
                if job['salary'] == 'A convenir':
                    j.salary = None
                    j.salary_max = None
                else:
                    s = int(job['salary'].split()[1].replace(',00', '').replace('.',''))
                    j.salary = s
                    j.salary_max = s
                j.description = job['description']

                category = ''

                if job['category'] == 'Informática / Telecomunicaciones':
                    category = 'programacion/tecnologia'
                elif job['category'] == 'Diseño / Artes gráficas':
                    category = 'diseño/multimedia'
                # la categoria de abajo la tiene mariano solo
                # elif job['category'] == '':
                #     category = 'redaccion/traduccion'
                elif job['category'] == 'Mercadotécnia / Publicidad / Comunicación':
                    category = 'marketing'
                elif job['category'] == 'Contabilidad / Finanzas' or job['category'] == 'Administración / Oficina':
                    category = 'administracion/finanzas'
                elif job['category'] == 'Legal / Asesoría':
                    category = 'legal'
                elif job['category'] == 'Ingeniería':
                    category = 'ingenieria/arquitectura'
                elif job['category'] == 'Producción / Operarios / Manufactura' or job['category'] == 'Mantenimiento y Reparaciones Técnicas':
                    category = 'produccion/operarios'
                elif job['category'] == 'Recursos Humanos':
                    category = 'recursosHumanos'
                elif job['category'] == 'Hostelería / Turismo':
                    category = 'hosteleria/turismo'
                elif job['category'] == 'Ventas' or job['category'] == 'CallCenter / Telemercadeo' or job['category'] == 'Atención a clientes':
                    category = 'ventas'
                elif job['category'] == 'Compras / Comercio Exterior':
                    category = 'compras/comercioExterior'
                elif job['category'] == 'Servicios Generales, Aseo y Seguridad ':
                    category = 'serviciosGenerales'
                elif job['category'] == 'Medicina / Salud':
                    category = 'medicina/salud'
                elif job['category'] == 'Almacén / Logística / Transporte':
                    category = 'almacenamiento/logistica'
                elif job['category'] == 'Construccion y obra':
                    category = 'construccion/obras'
                # No tengo ninguno con educacion, asi que no se como es la etiqueta
                # elif job['category'] == '':
                #     category = 'educacion'
                elif job['category'] == 'Investigación y Calidad':
                    category = 'investigacion/calidad'
                else:
                    category = 'otros'
                
                cat = Category.getByName(category)
                if cat is None:
                    cat = Category(category)
                    cat.save()
                    subCategory = Subcategory('general' + category)
                    cat.subcategories.append(subCategory)
                    cat.save()

                # aca iria todo el chorrete de if para la subcategoria, por ahora lo metemos en general
                j.subcategory_id = Subcategory.getByName('general' + category).id

                for requirement in job['requirements']:
                    r = requirement.split(':')
                    j.requirements.append(Requirement(r[0], r[1]))

                c = Company.get_by_name(job['company_name'])
                if c is not None:
                    c.jobs.append(j)
                    c.save()
                else:
                    c = Company(job['company_name'])
                    last_idc = Company.get_id()[0]['setval']
                    if last_idc is not None:
                        c.id = Company.get_id()[0]['setval']+1
                    else:
                        c.id = 1
                    c.logo = job['company_logo']
                    c.jobs.append(j)
                    c.save()
                activeJobs.append(j.id)
            else:
                activeJobs.append(jobExists.id)
        
        allJobs = Job.get_all_by_url('computrabajo')
        for job in allJobs:
            if job.id in activeJobs:
                pass
            else:
                job.active = False
                job.save()

        return "Ok", 201

class JobsMipleoRA(Resource):
    def post(self):
        user_id = validateToken(request, 'funcionario')
        data = request.get_json()
        if 'Scrapy' in request.headers:
            data = json.loads(data)
        activeJobs = []
        for job in data:
            jobExists = Job.search_by_url(job['url'])
            if jobExists is None:
                j = Job(job['url'], job['title'])
                last_id = j.get_id()[0]['setval']
                if last_id is not None:
                    j.id = j.get_id()[0]['setval']+1
                else:
                    j.id = 1
                j.location = job['location']
                if job['workday'] == 'Tiempo Completo':
                    j.workday = 'FullTime'
                elif job['workday'] == 'Medio Tiempo':
                    j.workday = 'ParTime'
                elif job['workday'] == 'Por Horas':
                    j.workday = 'ParTime'
                elif job['workday'] == 'Tiempo parcial':
                    j.workday = 'ParTime'
                elif job['workday'] == 'A convenir':
                    j.workday = 'NotSpecified'
                if job['contract_type'] == 'Contrato por tiempo indefinido':
                    j.contract_type = 'undefined'
                elif job['contract_type'] == 'Contrato por tiempo determinado':
                    j.contract_type = 'defined'
                elif job['contract_type'] == 'Contrato a Plazo Indeterminado':
                    j.contract_type = 'undefined'
                else:
                    j.contract_type = 'other'
                if job['salary'] == 'A convenir':
                    j.salary = None
                    j.salary_max = None
                else:
                    s = job['salary'].split()[1].replace(',00', '').replace('.','')
                    j.salary = s
                    j.salary_max = s
                j.description = job['description']

                category = ''
                if job['category'] == 'Diseño / Decoración / Artes Gráficas':
                    category = 'diseño/multimedia'
                elif job['category'] == 'Informática / Telecomunicaciones':
                    category = 'programacion/tecnologia'
                elif job['category'] == 'Marketing / Publicidad / Producción Audiovisual':
                    category = 'marketing'
                elif job['category'] == 'Administración / Contabilidad / Finanzas':
                    category = 'administracion/finanzas'
                elif job['category'] == 'Legal / Asesoría':
                    category = 'legal'
                elif job['category'] == 'Arquitectura / Ingenierías':
                    category = 'ingenieria/arquitectura'
                elif job['category'] == 'Producción / Mantenimiento / Operaciones':
                    category = 'produccion/operarios'
                elif job['category'] == 'Recursos Humanos / Relaciones Públicas':
                    category = 'recursosHumanos'
                elif job['category'] == 'Hotelería / Turismo':
                    category = 'hosteleria/turismo'
                elif job['category'] == 'Comercial / Ventas / Atención al Cliente':
                    category = 'ventas'
                elif job['category'] == 'Compras / Comercio Exterior':
                    category = 'compras/comercioExterior'
                elif job['category'] == 'Medicina / Salud':
                    category = 'medicina/salud'
                elif job['category'] == 'Almacenamiento / Logística / Distribución':
                    category = 'almacenamiento/logistica'
                elif job['category'] == 'Construcción / Obras / Edificaciones':
                    category = 'construccion/obras'
                elif job['category'] == 'Docencia / Educación':
                    category = 'educacion'
                elif job['category'] == 'Investigación y Calidad':
                    category = 'investigacion/calidad'
                else:
                    category = 'otros'
                
                cat = Category.getByName(category)
                if cat is None:
                    cat = Category(category)
                    cat.save()
                    subCategory = Subcategory('general' + category)
                    cat.subcategories.append(subCategory)
                    cat.save()

                # aca iria todo el chorrete de if para la subcategoria, por ahora lo metemos en general
                j.subcategory_id = Subcategory.getByName('general' + category).id

                if job['requirements'] is not None:
                    for requirement in job['requirements']:
                        r = requirement.split(':')
                        j.requirements.append(Requirement(r[0], r[1]))
                    j.save()
                c = Company.get_by_name(job['company_name'])
                if c is not None:
                    c.jobs.append(j)
                    c.save()
                else:
                    c = Company(job['company_name'])
                    last_idc = Company.get_id()[0]['setval']
                    if last_idc is not None:
                        c.id = Company.get_id()[0]['setval']+1
                    else:
                        c.id = 1
                    c.save()
                    c.jobs.append(j)
                    c.save()
                activeJobs.append(j.id)
            else:
                activeJobs.append(jobExists.id)
        
        allJobs = Job.get_all_by_url('mipleo')
        for job in allJobs:
            if job.id in activeJobs:
                pass
            else:
                job.active = False
                job.save()

        return "Ok", 201

class JobsWorkanaRA(Resource):
    def post(self):
        user_id = validateToken(request, 'funcionario')
        data = request.get_json()
        if 'Scrapy' in request.headers:
            data = json.loads(data)
        activeJobs = []
        response = requests.get("https://cotizaciones-brou.herokuapp.com/api/currency/latest")
        jsonResponse = response.json()
        cotiz = jsonResponse["rates"]["USD"]["buy"]
        for job in data:
            jobExists = Job.search_by_url(job['url'])
            if jobExists is None:
                j = Job(job['url'], job['title'])
                last_id = j.get_id()[0]['setval']
                if last_id is not None:
                    j.id = j.get_id()[0]['setval']+1
                else:
                    j.id = 1
                j.location = 'remote'
                if 'workday' in job and job['workday'] == 'Tiempo completo': 
                    j.workday = 'FullTime'
                elif 'workday' in job and job['workday'] == 'A tiempo parcial':
                    j.workday = 'PartTime'
                else:
                    j.workday = 'notspecified'
                if 'contract_type' in job and job['contract_type'] == 'Fecha de entrega: No definido':
                    j.contract_type = 'undefined'
                else: 
                    j.contract_type = 'defined'
                s = job['salary'].replace('.','')
                salaryArray = [int(s) for s in re.findall(r'-?\d+\.?\d*', s)]

                if 'Menos de' in job['salary']:
                    j.salary_max = salaryArray[0]*cotiz
                elif 'Más de' in job['salary']:
                    j.salary = salaryArray[0]*cotiz
                else:
                    j.salary = salaryArray[0]*cotiz
                    j.salary_max = salaryArray[1]*cotiz
                
                j.description = job['description']
                category = ''
                if job['category'] == 'Programación y Tecnología' or job['category'] == 'Programación Web' or job['category'] == 'Diseño Web' or job['category'] == 'Tiendas virtuales (ecommerce)' or job['category'] == 'Wordpress' or job['category'] == 'Programación de Apps. Android, iOS y otros' or job['category'] == 'Data Science' or job['category'] == 'Aplicaciones de escritorio':
                    category = 'programacion/tecnologia'
                elif job['category'] == 'Diseño y Multimedia' or job['category'] == 'Diseño de Logo' or job['category'] == 'Diseño Web' or job['category'] == 'Banners' or job['category'] == 'Ilustraciones' or job['category'] == 'Crear o editar video' or job['category'] == 'Infografías' or job['category'] == 'Imágenes para redes sociales' or job['category'] == 'Diseño de App Móvil' or job['category'] == 'Imagen Corporativa' or job['category'] == 'Modelos 3D' or job['category'] == 'Landing Page' or job['category'] == 'Diseño de moda':
                    category = 'diseño/multimedia'
                elif job['category'] == 'Redacción y Traducción' or job['category'] == 'Redacción de artículos' or job['category'] == 'Redacción para sitios web' or job['category'] == 'Revisión de textos' or job['category'] == 'Publicaciones para redes sociales' or job['category'] == 'Traducción' or job['category'] == 'Subtitulado':
                    category = 'redaccion/traduccion'
                elif job['category'] == 'Marketing Digital y Ventas' or job['category'] == 'SEO' or job['category'] == 'Community Management' or job['category'] == 'Publicidad en Google, Facebook' or job['category'] == 'Email marketing' or job['category'] == 'Data analytics' or job['category'] == 'Televentas' or job['category'] == 'Comercial / Vendedor':
                    category = 'marketing'
                elif job['category'] == 'Soporte Administrativo' or job['category'] == 'Asistente virtual' or job['category'] == 'Atención al cliente' or job['category'] == 'Data entry' or job['category'] == 'Investigación de mercado' or job['category'] == 'Televentas':
                    category = 'ventas'
                elif job['category'] == 'Legal':
                    category = 'legal'
                elif job['category'] == 'Finanzas y Negocios' or job['category'] == 'Revelamiento de datos' or job['category'] == 'Trabajar con un CRM' or job['category'] == 'Gestionar proyectos' or job['category'] == 'Hacer reclutamiento' or job['category'] == 'Planeamiento estratégico' or job['category'] == 'Tareas de Contabilidad':
                    category = 'administracion/finanzas'
                elif job['category'] == 'Ingeniería y Arquitectura' or job['category'] == 'Diseño industrial' or job['category'] == 'Dibujos de CAD' or job['category'] == 'Modelador en 3D' or job['category'] == 'Diseño de interiores':
                    category = 'ingenieria/arquitectura'
                else:
                    category = 'otros'
                cat = Category.getByName(category)
                if cat is None:
                    cat = Category(category)
                    cat.save()
                    subCategory = Subcategory('general' + category)
                    cat.subcategories.append(subCategory)
                    cat.save()

                # aca iria todo el chorrete de if para la subcategoria, por ahora lo metemos en general
                j.subcategory_id = Subcategory.getByName('general' + category).id

                j.save()
                if job['requirements'] is not None:
                    for requirement in job['requirements']:
                        j.requirements.append(Requirement(requirement, requirement))
                    j.save()
                    
                activeJobs.append(j.id)
            else:
                activeJobs.append(jobExists.id)

        allJobs = Job.get_all_by_url('workana')
        for job in allJobs:
            if job.id in activeJobs:
                pass
            else:
                job.active = False
                job.save()

        return "Ok", 201


class JobRA(Resource):
    def get(self, id):
        user_id = validateToken(request, 'funcionario')
        j = Job.get_by_id(id)
        if j is not None:
            res = {
                'msg': 'Ok',
                'results': JobSchema().dump(j)
            }
            return make_response(jsonify(res), 200)  
        raise ObjectNotFound('No existe un trabajo para el Id dado.')

class JobsSearchByTitleRA(Resource):
    def post(self):
        user_id = validateToken(request, ['funcionario', 'cliente'])
        j = Job.search_by_title(request.get_json()['title'])
        res = {
            'jobs': JobsByTitleSchema().dump(j, many=True)
        }
        return make_response(jsonify(res), 200)

class JobRecommendedUsersRA(Resource):
    def get(self, id):
        user_id = validateToken(request, 'funcionario')
        users = Curriculum.get_all_by_job_id(id)
        res = {
            'results': UserByEmailSchema().dump(users, many=True)
        }
        return make_response(jsonify(res), 200)


api.add_resource(JobsCompuTrabajoRA, '/api/jobs/a/computrabajo')
api.add_resource(JobRA, '/api/jobs/a/<int:id>')
api.add_resource(JobsSearchByTitleRA, '/api/jobs/a/searchbytitle')
api.add_resource(JobsWorkanaRA, '/api/jobs/a/workana')
api.add_resource(JobsMipleoRA, '/api/jobs/a/mipleo')
api.add_resource(JobRecommendedUsersRA, '/api/jobs/a/<int:id>/recommendations')

from flask import make_response, jsonify,request
from models import db, Permission
from flask_jwt_extended import jwt_required
from middleware import roles_required
from schemas import PermissionSchema
from permissions.logs import log_permissions_action

#Defining all methods of Permissions service
class Permissions():
    @jwt_required()
    @roles_required(['Admin'])
    def permissions(self,page,per_page):
        data = Permission.query.order_by(Permission.id.asc()).paginate(page=page,per_page=per_page,error_out=False)
        
        if not data:
            log_permissions_action("permissions","failure",'No permissions available')
            response = make_response(jsonify({'msg':'No permissions available'}))
        
        log_permissions_action("permissions","success","Details",{
            'data':[info.json() for info in data]
        })
        response = make_response(jsonify({'data':[info.json() for info in data]}), 200)
        return response
    
    @jwt_required()
    @roles_required(['Admin'])
    def create_permissions(self,data):
        data = request.get_json()
        
        if not data:
            errors = PermissionSchema().validate(data)
            if errors:
                log_permissions_action("create_permissions", "failure", "Validation errors",errors)
                return errors, 422
        
        permissions = Permission(permission_name = data['permission_name'])
        db.session.add(permissions)
        db.session.commit()
        
        log_permissions_action("permissions","success",'Permissions Created Successfully!',{
            'data':{
                        'id':permissions.id,
                        'permission_name':permissions.permission_name
                    }
        })
        response = jsonify({'msg':'Permissions Created Successfully!',
                        'data': {
                            'id':permissions.id,
                            'permission_name':permissions.permission_name
                        }})
        return response

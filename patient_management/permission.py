from rest_framework import permissions

class IsPatientUser(permissions.BasePermission):
    
   
    def has_permission(self, request, view):
       
        return request.user.user_type == 0 or request.user.user_type=="0"
    
class IsAdminUser(permissions.BasePermission):
    
   
    def has_permission(self, request, view):
       
        return request.user.user_type == 1 or request.user.user_type == "1"
    
class IsDocterUser(permissions.BasePermission):
    
   
    def has_permission(self, request, view):
       
        return request.user.user_type == 2 or request.user.user_type == "2"


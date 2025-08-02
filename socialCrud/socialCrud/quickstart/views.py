from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets, status, authentication, authtoken
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import DjangoModelPermissions
from django.db.utils import IntegrityError
from socialCrud.quickstart.serializers import GroupSerializer, UserSerializer, HomePageSerializer
from socialCrud.quickstart.models import PostIT


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated] 

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    ''' Create a User [POST] '''
    def create(self, request: Request, pk=None):
        self.permission_classes = [permissions.IsAuthenticated]
        self.check_permissions(request=request)
        try:
            queryset = User.objects.get_or_create(username=request.data['username'], password=request.data['password'], email=request.data['email'])
        except IntegrityError:
            return Response({'AlreadyExist': 'Code 208'}, status=status.HTTP_208_ALREADY_REPORTED)
        
        serializer = UserSerializer(queryset, many=True)
        return Response({'201':'created'}, status=status.HTTP_201_CREATED)
       

    def list(self, request: Request, pk=None): 
        queryset = User.objects.all().order_by('-date_joined')
        serialized = UserSerializer(queryset, many=True,context={'request':request})
        self.permission_classes = [permissions.IsAuthenticated]
        self.check_permissions(request=request)
        return Response(serialized.data, status=status.HTTP_200_OK)
    
    ''' Delete User [GET|POST] <id:int> '''
    def destroy(self, request: Request, pk=None):

        self.permission_classes = [permissions.IsAuthenticated]
        self.check_permissions(request=request)
        if pk:
            try:
                queryset = User.objects.get(id=pk)    
            except User.DoesNotExist:
                return Response({'IdNotFound':'Error 404'}, status=status.HTTP_404_NOT_FOUND)
            
            if queryset.username != str(request.user) and not request.user.is_superuser:
                return Response({'Unauthorized':'Error 401'}, status=status.HTTP_401_UNAUTHORIZED)
            
            else:
                queryset.delete()
                return Response({'IdNotFound':'Error 204'}, status=status.HTTP_204_NO_CONTENT)
            
        else:           
            return Response({'BadRequest':'Error 400'}, status=status.HTTP_400_BAD_REQUEST)
    # options
    def options(self, request: Request, pk=None):
        meta = self.metadata_class()
        data = meta.determine_metadata(request, self)
        data['actions']['GET'] = {'url': {'type':'field',
                                        'required':False,
                                        'read_only':True,
                                        'label':'Url'
                                        }
                                }
        data['actions']['DELETE'] = {
                                    'description': 'Make Sure You have Authenticated to Delete.',
                                    'PK': {'PK': 'PrimaryKey | ID', 'required': True, 'read_only':False, 'Label':'Url'},
                                    'url': {'type':'field',
                                        'required':False,
                                        'read_only':True,
                                        'label':'Url'
                                        },
                                    'username': {'type':'field',
                                        'required':False,
                                        'read_only':True,
                                        'label':'Username',
                                        'max_lenght':32
                                        }
                                }
        data['actions']['PATCH'] = {
                                    'description': "Make Sure You have Authenticated to UPDATE.",
                                    'PK': {'PK': 'PrimaryKey | ID', 'required': True, 'read_only':False, 'Label':'Url' },
                                    'url': {'type':'field',
                                            'required':False,
                                            'read_only':True,
                                            'Label':'Url'},
                                    'username': {'type':'field',
                                                 'required':False,
                                                 'read_only':True,
                                                 'Label': 'Username',
                                                 'max_lenght': 32},
                                    }
        data['actions']['POST'] = {
                                    'description': "To create a account proprerty.",
                                    'PK': {'PK': 'PrimaryKey | ID', 'required': False, 'read_only':False, 'Label':'Url'},
                                    'url': {'type':'field',
                                            'required':False,
                                            'read_only':True,
                                            'Label':'Url'},
                                    'username': {'type':'field',
                                                 'required':True,
                                                 'read_only':True,
                                                 'Label': 'Username',
                                                 'max_lenght': 32},
                                    'password': {'type':'field',
                                                 'required':True,
                                                 'read_only':True,
                                                 'Label': 'Password',
                                                 'max_lenght': 32},
                                    'email': {'type': 'field', 
                                              'required': True,
                                              'read_only': True,
                                              'Label': 'Email',
                                              'max_lenght': 64}
                                }   
        return Response(data=data, status=status.HTTP_200_OK)


class HomePageViewSet(viewsets.ModelViewSet):
    """
    API endpoint to see HomePage posts 
    """    
    queryset = PostIT.objects.all().order_by('-created_datetime')
    serializer_class = HomePageSerializer
    # options
    def options(self, request: Request, pk=None):
        meta = self.metadata_class()
        data = meta.determine_metadata(request, self)
        data['actions']['GET'] = {'url': {'type':'field',
                                        'required':False,
                                        'read_only':True,
                                        'label':'Url'
                                        }
                                }
        data['actions']['DELETE'] = {
                                    'description': 'Make Sure You have Authenticated to Delete.',
                                    'PK': {'PK': 'PrimaryKey | ID', 'required': True, 'read_only':False, 'Label':'Url'},
                                    'url': {'type':'field',
                                        'required':False,
                                        'read_only':True,
                                        'label':'Url'
                                        },
                                    'username': {'type':'field',
                                        'required':False,
                                        'read_only':True,
                                        'label':'Username',
                                        'max_lenght':32
                                        }
                                }
        data['actions']['PATCH'] = {
                                    'description': "Make Sure You have Authenticated to UPDATE.",
                                    'PK': {'PK': 'PrimaryKey | ID', 'required': True, 'read_only':False, 'Label':'Url' },
                                    'url': {'type':'field',
                                            'required':False,
                                            'read_only':True,
                                            'Label':'Url'},
                                    'username': {'type':'field',
                                                 'required':False,
                                                 'read_only':True,
                                                 'Label': 'Username',
                                                 'max_lenght': 32},
                                    'title': {'type':'field',
                                              'required':False,
                                              'read_only':True,
                                              'Label': 'String',
                                              'max_lenght': 32},
                                    'content': {'type':'field',
                                                'required':False,
                                                'read_only':True,
                                                'Label':'String',
                                                'max_lenght': 320}
        }
        data['actions']['POST'] = {
                                    'description': "Make Sure You have Authenticated to POST.",
                                    'PK': {'PK': 'PrimaryKey | ID', 'required': True, 'read_only':False, 'Label':'Url' },
                                    'url': {'type':'field',
                                            'required':False,
                                            'read_only':True,
                                            'Label':'Url'},
                                    'username': {'type':'field',
                                                 'required':False,
                                                 'read_only':True,
                                                 'Label': 'Username',
                                                 'max_lenght': 32},
                                    'title': {'type':'field',
                                              'required':False,
                                              'read_only':True,
                                              'Label': 'String',
                                              'max_lenght': 32},
                                    'content': {'type':'field',
                                                'required':False,
                                                'read_only':True,
                                                'Label':'String',
                                                'max_lenght': 320}
        }
        return Response(data=data, status=status.HTTP_200_OK)

    ''' post a POSTIT [POST] '''
    def create(self, request: Request, pk=None):
        self.permission_classes = [permissions.IsAuthenticated]
        self.check_permissions(request=request)
        ip_andress = request.META.get('HTTP_x_FORWARD')
        if ip_andress:
            ip_andress = ip_andress.strip(',')[0]
        elif not ip_andress:
            ip_andress = request.META.get('REMOTE_ADDR')
        try:
            queryset = PostIT.objects.get_or_create(creator = request.user, username=request.data['username'], title=request.data['title'], content=request.data['content'], ip_andress=ip_andress)
        except IntegrityError:
            return Response({'BadRequest':'Error 400'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = HomePageSerializer(queryset, many=True)
        return Response({'201':'created'}, status=status.HTTP_201_CREATED)

    ''' List POSTIT [Any] <id:int> '''
    def list(self, request,pk=None):
        queryset = PostIT.objects.all()
        serializer = HomePageSerializer(queryset, many=True, context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    ''' Update POSTIT [PATCH|POST] <id:int> '''
    def update(self, request: Request, pk=None, **kwargs):
        
        self.permission_classes = [permissions.IsAuthenticated]
        self.check_permissions(request=request)

        ip_andress = request.META.get('HTTP_X_FORWARDED_FOR')
        if ip_andress:
            ip_andress = ip_andress.strip(',')[0]
        elif not ip_andress:
            ip_andress = request.META.get("REMOTE_ADDR")
        queryset = PostIT.objects.get(id=pk) if pk else 1
        queryset.ip_andress = ip_andress

        if queryset == 1:
            return Response({'IdNotFound':'Error 404'}, status=status.HTTP_404_NOT_FOUND)

        if queryset.creator != str(request.user) and not request.user.is_superuser:
            validator = 401
        else:
            serializer = HomePageSerializer(queryset, data=request.data,  context={'request':request})
            validator = serializer if serializer.is_valid(raise_exception=True) else 1
        if validator == 1:
            return Response({'BadRequest':'Error 400'}, status=status.HTTP_400_BAD_REQUEST) 
        
        elif validator == 401:
            return Response({'Unauthorized':'Error 401'}, status=status.HTTP_401_UNAUTHORIZED)  
        
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    ''' POSTIT DELETE [POST|GET] <id:int> '''
    def destroy(self, request: Request, pk=None):
        self.permission_classes = [DjangoModelPermissions]
        self.check_permissions(request=request)
        if pk:
            try:
                queryset = PostIT.objects.get(id=pk)    
            except PostIT.DoesNotExist:
                return Response({'IdNotFound':'Error 404'}, status=status.HTTP_404_NOT_FOUND)
           
            if queryset.creator.strip() == str(request.user) or request.user.is_superuser:
                queryset.delete()
            else:
                return Response({'Unauthorized':'Error 401'}, status=status.HTTP_401_UNAUTHORIZED)
            
            return Response({'IdNotFound':'Error 204'}, status=status.HTTP_204_NO_CONTENT)
        
        else:           
            return Response({'BadRequest':'Error 400'}, status=status.HTTP_400_BAD_REQUEST)
    # #
    # #
    # #
    # #
    # #
    # #
class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
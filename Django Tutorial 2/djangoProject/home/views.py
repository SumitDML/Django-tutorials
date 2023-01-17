from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import TodoSerializers,TimingTodoSerializer
from .models import Todo,TimingTodo
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.decorators import action

# Create your views here.
# DEMONSTRATION
# -------------------------------------------------------------------------
@api_view(['GET', 'POST', 'PATCH', 'PUT'])
def home(request):
    if request.method == 'GET':
        return Response({
            'status': 200,
            'message': "yes ! Your project is working!!",
            'method_called': "You called GET method!"
        })
    elif request.method == 'POST':
        return Response({
            'status': 200,
            'message': "yes ! Your project is working!!",
            'method_called': "You called POST method!"
        })
    elif request.method == 'PATCH':
        return Response({
            'status': 200,
            'message': "yes ! Your project is working!!",
            'method_called': "You called PATCH method!"
        })
    else:
        return Response({
            'status': 200,
            'message': "yes ! Your project is working!!",
            'method_called': "You called INVALID method!"
        })


# API VIEW DEMONSTRATION
# -------------------------------------------------------------

# class TodoView(APIView):
#     def get(self, request):
#         return Response({
#             'status': 200,
#             'message': "yes ! Your project is working!!",
#             'method_called': "You called GET method!"
#         })
#
#     def post(self, request):
#         return Response({
#             'status': 200,
#             'message': "yes ! Your project is working!!",
#             'method_called': "You called POST method!"
#         })
#
#     def put(self, request):
#         return Response({
#             'status': 200,
#             'message': "yes ! Your project is working!!",
#             'method_called': "You called PUT method!"
#         })


# WITH EACH METHOD FOR DIFFERENT API
# -----------------------------------------------------------------------------

@api_view(['POST'])
def post_todo(request):
    try:
        data = request.data
        serializer = TodoSerializers(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': True,
                'message': "To-Do Created Successfully!",
                'data': serializer.data
            })

    except Exception as e:
        print(e)

    return Response({
        'status': False,
        'message': "Invalid Data",
        'data': serializer.errors
    })


@api_view(['GET'])
def get_todo(request):
    todo_objs = Todo.objects.all()
    serializer = TodoSerializers(todo_objs, many=True)
    return Response({
        'status': 200,
        'message': "Data Fetched Successfully!",
        'data': serializer.data
    })


@api_view(['PATCH'])
def patch_todo(request):
    try:
        data = request.data
        if not data.get('uid'):
            return Response({
                'status': False,
                'message': "UID is Required!"
            })
        obj = Todo.objects.get(uid=data.get('uid'))
        serializer = TodoSerializers(obj, data=data, partial=True)
        if serializer.is_valid():
            serializer.save
            return Response({
                'status': 200,
                'message': "Data Updated Successfully!",
                'data': serializer.data
            })

    except Exception as e:
        print(e)
    return Response({
        'status': False,
        'message': "Invalid UID",
    })


# USING API VIEWs
# --------------------------------------------------------------------------------

class TodoView(APIView):
    def get(self, request):
        todo_objs = Todo.objects.all()
        serializer = TodoSerializers(todo_objs, many=True)
        return Response({
            'status': 200,
            'message': str(len(serializer.data))+"Data Fetched Successfully!",
            'data': serializer.data
        })

    def post(self, request):
        try:
            data = request.data
            serializer = TodoSerializers(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status': True,
                    'message': "To-Do Created Successfully!",
                    'data': serializer.data
                })

        except Exception as e:
            print(e)

        return Response({
            'status': False,
            'message': "Invalid Data",
            'data': serializer.errors
        })

    def put(self, request):
        return Response({
            'status': 200,
            'message': "yes ! Your project is working!!",
            'method_called': "You called PUT method!"
        })

class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializers

    @action(detail=False, methods=['GET'])
    def get_timing_todo(self, request):
        objs = TimingTodo.objects.all()
        serializer = TimingTodoSerializer(objs,many=True)
        return Response({
            'status': True,
            'message': "Timing Todo fetched!",
            'data': serializer.data
        })

    @action(detail=False,methods=['POST'])
    def add_date_to_todo(self,request):
        try:
            data = request.data
            serializer = TimingTodoSerializer(data = data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status': True,
                    'message': "To-Do Created Successfully!",
                    'data': serializer.data
                 })
        except Exception as e:
            print(e)

        return Response({
            'status': False,
            'message': "Invalid Data",
            'data': serializer.errors
        })
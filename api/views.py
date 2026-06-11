from rest_framework import generics, permissions, viewsets
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter 
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room, Message
from .serializers import RoomSerializer, MessageSerializer


class StandardResultsPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'size'
    max_page_size = 100

class IsHostOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.host == request.user

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all().order_by('-created')
    serializer_class = RoomSerializer
    
    pagination_class = StandardResultsPagination
    filter_backends = [SearchFilter]
    search_fields = ['name', 'topic__name', 'description']

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsHostOrReadOnly()]
        
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        serializer.save(host=self.request.user)


#-------------------------------LC and RUD CBVs-------------------------------


# class StandardResultsPagination(PageNumberPagination):
#     page_size = 5
#     page_size_query_param = 'size'
#     max_page_size = 100

# class IsHostOrReadOnly(permissions.BasePermission):

#     def has_object_permission(self, request, view, obj):
#         if request.method in permissions.SAFE_METHODS:
#             return True
        
#         return obj.host == request.user


# class RoomListCreateAPIView(generics.ListCreateAPIView):
#     queryset = Room.objects.all().order_by('-created')
#     serializer_class = RoomSerializer

#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]

#     pagination_class = StandardResultsPagination
#     filter_backends = [SearchFilter]
#     search_fields = ['name', 'topic__name', 'description']

#     def perform_create(self, serializer):
#         serializer.save(host=self.request.user)


# class RoomRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Room.objects.all()
#     serializer_class = RoomSerializer

#     permission_classes = [IsHostOrReadOnly]




#--------------------------------CBV-------------------------------


# class RoomListCreateAPIView(APIView):

#     def get(self, request):
#         rooms = Room.objects.all()
#         search_query = request.GET.get('search', '')

#         if search_query != '':
#             rooms = rooms.filter(
#                 Q(name__icontains=search_query) |
#                 Q(topic__name__icontains=search_query) |
#                 Q(description__icontains=search_query)
#             )

#         paginator = Paginator(rooms, 5) 
#         page_number = request.GET.get('page') 

#         try:
#             rooms = paginator.page(page_number)
#         except PageNotAnInteger:
#             rooms = paginator.page(1)
#         except EmptyPage:
#             rooms = paginator.page(paginator.num_pages)

#         serializer = RoomSerializer(rooms, many=True)
#         return Response({
#             'rooms': serializer.data,
#             'page': rooms.number,
#             'total_pages': paginator.num_pages
#         })


#     def post(self, request):
#         if not request.user.is_authenticated:
#             return Response({"detail": "Authentication required."}, status=401)

#         serializer = RoomSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(host=request.user)
#             return Response(serializer.data, status=201) 
#         return Response(serializer.errors, status=400)


#-------------------------------FBV-------------------------------

# @api_view(['GET', 'POST'])
# def get_rooms(request):
#     if request.method == 'GET':
#         search_query = request.GET.get('search', '')

#         rooms = Room.objects.filter(
#             Q(name__icontains=search_query) |
#             Q(topic__name__icontains=search_query) |
#             Q(description__icontains=search_query)
#         )

#         paginator = Paginator(rooms, 5) 
#         page_number = request.GET.get('page')

#         try:
#             rooms = paginator.page(page_number) #now rooms is the page object, not the queryset
#         except PageNotAnInteger:
#             rooms = paginator.page(1)
#         except EmptyPage:
#             rooms = paginator.page(paginator.num_pages)

#         serializer = RoomSerializer(rooms, many=True)
#         return Response({
#             'rooms': serializer.data,
#             'page': rooms.number,
#             'total_pages': paginator.num_pages
#         })  

#     if request.method == 'POST':
#         serializer = RoomSerializer(data=request.data)
        
#         if serializer.is_valid():
#             serializer.save(host=request.user)
#             return Response(serializer.data, status=201) 
            
#         return Response(serializer.errors, status=400)
    

# @api_view(['GET', 'PUT', 'DELETE'])
# def get_room(request, pk):
#     try:
#         room = Room.objects.get(id=pk)
#     except Room.DoesNotExist:
#         return Response({'error': 'Room not found'}, status=404)

#     if request.method == 'GET':
#         serializer = RoomSerializer(room, many=False)
#         return Response(serializer.data)

#     if request.method == 'PUT':
#         serializer = RoomSerializer(room, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=400)

#     if request.method == 'DELETE':
#         room.delete()
#         return Response({'message': 'Room successfully deleted'}, status=204)



# @api_view(['GET', 'POST'])
# def get_messages(request):
#     if (request.method == 'GET'):
#         room_id = request.GET.get('room')
#         if room_id:
#                 messages = messages.filter(room__id=room_id)
        
#         search_query = request.GET.get('search')
#         if search_query:
#             messages = messages.filter(body__icontains=search_query)

#         serializer = MessageSerializer(messages, many=True)
#         return Response(serializer.data)

#     if(request.method == 'POST'):
#         if not request.user.is_authenticated:
#             return Response({"detail": "Authentication required to post."}, status=401)
        
#         serializer = MessageSerializer(data=request.data)
        
#         if(serializer.is_valid()):
#             serializer.save(user=request.user)
#             return Response(serializer.data, status=201)

#         return Response(serializer.errors, status=400)
    

# @api_view(['GET', 'PUT', 'DELETE'])
# def get_message(request, pk):
#     try:
#         message = Message.objects.get(id=pk)
#     except Message.DoesNotExist:
#         return Response({'error': 'Message not found'}, status=404)
    
#     if request.method == 'GET':
#         serializer = MessageSerializer(message, many=False)
#         return Response(serializer.data)
    
#     if request.method == 'PUT':
#         if not request.user.is_authenticated:
#             return Response({"detail": "Authentication required."}, status=401)
            
#         if message.user != request.user:
#             return Response({'error': 'You can only edit your own messages.'}, status=403)
#         serializer = MessageSerializer(data=request.data)
        
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
            
#         return Response(serializer.errors, status=400)
    
#     if request.method == 'DELETE':
#         if not request.user.is_authenticated:
#             return Response({"detail": "Authentication required."}, status=401)
            
#         if message.user != request.user:
#             return Response({'error': 'You can only delete your own messages.'}, status=403)
        
#         message.delete()
#         return Response({'message': 'Message successfully deleted'}, status=204)
            
    
    




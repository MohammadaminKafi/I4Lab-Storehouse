from rest_framework import viewsets, status, generics
from rest_framework.decorators import action, api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import AllowAny
from .models import (
    Student,
    Department,
    Professor,
    Category,
    Product,
    Test,
    Part,
    Request,
    RequestDetail,
    Borrow
)
from .serializers import (
    StudentSerializer,
    DepartmentSerializer,
    ProfessorSerializer,
    CategorySerializer,
    ProductSerializer,
    TestSerializer,
    PartSerializer,
    RequestSerializer,
    RequestDetailSerializer,
    BorrowSerializer,
    CreateRequestSerializer,
    ProductWithCategorySerializer,
    ProfessorWithDepartmentSerializer
)

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

class ProfessorViewSet(viewsets.ModelViewSet):
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=True, methods=['post'])
    def assign_test(self, request, pk=None):
        product = self.get_object()
        test_id = request.data.get('test_id')
        try:
            test = Test.objects.get(test_id=test_id)
            product.tests.add(test)
            return Response({'status': 'test assigned'}, status=status.HTTP_200_OK)
        except Test.DoesNotExist:
            return Response({'error': 'Test not found'}, status=status.HTTP_404_NOT_FOUND)

class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer

class PartViewSet(viewsets.ModelViewSet):
    queryset = Part.objects.all()
    serializer_class = PartSerializer

class RequestViewSet(viewsets.ModelViewSet):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        req = self.get_object()
        if req.status != 'pending':
            return Response({'error': 'Request is not pending'}, status=status.HTTP_400_BAD_REQUEST)
        # Approve the request
        req.status = 'approved'
        req.save()
        # Assign parts and create borrow records
        for detail in req.details.filter(status='pending'):
            available_part = Part.objects.filter(product=detail.product, available=True).first()
            if available_part:
                available_part.available = False
                available_part.save()
                detail.status = 'accepted'
                detail.save()
                Borrow.objects.create(
                    request_detail=detail,
                    part=available_part
                )
            else:
                detail.status = 'rejected'
                detail.save()
        return Response({'status': 'request approved and parts assigned'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        req = self.get_object()
        if req.status != 'pending':
            return Response({'error': 'Request is not pending'}, status=status.HTTP_400_BAD_REQUEST)
        req.status = 'rejected'
        req.save()
        # Update all details to rejected
        req.details.update(status='rejected')
        return Response({'status': 'request rejected'}, status=status.HTTP_200_OK)

class RequestDetailViewSet(viewsets.ModelViewSet):
    queryset = RequestDetail.objects.all()
    serializer_class = RequestDetailSerializer

class BorrowViewSet(viewsets.ModelViewSet):
    queryset = Borrow.objects.all()
    serializer_class = BorrowSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])
def create_request(request):
    """
    Create a new request with associated products and request details.
    """
    serializer = CreateRequestSerializer(data=request.data)

    if serializer.is_valid():
        # Create the request and associated request details
        request_obj = serializer.save()
        return Response({
            'status': 'success',
            'request_id': request_obj.request_id
        }, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@permission_classes([AllowAny])
@authentication_classes([])
class AvailableProductListView(generics.ListAPIView):
    queryset = Product.objects.filter(available=True)  # Filter only available products
    serializer_class = ProductWithCategorySerializer

@permission_classes([AllowAny])
@authentication_classes([])
class ProfessorListView(generics.ListAPIView):
    queryset = Professor.objects.all()  # Retrieve all professors
    serializer_class = ProfessorWithDepartmentSerializer

@permission_classes([AllowAny])
@authentication_classes([])
class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
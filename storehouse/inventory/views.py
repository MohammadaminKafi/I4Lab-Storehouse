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
    
    @action(detail=False, methods=['get'])
    def pending(self, request):
        """ Return a list of all requests that are in 'pending' status. """
        pending_requests = self.get_queryset().filter(status='pending')
        serializer = self.get_serializer(pending_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'])
    def details(self, request, pk=None):
        """
        Return all request_details for this specific request.
        """
        req = self.get_object()
        details = req.details.all()
        serializer = RequestDetailSerializer(details, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class RequestDetailViewSet(viewsets.ModelViewSet):
    queryset = RequestDetail.objects.all()
    serializer_class = RequestDetailSerializer

    @action(detail=True, methods=['post'])
    def approve_detail(self, request, pk=None):
        """
        Approve a single RequestDetail by assigning a part and creating a Borrow record.
        """
        detail = self.get_object()
        if detail.status != 'pending':
            return Response(
                {'error': 'Detail is not pending'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Try to find an available part
        part = Part.objects.filter(product=detail.product, available=True).first()
        if not part:
            return Response({'error': 'No available part for this product'}, status=status.HTTP_400_BAD_REQUEST)

        # Mark part as unavailable
        part.available = False
        part.save()

        # Mark detail as accepted
        detail.status = 'accepted'
        detail.save()

        # Create Borrow record
        Borrow.objects.create(request_detail=detail, part=part)

        return Response(
            {'status': f'RequestDetail {detail.detail_id} approved and part assigned.'}, 
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['post'])
    def reject_detail(self, request, pk=None):
        """
        Reject a single RequestDetail, which has no effect on borrows.
        """
        detail = self.get_object()
        if detail.status != 'pending':
            return Response(
                {'error': 'Detail is not pending'},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Mark detail as rejected
        detail.status = 'rejected'
        detail.save()

        return Response(
            {'status': f'RequestDetail {detail.detail_id} rejected.'},
            status=status.HTTP_200_OK
        )

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
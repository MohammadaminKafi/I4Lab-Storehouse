from rest_framework import serializers
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

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = '__all__'

class PartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Part
        fields = '__all__'

class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = '__all__'

class RequestDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestDetail
        fields = '__all__'

class BorrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrow
        fields = '__all__'



class ProductRequestSerializer(serializers.Serializer):
    product = serializers.IntegerField()  # Product ID
    borrow_due_date = serializers.DateTimeField()  # Due date for borrowing
    retrieval_due_date = serializers.DateTimeField()  # Due date for retrieval
    description = serializers.CharField()  # Description of the product's need

class CreateRequestSerializer(serializers.Serializer):
    student_number = serializers.CharField()  # Student number
    professor_id = serializers.IntegerField()  # Professor ID
    products = ProductRequestSerializer(many=True)  # List of products to request

    def validate_student_number(self, value):
        try:
            student = Student.objects.get(student_number=value)
        except Student.DoesNotExist:
            raise serializers.ValidationError("Student with this number does not exist.")
        return value

    def validate_professor_id(self, value):
        try:
            professor = Professor.objects.get(professor_id=value)
        except Professor.DoesNotExist:
            raise serializers.ValidationError("Professor with this ID does not exist.")
        return value

    def create(self, validated_data):
        student = Student.objects.get(student_number=validated_data['student_number'])
        professor = Professor.objects.get(professor_id=validated_data['professor_id'])

        # Create the request record
        request = Request.objects.create(student=student, referrer=professor)

        # Create request details and associate them with the request
        products_data = validated_data['products']
        for product_data in products_data:
            product = Product.objects.get(product_id=product_data['product'])
            RequestDetail.objects.create(
                request=request,
                product=product,
                borrow_due_date=product_data['borrow_due_date'],
                retrieval_due_date=product_data['retrieval_due_date'],
                description=product_data['description']
            )
        return request

class ProductWithCategorySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)  # Include category name
    
    class Meta:
        model = Product
        exclude = ['available']

class ProfessorWithDepartmentSerializer(serializers.ModelSerializer):
    department_id = serializers.IntegerField(source='department.department_id', read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)

    class Meta:
        model = Professor
        fields = ['professor_id', 'first_name', 'last_name', 'department_id', 'department_name']

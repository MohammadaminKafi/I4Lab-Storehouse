from django.contrib import admin
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

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'student_number', 'first_name', 'last_name', 'phone_number')
    search_fields = ('student_number', 'first_name', 'last_name')

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('department_id', 'name')
    search_fields = ('name',)

@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('professor_id', 'first_name', 'last_name', 'email', 'phone_number', 'department')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('department',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_id', 'name')
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'name', 'category', 'available', 'tested', 'created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('category', 'available', 'tested')

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('test_id', 'product', 'test_path', 'created_at')
    search_fields = ('product__name',)
    list_filter = ('product',)

@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
    list_display = ('part_id', 'product', 'serial_number', 'available', 'added_at')
    search_fields = ('serial_number', 'product__name')
    list_filter = ('product', 'available')

@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('request_id', 'student', 'referrer', 'submission_date', 'status', 'updated_at')
    search_fields = ('student__student_number', 'referrer__first_name', 'referrer__last_name')
    list_filter = ('status', 'submission_date', 'updated_at')

@admin.register(RequestDetail)
class RequestDetailAdmin(admin.ModelAdmin):
    list_display = ('detail_id', 'request', 'product', 'status', 'borrow_due_date', 'retrieval_due_date')
    search_fields = ('request__request_id', 'product__name')
    list_filter = ('status', 'borrow_due_date', 'retrieval_due_date')

@admin.register(Borrow)
class BorrowAdmin(admin.ModelAdmin):
    list_display = ('borrow_id', 'request_detail', 'part', 'borrow_date', 'borrow_test', 'retrieval_date', 'retrieval_test')
    search_fields = ('request_detail__request__request_id', 'part__serial_number')
    list_filter = ('borrow_test', 'retrieval_test', 'borrow_date', 'retrieval_date')

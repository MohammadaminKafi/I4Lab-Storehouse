from django import forms
from django.contrib import admin
from django.urls import reverse, path
from django.utils.html import format_html
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404, render
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
    list_display = ['request_id', 'student', 'status', 'referrer', 'view_details', 'approve_button', 'reject_button', 'submission_date']
    list_filter = ['status', 'submission_date', 'updated_at']
    search_fields = ['request_id', 'student__student_number', 'referrer__last_name']
    
    def view_details(self, obj):
        """
        Creates a link to the RequestDetailAdmin changelist,
        filtered by this Request's ID.
        """
        url = (
            reverse("admin:inventory_requestdetail_changelist")
            + f"?request__request_id__exact={obj.request_id}"
        )
        return format_html('<a href="{}">View Details</a>', url)
    view_details.short_description = "Request Details"

    def approve_button(self, obj):
        # We'll create a link that calls the "approve_request" admin action
        if obj.status == 'pending':
            url = reverse('admin:inventory_request_approve', args=[obj.pk])
            return format_html("<a class='button' href='{}'>Approve</a>", url)
        return "—"
    approve_button.short_description = "Approve"

    def reject_button(self, obj):
        # We'll create a link that calls the "reject_request" admin action
        if obj.status == 'pending':
            url = reverse('admin:inventory_request_reject', args=[obj.pk])
            return format_html("<a class='button' href='{}'>Reject</a>", url)
        return "—"
    reject_button.short_description = "Reject"

    def get_urls(self):
        # Get the default admin urls
        urls = super().get_urls()
        my_urls = [
            path(
                '<int:request_id>/approve/',
                self.admin_site.admin_view(self.approve_request),
                name='inventory_request_approve',
            ),
            path(
                '<int:request_id>/reject/',
                self.admin_site.admin_view(self.reject_request),
                name='inventory_request_reject',
            ),
        ]
        return my_urls + urls
    
    def approve_request(self, request, request_id):
        # This method matches your existing logic to "approve" from the ViewSet
        # We'll replicate it in admin
        req = get_object_or_404(Request, pk=request_id)
        if req.status != 'pending':
            self.message_user(request, "Request is not pending, cannot approve.", level="error")
            return redirect('admin:inventory_request_changelist')

        # Approve
        req.status = 'approved'
        req.save()

        # # For each pending detail, assign part and create Borrow
        # details = req.details.filter(status='pending')
        # for detail in details:
        #     available_part = Part.objects.filter(product=detail.product, available=True).first()
        #     if available_part:
        #         available_part.available = False
        #         available_part.save()
        #         detail.status = 'accepted'
        #         detail.save()
        #         Borrow.objects.create(
        #             request_detail=detail,
        #             part=available_part
        #         )
        #     else:
        #         detail.status = 'rejected'
        #         detail.save()

        self.message_user(request, f"Request {request_id} approved and parts assigned.")
        return redirect('admin:inventory_request_changelist')
    
    def reject_request(self, request, request_id):
        from django.shortcuts import redirect, get_object_or_404
        req = get_object_or_404(Request, pk=request_id)
        if req.status != 'pending':
            self.message_user(request, "Request is not pending, cannot reject.", level="error")
            return redirect('admin:inventory_request_changelist')

        req.status = 'rejected'
        req.save()
        # Update all details to rejected
        req.details.update(status='rejected')

        self.message_user(request, f"Request {request_id} rejected.")
        return redirect('admin:inventory_request_changelist')

@admin.register(RequestDetail)
class RequestDetailAdmin(admin.ModelAdmin):
    list_display = ('detail_id', 'request', 'product', 'status', 'borrow_due_date', 'retrieval_due_date')
    list_filter = ['status', 'borrow_due_date', 'retrieval_due_date', 'product']
    search_fields = ['request__request_id', 'product__name']

@admin.register(Borrow)
class BorrowAdmin(admin.ModelAdmin):
    list_display = ('borrow_id', 'request_detail', 'part', 'borrow_date', 'borrow_test', 'retrieval_date', 'retrieval_test')
    search_fields = ('request_detail__request__request_id', 'part__serial_number')
    list_filter = ('borrow_test', 'retrieval_test', 'borrow_date', 'retrieval_date')
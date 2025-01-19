from django.db import models

# Enums for status fields
class RequestStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    REVIEWED = 'reviewed', 'Reviewed'
    APPROVED = 'approved', 'Approved'
    REJECTED = 'rejected', 'Rejected'

class RequestDetailStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    ACCEPTED = 'accepted', 'Accepted'
    REJECTED = 'rejected', 'Rejected'

class BorrowTestStatus(models.TextChoices):
    NOT_TESTED = 'not_tested', 'Not Tested'
    SUCCESSFUL = 'successful', 'Successful'
    FAILED = 'failed', 'Failed'

class RetrievalTestStatus(models.TextChoices):
    NOT_TESTED = 'not_tested', 'Not Tested'
    SUCCESSFUL = 'successful', 'Successful'
    FAILED = 'failed', 'Failed'

# 1. Students
class Student(models.Model):
    student_id = models.AutoField(primary_key=True)
    student_number = models.CharField(max_length=20, unique=True, default='000000000')
    national_number = models.CharField(max_length=10, null=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# 2. Department
class Department(models.Model):
    department_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# 3. Professor
class Professor(models.Model):
    professor_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='professors')

    def __str__(self):
        return f"Prof. {self.first_name} {self.last_name}"

# 4. Category
class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

# 5. Product
class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=100)
    link = models.URLField(null=True, blank=True)
    datasheet = models.FileField(upload_to='datasheets/', null=True, blank=True)
    tested = models.BooleanField(default='false')
    available = models.BooleanField(default='true')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    def __str__(self):
        return self.name

# 6. Test
class Test(models.Model):
    test_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='tests')
    test_path = models.URLField(null=True, blank=True)
    test_manual = models.FileField(upload_to='test_manuals/', null=True, blank=True)
    test_description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Test {self.test_id} for {self.product.name}"

# 7. Part
class Part(models.Model):
    part_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='parts')
    serial_number = models.CharField(max_length=100, unique=True)
    available = models.BooleanField(default='true')
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Part {self.serial_number} of {self.product.name}"

# 8. Request
class Request(models.Model):
    request_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='requests')
    referrer = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name='referrals')
    referrer_organization = models.CharField(max_length=255, null=True, blank=True)
    submission_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10,
        choices=RequestStatus.choices,
        default=RequestStatus.PENDING
    )
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Request {self.request_id} by {self.student}"

# 9. RequestDetails
class RequestDetail(models.Model):
    detail_id = models.AutoField(primary_key=True)
    request = models.ForeignKey(Request, on_delete=models.CASCADE, related_name='details')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='request_details')
    status = models.CharField(
        max_length=10,
        choices=RequestDetailStatus.choices,
        default=RequestDetailStatus.PENDING
    )
    borrow_due_date = models.DateTimeField(null=True, blank=True)
    retrieval_due_date = models.DateTimeField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Detail {self.detail_id} for Request {self.request.request_id}"

# 10. Borrow
class Borrow(models.Model):
    borrow_id = models.AutoField(primary_key=True)
    request_detail = models.ForeignKey(RequestDetail, on_delete=models.CASCADE, related_name='borrows')
    part = models.ForeignKey(Part, on_delete=models.CASCADE, related_name='borrows')
    borrow_date = models.DateTimeField(auto_now_add=True)
    borrow_test = models.CharField(
        max_length=12,
        choices=BorrowTestStatus.choices,
        default=BorrowTestStatus.NOT_TESTED
    )
    retrieval_date = models.DateTimeField(null=True, blank=True)
    retrieval_test = models.CharField(
        max_length=12,
        choices=RetrievalTestStatus.choices,
        default=RetrievalTestStatus.NOT_TESTED
    )

    def __str__(self):
        return f"Borrow {self.borrow_id} of Part {self.part.serial_number}"
    

# forms.py
from django import forms
from .models import Borrow, Part, RequestDetail

class BorrowForm(forms.ModelForm):
    class Meta:
        model = Borrow
        # Exclude borrow_date since it is auto-filled
        fields = ['request_detail', 'part', 'borrow_test', 'retrieval_date', 'retrieval_test']

    def __init__(self, *args, **kwargs):
        # Retrieve the request_detail_id passed in the URL
        request_detail_id = kwargs.get('initial', {}).get('request_detail_id', None)
        super().__init__(*args, **kwargs)

        if request_detail_id:
            # Corrected query using 'detail_id' instead of 'id'
            request_detail = RequestDetail.objects.get(detail_id=request_detail_id)
            product_id = request_detail.product_id

            # Prepopulate the request_detail field and filter parts by the associated product_id
            self.fields['request_detail'].initial = request_detail_id
            self.fields['part'].queryset = Part.objects.filter(product_id=product_id)

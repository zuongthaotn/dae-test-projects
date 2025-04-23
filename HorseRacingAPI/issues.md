1.  Error : google.api_core.exceptions.Forbidden: 403 Billing has not been enabled for this project. Enable billing at https://console.cloud.google.com/billing. DML queries are not allowed in the free tier.
DK google cloud, su dung billing (creaditcard or paypal)

2. "message": "iam.gserviceaccount.com does not have storage.objects.create access to the Google Cloud Storage object. Permission 'storage.objects.create' denied on resource (or it may not exist).",
Tạo sẵn thư mục trên GCS để upload file vào nhưng bằng cách thần kì nào đó, user API lại ko có quyền truy cập vào folder. Xóa foldẻ đó đi hoặc đổi tên folder khác trong code.

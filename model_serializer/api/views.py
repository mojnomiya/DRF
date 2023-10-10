import io
from django.http import HttpResponse, JsonResponse
from django.views import View
from rest_framework.parsers import JSONParser
from api.models import Student
from rest_framework.renderers import JSONRenderer
from api.serializers import StudentSerializer
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


@method_decorator(csrf_exempt, name="dispatch")
class StudentAPI(View):
    def get(self, request, *args, **kwargs):
        json_data = request.body
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        id = pythondata.get("id", None)
        if id is not None:
            stu = Student.objects.get(id=id)
            serializer = StudentSerializer(stu)
            json_data = JSONRenderer().render(serializer.data)
            return HttpResponse(json_data, content_type="application/json")
        stu = Student.objects.all()
        serializer = StudentSerializer(stu, many=True)
        json_data = JSONRenderer().render(serializer.data)
        return HttpResponse(json_data, content_type="application/json")

    def post(self, request, *args, **kwargs):
        json_data = request.body
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        serializer = StudentSerializer(data=pythondata)

        if serializer.is_valid():
            serializer.save()
            res = {"msg": "Data created"}
            return JsonResponse(res, safe=False)
        return JsonResponse(serializer.errors, safe=False)

    def put(self, request, *args, **kwargs):
        json_data = request.body
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        id = pythondata.get("id")
        stu = Student.objects.get(id=id)

        serializer = StudentSerializer(stu, data=pythondata, partial=True)

        if serializer.is_valid():
            serializer.save()
            res = {"msg": "Data Updated"}
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type="application/json")

        json_data = JSONRenderer().render(serializer.errors)
        return HttpResponse(json_data, content_type="application/json")

    def delete(self, request, *args, **kwargs):
        json_data = request.body
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        id = pythondata.get("id")
        stu = Student.objects.get(id=id)
        stu.delete()
        res = {"msg": "Data Deleted!!"}

        return JsonResponse(res, safe=False)

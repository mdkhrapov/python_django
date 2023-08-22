from django.core.files.storage import FileSystemStorage
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

# Create your views here.

def process_get_view(request: HttpRequest) -> HttpResponse:
    a = request.GET.get("a", "")
    b = request.GET.get("b", "")
    result = a + b
    context = { "a": a,
                "b": b,
                "result": result
    }
    return render(request, "requestdataapp/request-query-params.html", context=context)

def user_form(request: HttpRequest) -> HttpResponse:
    context = {}
    return render(request, "requestdataapp/user-bio-form.html", context=context)

def handle_file_upload(request: HttpRequest) -> HttpResponse:
    context = {}
    if request.method == "POST" and request.FILES.get("myfile"):
        myfile = request.FILES["myfile"]
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        filesize_mb = int(fs.size(myfile.name))/(1024 * 1024)     # переводим в Мб
        context = {"filesize": filesize_mb}

        if filesize_mb > 1:
            fs.delete(myfile.name)
            print("file was delete")
            return render(request, "requestdataapp/error-upload.html", context=context)

        print(f"saved file: {filename}")
    return render(request, "requestdataapp/file-upload.html", context=context)
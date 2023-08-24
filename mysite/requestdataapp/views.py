from django.core.files.storage import FileSystemStorage
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from .forms import UserBioForm, UploadFileForm

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
    context = { "form": UserBioForm(), }
    return render(request, "requestdataapp/user-bio-form.html", context=context)

def upload_file_form(request: HttpRequest) -> HttpResponse:
    context = { "form": UploadFileForm(), }
    return render(request, "requestdataapp/file_upload", context=context)

def handle_file_upload(request: HttpRequest) -> HttpResponse:
    filesize_mb = 0

    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            #myfile = request.FILES["myfile"]
            myfile = form.cleaned_data["file"]
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            filesize_mb = int(fs.size(myfile.name))/(1024 * 1024)     # переводим в Мб
            print(f"saved file: {filename}")

            if filesize_mb > 1:
                fs.delete(myfile.name)
                print("file was delete")
                return render(request, "requestdataapp/error-upload.html", context=context)
    else:
        form = UploadFileForm()

    context = {"form": form, "filesize":filesize_mb}
    return render(request, "requestdataapp/file-upload.html", context=context)
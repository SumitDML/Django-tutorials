from django.http import HttpResponse,JsonResponse

def home_page(request):
    print("Home Page Requested")
    friends = ["Sumit","Sakti","Suraj","Abhinav"]
    #return HttpResponse("<h1>This is HomePage<h1>")
    return JsonResponse(friends,safe=False)
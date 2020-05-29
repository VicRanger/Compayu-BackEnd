from django.shortcuts import render


# 门户访问地址
def indexPage(request):
    response = render(request, 'indexPage.html')
    return response
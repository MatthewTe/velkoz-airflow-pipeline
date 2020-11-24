from django.shortcuts import render


def stock_dashboard_index(request):
    """
    """
    return render(request, 'stock_dashboard/stock_dashboard_index.html')

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Company

@login_required
def profile_edit(request):
    company, created = Company.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        company.name = request.POST.get('name', '')
        company.description = request.POST.get('description', '')
        company.industry = request.POST.get('industry', '')
        company.website = request.POST.get('website', '')
        company.save()
        return redirect('companies:profile_view', pk=company.pk)
    return render(request, 'companies/edit.html', {'company': company})

def profile_view(request, pk):
    company = get_object_or_404(Company, pk=pk)
    return render(request, 'companies/view.html', {'company': company})

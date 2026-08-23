# Import weasyprint only when needed to avoid issues on systems without GTK
def generate_resume_pdf(profile, request):
    import weasyprint
    from django.template.loader import render_to_string
    html_string = render_to_string(
        'profiles/themes/classic.html', {'profile': profile}, request=request
    )
    pdf = weasyprint.HTML(
        string=html_string, base_url=request.build_absolute_uri('/')
    ).write_pdf()
    return pdf

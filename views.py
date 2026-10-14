from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .models import Resume
from .serializers import ResumeSerializer
from .ai import extract_text_from_pdf, calculate_similarity


# =====================================
# 1️⃣ DRF API - Resume Upload
# =====================================
class ResumeUploadView(APIView):

    def post(self, request):
        name = request.data.get('name')
        file = request.FILES.get('file')
        job_description = request.data.get('job_description')

        if not file or not job_description:
            return Response(
                {"error": "File and job description required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            with transaction.atomic():
                resume = Resume.objects.create(name=name, file=file)

                resume_text = extract_text_from_pdf(resume.file.path)
                score = calculate_similarity(resume_text, job_description)

                resume.score = score
                resume.save()

            serializer = ResumeSerializer(resume)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {"error": f"Processing failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# =====================================
# 2️⃣ DRF API - Resume List
# =====================================
class ResumeListView(APIView):

    def get(self, request):
        resumes = Resume.objects.all().order_by('-uploaded_at')
        serializer = ResumeSerializer(resumes, many=True)
        return Response(serializer.data)


# =====================================
# 3️⃣ Template View - Home Page
# =====================================
def home(request):
    return render(request, 'core/frontend/home.html')


# =====================================
# 4️⃣ Template View - Upload Resume (UI)
# =====================================
def upload_resume(request):

    if request.method == "POST":
        name = request.POST.get('name')
        file = request.FILES.get('file')
        job_description = request.POST.get('job_description')

        if not file or not job_description:
            return render(
                request,
                'core/frontend/home.html',
                {"error": "File and Job Description required"}
            )

        try:
            with transaction.atomic():
                resume = Resume.objects.create(name=name, file=file)

                resume_text = extract_text_from_pdf(resume.file.path)
                score = calculate_similarity(resume_text, job_description)

                resume.score = score
                resume.save()

            return render(
                request,
                'core/frontend/home.html',
                {
                    "score": round(score, 2),
                    "name": name
                }
            )

        except Exception as e:
            return render(
                request,
                'core/frontend/home.html',
                {"error": f"Something went wrong: {str(e)}"}
            )

    return render(request, 'core/frontend/home.html')
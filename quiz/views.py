from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from django.http import JsonResponse
from django.contrib import messages
from .models import Assessment, Question, UserAssessment, UserResponse
import json
import random
import csv
import io

# Create your views here.

@login_required
def assessment_list(request):
    available_assessments = Assessment.objects.all()
    user_assessments = UserAssessment.objects.filter(user=request.user)
    
    context = {
        'available_assessments': available_assessments,
        'user_assessments': user_assessments,
    }
    return render(request, 'quiz/assessment_list.html', context)

@login_required
def start_assessment(request, assessment_id):
    assessment = get_object_or_404(Assessment, id=assessment_id)
    
    # Check if user has already started this assessment
    user_assessment, created = UserAssessment.objects.get_or_create(
        user=request.user,
        assessment=assessment,
    )
    
    if not created and user_assessment.completed_at:
        return redirect('quiz:assessment_list')
    
    return redirect('quiz:take_question', assessment_id=assessment_id)

@login_required
def take_question(request, assessment_id):
    assessment = get_object_or_404(Assessment, id=assessment_id)
    user_assessment = get_object_or_404(UserAssessment, user=request.user, assessment=assessment)
    
    if user_assessment.completed_at:
        return redirect('quiz:assessment_list')
    
    questions = assessment.questions.all()
    if user_assessment.current_question_index >= questions.count():
        user_assessment.completed_at = timezone.now()
        user_assessment.save()
        return redirect('quiz:assessment_results', assessment_id=assessment_id)
    
    current_question = questions[user_assessment.current_question_index]
    
    # Prepare options and shuffle
    options = [
        (1, current_question.option1),
        (2, current_question.option2),
        (3, current_question.option3),
        (4, current_question.option4)
    ]
    random.shuffle(options)

    # Map shuffled index (1-4) to original option number
    shuffled_to_original = {i+1: orig_pos for i, (orig_pos, _) in enumerate(options)}
    # Map original option number to text for template clarity (not strictly needed, but can help)
    original_to_text = {orig_pos: text for orig_pos, text in options}

    # Store mapping in session for this question
    if 'option_mappings' not in request.session:
        request.session['option_mappings'] = {}
    request.session['option_mappings'][str(current_question.id)] = shuffled_to_original
    request.session.modified = True

    context = {
        'assessment': assessment,
        'question': current_question,
        'question_number': user_assessment.current_question_index + 1,
        'total_questions': questions.count(),
        'options': [(i+1, text) for i, (orig_pos, text) in enumerate(options)],  # (shuffled index, text)
    }
    return render(request, 'quiz/take_question.html', context)

@login_required
def submit_answer(request, assessment_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    
    data = json.loads(request.body)
    selected_option = data.get('selected_option')
    
    assessment = get_object_or_404(Assessment, id=assessment_id)
    user_assessment = get_object_or_404(UserAssessment, user=request.user, assessment=assessment)
    
    if user_assessment.completed_at:
        return JsonResponse({'error': 'Assessment already completed'}, status=400)
    
    questions = assessment.questions.all()
    current_question = questions[user_assessment.current_question_index]
    
    # Retrieve mapping from session
    option_mappings = request.session.get('option_mappings', {})
    shuffled_to_original = option_mappings.get(str(current_question.id))
    print('DEBUG: option_mappings:', option_mappings)
    print('DEBUG: shuffled_to_original:', shuffled_to_original)
    print('DEBUG: selected_option:', selected_option)
    if not shuffled_to_original:
        return JsonResponse({'error': 'Option mapping not found. Please reload the page.'}, status=400)

    try:
        selected_option = int(selected_option)
    except (TypeError, ValueError):
        return JsonResponse({'error': 'Invalid option selected.'}, status=400)

    # Map shuffled index to original option number
    original_position = shuffled_to_original.get(str(selected_option))
    print('DEBUG: original_position:', original_position)
    print('DEBUG: correct_option:', current_question.correct_option)
    if not original_position:
        return JsonResponse({'error': 'Invalid option selected.'}, status=400)

    # Record user's response
    is_correct = (original_position == current_question.correct_option)
    UserResponse.objects.create(
        user_assessment=user_assessment,
        question=current_question,
        selected_option=original_position,
        is_correct=is_correct
    )
    
    if is_correct:
        user_assessment.score += 1
    
    user_assessment.current_question_index += 1
    user_assessment.save()
    
    # Clean up mapping for this question
    if str(current_question.id) in request.session.get('option_mappings', {}):
        del request.session['option_mappings'][str(current_question.id)]
        request.session.modified = True
    
    return JsonResponse({'success': True})

@login_required
def assessment_results(request, assessment_id):
    assessment = get_object_or_404(Assessment, id=assessment_id)
    user_assessment = get_object_or_404(UserAssessment, user=request.user, assessment=assessment)
    
    if not user_assessment.completed_at:
        return redirect('quiz:take_question', assessment_id=assessment_id)
    
    responses = UserResponse.objects.filter(user_assessment=user_assessment)
    total_questions = assessment.questions.count()
    
    context = {
        'assessment': assessment,
        'user_assessment': user_assessment,
        'responses': responses,
        'total_questions': total_questions,
        'score_percentage': (user_assessment.score / total_questions) * 100,
    }
    return render(request, 'quiz/assessment_results.html', context)

@login_required
@user_passes_test(lambda u: u.is_staff)
def create_assessment(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        csv_file = request.FILES.get('csv_file')
        
        if not title or not csv_file:
            messages.error(request, 'Please provide both title and CSV file.')
            return redirect('quiz:create_assessment')
        
        try:
            # Create the assessment
            assessment = Assessment.objects.create(
                title=title,
                created_by=request.user
            )
            
            # Process CSV file
            csv_file_content = csv_file.read().decode('utf-8')
            csv_reader = csv.reader(io.StringIO(csv_file_content))
            
            questions_created = 0
            for row in csv_reader:
                if len(row) != 5:  # Check if row has all required columns
                    continue
                
                question_text, option1, option2, option3, option4 = row
                
                # Create the question
                Question.objects.create(
                    assessment=assessment,
                    question_text=question_text.strip(),
                    option1=option1.strip(),
                    option2=option2.strip(),
                    option3=option3.strip(),
                    option4=option4.strip(),
                    correct_option=1  # First option is always correct
                )
                questions_created += 1
            
            messages.success(request, f'Assessment created successfully with {questions_created} questions.')
            return redirect('quiz:assessment_list')
            
        except Exception as e:
            messages.error(request, f'Error creating assessment: {str(e)}')
            return redirect('quiz:create_assessment')
    
    return render(request, 'quiz/create_assessment.html')

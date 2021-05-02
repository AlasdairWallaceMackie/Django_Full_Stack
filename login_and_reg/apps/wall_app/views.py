from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from .models import *

def wall(request):
    context = {
        'current_user': User.objects.get( id = request.session['current_user_id'] ),
        'all_messages': Message.objects.order_by('-created_at'),
    }
    print(f"First name: {context['current_user'].first_name}")
    return render(request, 'wall.html', context)

def create_message(request):
    print("Creating message")
    Message.objects.create(
        user_id = User.objects.get(id = request.session['current_user_id']),
        message = request.POST['message_field']
    )
    return redirect('/wall')

def delete_message(request):
    pass
    return redirect('/wall')

def create_comment(request):
    print("Creating comment")
    Comment.objects.create(
        user_id = User.objects.get(id = request.session['current_user_id']),
        message_id = Message.objects.get(id = request.POST['message_id']),
        comment = request.POST['comment_field']
    )
    return redirect('/wall')

def recent_message(request):
    response = ""
    message = Message.objects.order_by('-created_at').first()
    print(f"Author name: {message.author_full_name}")
    response += f"""
        <div class="message">
            <h4>{message.author_full_name()} - {message.post_date()}</h4>
            <p>{message.message}</p>
            
            <div class="comments_list">
    """

    for comment in message.comments.all():
        response += f"""
            <div class="comment">
                <strong>{comment.author_full_name()} - {comment.post_date()}</strong>
                <p>{comment.comment}</p>
            </div>
        """

    response += "</div></div>" ## Closes out .message and .comments_list elements

    return JsonResponse({'recent_message': response})

def recent_comment(request):
    response = ""
    comment = Comment.objects.order_by('-created_at').first()
    response += f"""
        <div class="comment">
            <strong>{comment.author_full_name()} - {comment.post_date()}</strong>
            <p>{comment.comment}</p>
        </div>
    """

    return JsonResponse({'recent_comment': response})

def all_messages(request):
    response = ""
    for message in Message.objects.all().order_by('-created_at'):
        response += f"""
            <div class="message">
                <h4>{message.author_full_name} - {message.post_date}</h4>
                <p>{message.message}</p>
                
                <div class="comments_list">
        """
        for comment in message.comments.all():
            response += f"""
                <div class="comment">
                    <strong>{comment.author_full_name} - {comment.post_date}</strong>
                    <p>{comment.comment}</p>
                </div>
            """
        response += "</div></div>" ## Closes out .message and .comment elements
        response += """
            <form class="post_comment" action="/wall/comment" method="POST">
                {% csrf_token %}
                <input type="hidden" name="message_id" value="{{message.id}}">
                <label for="comment_field">Post a comment</label>
                <textarea name="comment_field" id="comment_field" cols="30" rows="1"></textarea>
                <input type="submit" class="submit-button green" value="Post a comment">
            </form>
        """
    print("Incoming JSON Response")

    return JsonResponse({'messages_list': response})
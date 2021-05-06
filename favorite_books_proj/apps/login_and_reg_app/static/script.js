console.log("Script linked")

$(document).ready(function(){
    console.log("Document ready")
    console.log("Current URL: " + window.location.pathname)
    $('.error_row').attr('active', 'false')

    $('input').focusout(function(e){
        id = this.id
        console.log("Validating " + id)
        validate(id)
    });
    $('textarea').focusout(function(e){
        id = this.id
        console.log("Validating " + id)
        validate(id)
    });

    function validate(id){
        console.log("ID: " + id)
        id = '#' + id
        var value = $(id).val();
        var errorMessage = "";
        console.log(`"Validating ID ${id}: " + ${value}`)

        switch(id){
            case '#first_name':
            case '#last_name':
                if (value == NaN || value.length < 2 || value.length > 32){
                    errorMessage = "Must be between 2 and 32 characters"
                }
                break;
            case '#login_email':
            case '#email':
                re = /[A-Za-z0-9.-_+]+@[A-Za-z0-9.-_+]+\.[A-Za-z0-9]+/gm;
                if (re.test(value) == false){
                    errorMessage = "Invalid email"
                }
                break;
            case '#birthday':
                console.log("Birthday:" + value)
                if(value == ""){
                    errorMessage = "Please enter a birthday"
                }
                else if( age(value) < 13 ){
                    errorMessage = "Must be at least 13 years old"
                }
                break;
            case '#password':
                if (value.length < 8){
                    errorMessage = "Password must be at least 8 characters"
                }
                break;
            case '#confirm':
                if (value != $('#password').val()){
                    errorMessage = "No match"
                }
                break;
            case '#login_password':
                if (value.length < 1){
                    errorMessage = "Please enter a password"
                }
                break;
            case '#title':
                if (value.length < 1){
                    errorMessage = "Please enter a title"
                }
                break;
            case '#desc':
                if (value.length < 5){
                    errorMessage = "Description must be at least 5 characters"
                }
                break;
        }
        
        if (errorMessage != ""){
            console.log("Error message: " + errorMessage)
            $(id).css("background-color", "lightcoral");

            if ($(id).parent().parent().next('tr').children('.error_row').attr("active") == 'false'){
                $(id).parent().parent().next('tr').children('.error_row').append(`<span class="error">${errorMessage}</span>`).attr("active", 'true');
            }
            return 1;
        }
        else{
            console.log("No validation issues found")
            $(id).css("background-color", "white");
            $(id).parent().parent().next('tr').children('.error_row').attr("active", 'false').children().remove()
            return 0;
        }

    function age(birthday){
        var birthdayObject = new Date(birthday)
        var difference = Date.now() - birthdayObject.getTime();
        var ageDate = new Date(difference)
        var year = ageDate.getUTCFullYear();
        var age = Math.abs(year - 1970)
        return age;
        }
    }

    $('form').submit(function(){
        console.log("Form submit clicked")
        var errors = 0
        var form_id = "#" + $(this).attr('id')
        current_form = this
        
            // if (form_id == "#post_message"){
            //     $.post('/wall/message', $(this).serialize(), function(){
            //         $.get('/wall/message/recent', function(data){
            //             console.log(data['recent_message'])
            //             $('#messages_list').prepend(data['recent_message'])
            //             target = $('.message').first()
            //             $(target).hide()
            //             $('.post_comment').first().clone().appendTo(target)
            //             $(target).slideDown()
            //         });
            //     });
            // }
            // else{
            //     console.log("Submitting comment")
            //     $.post('/wall/comment', $(this).serialize(), function(){
            //         $.get('/wall/comment/recent', function(data){
            //             current_comments_list = $(current_form).siblings('.comments_list')
            //             $(current_comments_list).append(data['recent_comment'])
            //             target = $(current_comments_list).children('.comment').last()
            //             $(target).hide().slideDown()
            //         });
            //     });
            // }
        


        if (form_id == "#registration")
            submitUrl = "/user"
        else if (form_id == "#login")
            submitUrl = "/login"
        else if (form_id=="add-book")
            submitUrl = "/books/create"
        else if (form_id == "#book-info")
            submitUrl = window.location.pathname + "/update"
        
        $(form_id).find('input').each(function(){
            console.log(".each ID: " + $(this).attr('id'))
            errors += validate($(this).attr('id'));
        });
        $(form_id).find('textarea').each(function(){
            console.log("Finding textarea")
            console.log(".each ID: " + $(this).attr('id'))
            errors += validate($(this).attr('id'));
        });
        
        console.log(`There are ${errors} errors`)
        if (errors == 0){
            $.post( submitUrl, $(form_id).serialize(), function(){
                if (window.location.pathname == '/')
                    window.location.replace("/success")
            });
        }
        
        return false;
    });

    if(window.location.pathname == "/success"){
        console.log("Now in SUCCESS template");
        window.setTimeout(function(){
            console.log("Redirecting");
            window.location.href = "/books";
        }, 5000);
    }

    let re = /\/books\/\d+/

    if( re.test(window.location.pathname) ){
        console.log("Now in show_book template")

        //Get logged in user info
        //Get current book info
        $.get(window.location.pathname + '/info', function(data){
            $('#book-info').attr('action', `${data['book_id']}/update`)
            var title_field = "";
            var description_field = `<label for="description">Description: </label>`;
            var submit_field = "";

            if(data['uploaded_by_user']){
                title_field += `<input required class="edit-title" type="text" name="title" value="${data['book_title']}">`;
                description_field += `<textarea name="desc" id="desc" cols="32" rows="10">${data['book_desc']}</textarea>`
                submit_field += `<input class="submit-button" type="submit" value="Update">
                <button class="submit-button delete">Delete</button>`
            }
            else{
                title_field += `<h3>${data['book_title']}</h3>`
                description_field += `<i>${data['book_desc']}</i>`
                submit_field = NaN 
            }
            
            $('.title-field').append(title_field);
            $('.description-field').append(description_field)
            $('.submit-field').append(submit_field)

            $('.delete').click(function(){
                console.log("Clicked on delete")
                $('#wrapper').after(
                    `<div class="modal">
                    <h4>Are you sure?</h4>
                    <a href="${window.location.pathname + "/destroy"}" class="submit-button delete">Yes</a>
                    <button id="no" class="submit-button">No</button>
                    </div>`
                )

                // $('#wrapper').click(function(){
                //     console.log("Wrapper clicked")
                //     $('.modal').css("display", "none")
                // });
                $('#no').click(function(){
                    $('.modal').remove();
                });
                
            });
            
            // if(data['is_favorite'] == True){

            // }
        });
    }

});


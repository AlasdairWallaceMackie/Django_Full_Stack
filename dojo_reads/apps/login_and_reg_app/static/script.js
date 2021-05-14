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

        if (form_id == "#registration")
            submitUrl = "/users/create"
        else if (form_id == "#login")
            submitUrl = "/login"
        else
            return true;
        
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
                else if( /\/books\/\d+/.test(window.location.pathname) ){
                    window.location.replace("/books");
                }
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
    
    $('.delete').click(function(){
        console.log("Clicked on delete")
        $('#wrapper').append(
            `<div class="modal">
            <h4>Are you sure?</h4>
            <a href="${window.location.pathname + "/destroy"}" class="submit-button delete">Yes</a>
            <button id="no" class="submit-button">No</button>
            </div>`
        )

        // $('#wrapper').off()
        $('#wrapper').click(function(){
            console.log("Wrapper clicked")
            
            $('#no').click(function(){
                $('.modal').remove();
            });
            $('#wrapper').click(function(){
                $('.modal').remove();
            });
        });
        
        return false;
    });

        console.log("Hovering in editing field")
        $('.star').hover(function(){
            //Hover in
            if ($(this).parent().hasClass('edit')){
                drawStars($(this).attr('value'));
            }
        },function(){
            //Hover out
            if ($(this).parent().hasClass('edit')){
                drawStars($('#form-star-rating').attr('value'))           
            }
        });
    
        $('.star').click(function(){
            console.log("Star clicked")
            $('#form-star-rating').val($(this).attr('value'))
        });



    function drawStars(rating){
        $('.edit').children('.star').each(function(){
            $(this).attr('src', "/static/img/empty_star.png")
        });
        for( var i=1; i<=rating; i++ ){
            $(`.star[value=${i}]`).attr('src', "/static/img/filled_star.png")
        }
    }
});
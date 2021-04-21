$(document).ready(function(){

    $(document).click(function(){
        $('#error-messages').css("display", "none");
    });

    $('.remove').click(function(){
        console.log("Clicked REMOVE")
        
        courseID = $(this).attr('course-id'); 
        courseName = $(this).attr('course-name'); 

        $('#wrapper').after(
            `<div id="warning" class="modal">
                <h2>Warning</h2>
                <p>Are you sure you want to delete <b>${courseName}</b>?
                <br><br><br>
                <button class="styled-button button-no">No</button>
                <a href="/courses/${courseID}/destroy" class="delete-button styled-button">Yes! I want to delete this</a>
            </div>`
        )

        $('#wrapper').click(function(){
            $('#warning').remove()
        });
        $('.button-no').click(function(){
            console.log("Clicked NO")
            $('#warning').remove()
        });
        $('delete_button').click(function(){
            //
        });


        return false;
    });

});
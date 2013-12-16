(function(){
    /**
     * Handle profile password reset
     */
    $('#profile-pass-change').submit(function(e){
        e.preventDefault();
        var old_password = $('#old_password').val();
        var new_password = $('#new_password').val();
        var data = {
            'old_password': old_password,
            'new_password': new_password,
            'api_key': api_key
        };
        $.ajax({
          type: 'PATCH',
          crossDomain: true,
          url: api_url + '/api/v1/users/' + user_id + '/password',
          data: JSON.stringify(data),
          contentType: 'application/json',
          success: function (response, status, xhr) {
            console.log("Success!!");
            console.log(response.data);
            console.log(xhr.status);
            if (xhr.status === 200) {
                window.location.href = '/music';
                //$(this).hide();
            } else {
                // response.form contains the HTML for the replacement form
                console.log(response.message)
                $("#new_password").replaceWith(response.message);
            }
          },
          error: function (xhr, desc, err) {
            console.log(xhr);
            console.log("Desc: " + desc + "\nErr:" + err);
            if (xhr.status === 400 || xhr.status === 401) {
                alert(err);
            } else {
                alert("The service is currently unavailable. Please try again.");
            }
          }
        });
    });

    /**
     * Handle facebook connect
    */
    $("#profile-connect-facebook").submit(function(e){
        e.preventDefault();
        window.location = '/auth/logout';
    });
    
})();

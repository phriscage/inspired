(function(){
    /**
     * Handle submit for user
     */
    $('#email-signup-container-form').submit(function(e){
        e.preventDefault();
        var first_name = $('#first_name').val();
        var last_name = $('#last_name').val();
        var email_address = $('#email_address').val();
        var password = $('#password').val();
        var data = {
            'first_name': first_name,
            'last_name': last_name,
            'email_address': email_address,
            'password': password
        };
        $.ajax({
          type: 'POST',
          crossDomain: true,
          url: api_url + '/api/v1/users',
          data: JSON.stringify(data),
          contentType: 'application/json',
          success: function (response, status, xhr) {
            console.log("Success!!");
            console.log(response.data);
            console.log(xhr.status);
            if (xhr.status === 201) {
                // response.redirect contains the string URL to redirect to
                window.location.href = '/auth/login';
            } else {
                // response.form contains the HTML for the replacement form
                $("#first_name").replaceWith(response.message);
            }
          },
          error: function (xhr, desc, err) {
            console.log(xhr);
            console.log("Desc: " + desc + "\nErr:" + err);
          }
        });
    });
})();

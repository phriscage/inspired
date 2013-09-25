(function(){
    /**
     * Handle submit for user
     */
    $('#email-login-container-form').submit(function(e){
        e.preventDefault();
        var email_address = $('#email_address').val();
        var password = $('#password').val();
        var data = {
            'email_address': email_address,
            'password': password
        };
        $.ajax({
          type: 'POST',
          url: '/auth/login',
          data: JSON.stringify(data),
          contentType: 'application/json',
          success: function (response, status, xhr) {
            console.log("Success!!");
            console.log(response.data);
            console.log(xhr.status);
            if (xhr.status === 200 && response.code == 302) {
                // response.redirect contains the string URL to redirect to
                window.location.href = response.url;
            } else {
                // response.form contains the HTML for the replacement form
                console.log(response.message)
                $("password").replaceWith(response.message);
            }
          },
          error: function (xhr, desc, err) {
            console.log(xhr);
            console.log("Desc: " + desc + "\nErr:" + err);
          }
        });
    });
})();

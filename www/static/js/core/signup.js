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
          url: api_url,
          data: JSON.stringify(data),
          contentType: 'application/json',
          success: function (response, status) {
            console.log("Success!!");
            console.log(response.data);
            if (response.code === 302) {
                // response.redirect contains the string URL to redirect to
                window.location.href = response.url;
            } else {
                // response.form contains the HTML for the replacement form
                $("#email-login-container-form").replaceWith(response.form);
            }
          },
          error: function (xhr, desc, err) {
            console.log(xhr);
            console.log("Desc: " + desc + "\nErr:" + err);
          }
        });
    });
})();

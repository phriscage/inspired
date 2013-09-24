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
          url: 'http://api-dev.inspiredapp.tv:8001/api/v1/users/',
          crossDomain: true,
          data: JSON.stringify(data),
          contentType: 'application/json',
          success: function (data, status) {
            console.log("Success!!");
            console.log(data);
            console.log(status);
          },
          error: function (xhr, desc, err) {
            <!--console.log(xhr);-->
            console.log("Desc: " + desc + "\nErr:" + err);
          }
        });
    });
})();

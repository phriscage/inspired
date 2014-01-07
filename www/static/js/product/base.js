(function(){
    /**
     * Handle product data population
     */
    if (typeof product_id == 'undefined') {
        alert("The product_id is not available. Please try again.");
    };
    var data = {
        'api_key': api_key
    };
    $.ajax({
      crossDomain: true,
      url: api_url + '/api/v1/products/' + product_id,
      data: data,
      contentType: 'application/json',
      //statusCode: {
        //404: function() {
          //alert("Item is not found");
          ////window.location.href = '/404';
        //},
      //},
      success: function (response, status, xhr) {
        console.log("Success!!");
        console.log(response.data);
        console.log(response.message);
        console.log(xhr.status);
        //if (xhr.status === 200) {
            //$(this).hide();
            // response.form contains the HTML for the replacement form
            //console.log(response.message)
            //$("#new_password").text(response.data);
        //}
      },
      error: function (xhr, desc, err) {
        console.log("Error");
        console.log(xhr);
        var response_json = xhr.responseJSON;
        console.log(response_json);
        console.log(xhr.responseText);
        $('.product-brand').html(response_json.message);
        $('.product-model').html(xhr.responseText);
        //if (xhr.status === 400 || xhr.status === 401) {
            //alert(err);
        //} else {
            //alert("The service is currently unavailable. Please try again.");
        //}
      }
    });

})();

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
        
        /*  creating the foundation data-clearing ul does not seem to work 
        *   so updating the li.clearing-featured-img instead for now
        */
        
        //var ul = $('<ul data-clearing>').addClass('clearing-thumbs clearing-feature product-image');
        $.each(response.data.product_images, function(i, item) {
            var image_url = window.location.origin + item.url;
            var $li, $img, $a;
            if (i === 0) {
                $img = $('<img>').attr('src', image_url);
                $a = $('<a>').attr('href', image_url).append($img);
                //$li = $('<li>').addClass('clearing-featured-img').css({background: "yellow"}).append($a);
                //$li = $('<li>').addClass('clearing-featured-img').append($a);
                $('li.clearing-featured-img').append($a);
                
            } else {
                $img = $('<img>').attr('src', image_url);
                $a = $('<a>').attr('href', image_url).append($img);
                $li = $('<li>').append($a);
                //console.log($li[0].outerHTML)
                //$('li.clearing-other-img').append($a);
                $('ul.clearing-thumbs clearing-feature product-image').append($li);
                //$('.test').append($li);
            }
            //$('ul.clearing-thumbs clearing-feature product-image').append($li);
            //ul.append($li);
        });
        //$('#product-images').html(ul);
        //$('#product-images').html(ul[0].outerHTML);
        $('.product-brand').html(response.data.brand);
        $('.product-model').html(response.data.model);
        $('.product-description').html(response.data.description);
      },
      error: function (xhr, desc, err) {
        console.log("Error");
        console.log(xhr);
        var response = xhr.responseJSON;
        console.log(response);
        console.log(xhr.responseText);
        $('.product-brand').html(response.message);
        //if (xhr.status === 400 || xhr.status === 401) {
            //alert(err);
        //} else {
            //alert("The service is currently unavailable. Please try again.");
        //}
      }
    });

})();

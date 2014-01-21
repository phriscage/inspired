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
        
        /*  create the product images and product metadata for the product-page
        */
        
        var columns1, columns2, product_images, product_brand, product_model;
        var product_description;
        columns1 = $('<div>').addClass('small-6 large-5 columns');
        product_images = $('<ul data-clearing>').addClass(
            //'clearing-thumbs clearing-feature product-image').attr('data-clearing',null);
            'clearing-thumbs clearing-feature product-image');
        $.each(response.data.product_images, function(i, item) {
            var image_url = window.location.origin + item.url;
            var $product_li, $product_img, $product_a;
            if (i === 0) {
                $product_img = $('<img>').attr('src', image_url);
                $product_a = $('<a>').attr('href', image_url).append($product_img);
                $product_li = $('<li>').addClass('clearing-featured-img').css(
                    {background: "yellow"}).append($product_a);
            } else {
                $product_img = $('<img>').attr('src', image_url);
                $product_a = $('<a>').attr('href', image_url).append($product_img);
                $product_li = $('<li>').append($product_a);
            }
            console.log($product_li[0]);
            product_images.append($product_li);
        });
        var maximize_img = $('<img>').attr('src', window.location.origin + '/static/img/maximize.svg').css({type: 'image/svg+xml'});
        var maximize_btn = $('<div>').addClass('maximize-btn').append(maximize_img);
        columns1.append(product_images, maximize_btn);
        console.log(columns1[0]);
        columns2 = $('<div>').addClass('small-6 large-7 columns');
        product_brand = $('<div>').addClass('product-brand').html(response.data.brand);
        product_model = $('<div>').addClass('product-model').html(response.data.model);
        product_description = $('<div>').addClass('product-description').html(response.data.description);
        columns2.append(product_brand, product_model, product_description);
        $('#product-page').append(columns1, columns2);
        
        /*  insert the product_retailers from the response.data.product_retailers
        *   and parent retailer data.
        */
        $.each(response.data.product_retailers, function(i, item) {
            var retailer_image_url = window.location.origin + item.retailer.image_url;
            var $column1, $column2, $column3;
            var $row, $retailer, $retailler_btn, $columns, $retailler_img, $retailler_price;
            $retailler_price = $('<div>').addClass('retailer-price').html(item.price);
            $retailler_img = $('<img>').attr('src', retailer_image_url);
            $columns = $('<div>').addClass('columns').css({padding: 0})
            $columns.append($retailler_img, $retailler_price);
            $retailler_btn = $('<div>').addClass('retailer-btn').attr('data-src', 
                item.url).append($columns);
            $column2 = $('<div>').addClass('small-10 large-6 columns');
            $column2.append($retailler_btn);
            $column1 = $('<div>').addClass('small-1 large-3 columns').css(
                {color: '#fff'}).html('.');
            $column3 = $('<div>').addClass('small-1 large-3 columns').css(
                {color: '#fff'}).html('.');
            $row = $('<div>').addClass('row');
            $row.append($column1, $column2, $column3)
            console.log($row[0]);
            $('#retailer-list').append($row);
        });
      },
      error: function (xhr, desc, err) {
        console.log("Error");
        console.log(xhr);
        var response = xhr.responseJSON;
        console.log(response);
        console.log(xhr.responseText);
        //if (xhr.status === 400 || xhr.status === 401) {
            //alert(err);
        //} else {
            //alert("The service is currently unavailable. Please try again.");
        //}
      }
    });

})();

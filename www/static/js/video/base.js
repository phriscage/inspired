(function(){
    /**
     * Handle video data population
     */
    if (typeof video_id == 'undefined') {
        alert("The video_id is not available. Please try again.");
    };
    var data = {
        'api_key': api_key
    };
    $.ajax({
      crossDomain: true,
      url: api_url + '/api/v1/videos/' + video_id,
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
        
        /*  create the video page title
        */
        
        var video_poster_iframer_src = '//www.youtube-nocookie.com/embed/' + response.data.video_sources[0].source_id + '?rel=0';
        var video_poster = $('<iframe>').attr({width: '320', height: '240', src: video_poster_iframer_src, 
            frameborder: '0', allowfullscreen: ''});
        $('.video-poster').append(video_poster);

        var product_style;
        var count = 1;
        var look_columns, look_title, look_componsition, look_mark;
        $.each(response.data.products, function(i, product) {
            if (typeof product_style === 'undefined') {
                console.log("defining product_style");
                product_style = product.product_style.name;
                look_columns = $('<div>').addClass('look small-11 small-centered columns');
                look_title = $('<div>').addClass('look-title').html('Look ' + count);
                look_componsition = $('<div>').addClass('look-composition premium-look');
                look_mark = $('<div>').addClass('look-mark').html(product_style);
                look_componsition.append(look_mark);
                look_columns.append(look_title);
            }
            console.log(product_style);
            var $look_item, $look_item_image_url, $look_item_img, $look_item_info, $look_item_brand, $look_item_model;
            $look_item = $('<a>').attr('href', product.uri).addClass('look-item');
            $look_item_image_url = window.location.origin + product.product_images[0].url;
            $look_item_img = $('<img>').addClass('look-item-img').attr('src', $look_item_image_url);
            $look_item_info = $('<div>').addClass('look-item-info');
            $look_item_brand = $('<div>').addClass('look-item-brand').html(product.brand);
            $look_item_model = $('<div>').addClass('look-item-model').html(product.model);

            $look_item_info.append($look_item_brand, $look_item_model);
            $look_item.append($look_item_img, $look_item_info);

            if (product_style !== product.product_style.name) {
             //   console.log(product_style, product.product_style.name);
                look_columns.append(look_componsition);
                look_columns.append($('<div>').addClass('look-separator'));
                $('#looks-container').append(look_columns);

                count += 1;
                product_style = product.product_style.name;
                look_columns = $('<div>').addClass('look small-11 small-centered columns');
                look_title = $('<div>').addClass('look-title').html('Look ' + count);
                look_componsition = $('<div>').addClass('look-composition premium-look');
                look_mark = $('<div>').addClass('look-mark').html(product_style);
                look_componsition.append(look_mark);
                look_columns.append(look_title);
            }
            look_componsition.append($look_item);
        });
        look_columns.append(look_componsition);
        $('#looks-container').append(look_columns);
        
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

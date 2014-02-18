(function(){
    /**
     * Handle artist data population
     */
    if (typeof artist_id == 'undefined') {
        alert("The artist_id is not available. Please try again.");
    };
    var data = {
        'api_key': api_key
    };
    $.ajax({
      crossDomain: true,
      url: api_url + '/api/v1/artists/' + artist_id,
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
        
        /*  create the artist page title
        */
        
        var artist_image_url = window.location.origin + response.data.image_url
        var artist_img = $('<img>').attr('src', artist_image_url);
        $('.artist-poster').append(artist_img);
        var artist_page_band = $('<span>').html(response.data.name + ' Music Videos');
        $('.artist-page-band').append(artist_page_band);

        $.each(response.data.videos, function(i, video) {
            var $video, $video_img, $video_info, $video_title, $artist_name;
            $video = $('<a>').attr('href', '/video/1').addClass('four columns artist-video-btn');
            // need to create a video image_url
            $video_img = $('<img>').addClass('video-img').attr('src', artist_image_url);
            $video_info = $('<div>').addClass('video-info');
            $video_title = $('<div>').addClass('video-title').html(video.name);
            $artist_name = $('<div>').addClass('artist-name').html(response.data.name);
            $video_info.append($video_title, $artist_name);
            $video.append($video_img, $video_info);
            $('#artist-video-list').append($video);
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

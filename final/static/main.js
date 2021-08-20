

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};


function like(pk) {
    fetch('/like', {
          method: 'POST',
          headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Accept": "application/json",
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
              'pk': pk
          })
        })
        .then(response => response.json())
        .then(result => {
            // Print result
            console.log(result);

            if (result.already_liked == true) {

                label = document.getElementById(`${pk}-label`);
                console.log(label)
                label.innerHTML= 'Already liked!';
            }

            else if (result.already_liked == false) {
                new_count = document.getElementById(`${pk}`);
                new_count.innerHTML = result.new_like_count;
                console.log(result.new_like_count);
            }
            //lbut = document.getElementById(`${arg}-label`);
        
           // count_field = document.getElementById(`${arg}`);

            //lbut.innerHTML = result.lbutsays

            //count_field.innerHTML = result.new_count
    
        });
        
    };

function like(pk) {
    fetch('/like', {
          method: 'POST',
          headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Accept": "application/json",
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
              'pk': pk
          })
        })
        .then(response => response.json())
        .then(result => {
            // Print result
            console.log(result);

            if (result.already_liked == true) {

                label = document.getElementById(`${pk}-label`);
                console.log(label)
                label.innerHTML= 'Already liked!';
            }

            else if (result.already_liked == false) {
                new_count = document.getElementById(`${pk}`);
                new_count.innerHTML = result.new_like_count;
                console.log(result.new_like_count);
            }
            //lbut = document.getElementById(`${arg}-label`);
        
           // count_field = document.getElementById(`${arg}`);

            //lbut.innerHTML = result.lbutsays

            //count_field.innerHTML = result.new_count
    
        });
        
    };

    function vehlike(pk) {
        fetch('/vehlike', {
              method: 'POST',
              headers: {
                "X-CSRFToken": getCookie("csrftoken"),
                "Accept": "application/json",
                'Content-Type': 'application/json'
              },
              body: JSON.stringify({
                  'pk': pk
              })
            })
            .then(response => response.json())
            .then(result => {
                // Print result
                console.log(result);
    
                if (result.already_liked == true) {
    
                    label = document.getElementById(`${pk}-label`);
                    console.log(label)
                    label.innerHTML= 'Already liked!';
                }
    
                else if (result.already_liked == false) {
                    new_count = document.getElementById(`${pk}`);
                    new_count.innerHTML = result.new_like_count;
                    console.log(result.new_like_count);
                }
                //lbut = document.getElementById(`${arg}-label`);
            
               // count_field = document.getElementById(`${arg}`);
    
                //lbut.innerHTML = result.lbutsays
    
                //count_field.innerHTML = result.new_count
        
            });
            
        };






function messenger() {
    element = document.getElementById('messenger_div');

    if (element.style.display == "none") 
    {
        element.style.display = "block";
    }
    else
    {
        element.style.display = "none";          
    }
};



function confirmdelete(pk) {
    element = document.getElementById(`${pk}-delete`);
    confirm_button = document.getElementById(`${pk}-confirm`);


    if (element.innerHTML == "Delete") 
    {
        element.innerHTML = "Cancel";
        confirm_button.style.display = "block"
    }
    else
    {
        element.innerHTML= "Delete";      
        confirm_button.style.display = "none"
    
    }

}



function deletemessage(pk) {
    console.log(pk);

    fetch('/deletemessage', {
          method: 'POST',
          headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Accept": "application/json",
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
              'pk': pk
          })
        })
        .then(response => response.json())
        .then(result => {
            // Print result
            console.log(result);

        
            message = document.getElementById(`${pk}`)
            message.style.display = "none";
            })

          
        };
        


function projectpreview(name) {
    console.log(name);
    fetch('/projectpreview', {
          method: 'POST',
          headers: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Accept": "application/json",
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
              'name': name
          })
        })
        .then(response => response.json())
        .then(data => JSON.parse(data) )
        .then(result => {
            console.log(result);
          
            $('#exteriorimage').attr('src', result.exterior_image)
            $('#interiorimage').attr('src', result.exterior_image)
            $('#fullbuildpage').attr('href', result.fullbuildpage)
            $('#owner').attr('href', 'profile/' + result.owner)
            $('#description').append(result.description)


            })

          
        };


function handleReply(response_id) {
    const reply_form_container = document.querySelector(`#reply-form-container-${response_id}`)
    if (reply_form_container) {
        reply_form_container.style.display = 'block';
    }
}

function handleCancel(response_id) {
    const reply_form_container = document.querySelector(`#reply-form-container-${response_id}`)
    if (reply_form_container) {
        reply_form_container.style.display = 'none';
    }
}

$(document).ready(function(){


    fullWidth = true

    $('.hideSidebar').on('click', function() {

        if (fullWidth == true) {

            $('body').css('--sidebarwidth', '33px');
            console.log($('body'))
            fullWidth = false
            $('.hideSidebar').toggle()
        }
        else {
            $('body').css('--sidebarwidth', '300px');
            fullWidth = true
            $('.hideSidebar').toggle()

        }
    })


    $('.dropdown-tree').on('click', function () {
        
    
        $('.myUL').toggle('slow');
        $('.dropdown-img-tree').toggleClass('dropdown-img-up');
    })

    $('#function_selection').on('change', function() {
        console.log(this.value);
 
        $(location).attr('href', '/furniturebytype/'+this.value);

            });
  
            $('#function_selection2').on('change', function() {
                console.log(this.value);
         
                $(location).attr('href', '/furniturebytype/'+this.value);
        
                    });
          
              
        
         
        
    




    $('.tree-link').one('click', function(){
        console.log(this)
        projectpreview(this.id); 
                    });


                    var toggler = document.getElementsByClassName("caret");
                    var i;
                    console.log(toggler);
                  
                    for (i = 0; i < toggler.length; i++) {
                        toggler[i].addEventListener("click", function() {
                        console.log('clickedtoggler');
                        this.parentElement.querySelector(".nested").classList.toggle("active");
                        console.log(this.classList)
                        this.classList.toggle("caret-down");
                         });
                         }
  
               //exterior images     
    $('.carousel__button--right').on('click', function (event) {
        var currentImg = $('.show');
        var annotation = $('#image_annotation');
        var nextImg = currentImg.next();
        if(nextImg.length) {
            nextImg.addClass('show');
            currentImg.removeClass('show');
            var newText = nextImg.attr('alt');
            annotation.text(newText);
        }
        else if(!nextImg.length) {
        
            nextImg = $('.carousel__track img').first();
            nextImg.addClass('show');
            currentImg.removeClass('show');
            var newText = nextImg.attr('alt');
            annotation.text(newText);
        }

    })

    $('.carousel__button--left').on('click', function () {
        var currentImg = $('.show');
        var annotation = $('#image_annotation');
        var nextImg = currentImg.prev();
        if(nextImg.length) {
            nextImg.addClass('show');
            currentImg.removeClass('show');
            var newText = nextImg.attr('alt');
            annotation.text(newText);
        }
        else if(!nextImg.length) {
            console.log('prevsecondelse')
            nextImg = $('.carousel__track img').last();
            nextImg.addClass('show');
            currentImg.removeClass('show');
            var newText = nextImg.attr('alt');
            annotation.text(newText);
        }

    })

    //room images

$.each([1,2,3,4,5,6,7], function(i) {
    
    $('.carousel__button--right'+[i]).on('click', function () {
        var currentImg = $('.show'+[i]);
        var annotation = $('#image_annotation'+[i]);
        var nextImg = currentImg.next();
        if(nextImg.length) {
            console.log('clicke'+[i])
            nextImg.addClass('show'+[i]);
            currentImg.removeClass('show'+[i]);
            var newText = nextImg.attr('alt');
            annotation.text(newText);
        }
        else if(!nextImg.length) {
            console.log('clickendendende'+[i])
            nextImg = $('.carousel__track'+[i]).children('img').first();
            nextImg.addClass('show'+[i]);
            currentImg.removeClass('show'+[i]);
            var newText = nextImg.attr('alt');
            annotation.text(newText);
        }

    })

    $('.carousel__button--left'+[i]).on('click', function () {
        var currentImg = $('.show'+[i]);
        var annotation = $('#image_annotation'+[i]);
        var nextImg = currentImg.prev();
        if(nextImg.length) {
            nextImg.addClass('show'+[i]);
            currentImg.removeClass('show'+[i]);
            var newText = nextImg.attr('alt');
            annotation.text(newText);
        }
        else if(!nextImg.length) {
            console.log('prevsecondelse')
            nextImg = $('.carousel__track'+[i]).children('img').last();
            nextImg.addClass('show'+[i]);
            currentImg.removeClass('show'+[i]);
            var newText = nextImg.attr('alt');
            annotation.text(newText);
        }

    })
})

$.each([0,1,2,3,4,5,6,7], function(i) {
    
    let x = i;
    $('.dropdown'+[i]).on('click', function (i) {
        
    
        $('.picture-section'+[x]).toggle('slow');
        $('.dropdown-img'+[x]).toggleClass('dropdown-img-up');
    })
});
                  

$('#search-modal-button').on('click', function () {
    console.log('modalopenclicked');

    $('#search-modal').toggle();
});

$('.close1').on('click', function () {

    console.log('clicked');

    $('#search-modal').toggle();

});





                 });
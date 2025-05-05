$(document).ready(function(){
    // offcanvas
    $(document).on('click', '#offcanvas-dismiss-cart, #offcanvas-dismiss-menu, .offcanvas-overlay', function () {
        $('.offcanvas').removeClass('active');
        $('body').removeClass('offcanvas-page');
        $('.offcanvas-overlay').removeClass('active');
    });

    $('#offcanvas-trigger-cart').on('click', function () {
        $('#offcanvasCart').addClass('active');
        $('body').addClass('offcanvas-page');
        $('.offcanvas-overlay').addClass('active');
    });
    // offcanvas
    // responsiveMenu
    $('.dropdown-toggle').on('click', function(e) {
      e.stopPropagation();
      e.preventDefault();

      var self = $(this);
      if (self.is('.disabled, :disabled')) {
        return false;
      }
      self.parent().toggleClass("open");
    });

    $(document).on('click', function(e) {
      if ($('.dropdown').hasClass('open')) {
        $('.dropdown').removeClass('open');
      }
    });

    $('.nav-btn.nav-slider').on('click', function() {
      $('.overlay').show();
      $('nav').toggleClass("open");
    });

    $('.overlay').on('click', function() {
      if ($('nav').hasClass('open')) {
        $('nav').removeClass('open');
      }
      $(this).hide();
    });


      $('li.active').addClass('open').children('ul').show();
      $("li.has-sub > a").on('click', function () {
          $(this).removeAttr('href');
          var e = $(this).parent('li');
          if (e.hasClass('open')) {
              e.removeClass('open');
              e.find('li').removeClass('opne');
              e.find('ul').slideUp(200);
          }
          else {
              e.addClass('open');
              e.children('ul').slideDown(200);
              e.siblings('li').children('ul').slideUp(200);
              e.siblings('li').removeClass('open');
              e.siblings('li').find('li').removeClass('open');
              e.siblings('li').find('ul').slideUp(200);
          }
      });
    // responsiveMenu

    $('.dropdown-toggle').dropdown();

    //    quantity-selector
        jQuery('<div class="quantity-nav"><div class="quantity-button quantity-up">+</div><div class="quantity-button quantity-down">-</div></div>').insertAfter('.quantity input');
        jQuery('.quantity').each(function() {
        var spinner = jQuery(this),
            input = spinner.find('input[type="number"]'),
            btnUp = spinner.find('.quantity-up'),
            btnDown = spinner.find('.quantity-down'),
            min = input.attr('min'),
            max = input.attr('max');

        btnUp.click(function() {
            var oldValue = parseFloat(input.val());
            if (oldValue >= max) {
            var newVal = oldValue;
            } else {
            var newVal = oldValue + 1;
            }
            spinner.find("input").val(newVal);
            spinner.find("input").trigger("change");
        });

        btnDown.click(function() {
            var oldValue = parseFloat(input.val());
            if (oldValue <= min) {
            var newVal = oldValue;
            } else {
            var newVal = oldValue - 1;
            }
            spinner.find("input").val(newVal);
            spinner.find("input").trigger("change");
        });

        });
    //    quantity-selector
        $("nav.navbar ul.navbar-ul li.nav-item ul.mega-menu li.menu-mega-item .mega-menu-sublist-row").hover(function(){
            $(this).siblings().removeClass('active');
            $(this).addClass('active');
        });

        //    hover-menu-overlay
           $('li.nav-overlay').hover(function(){
            $('.mega-menu').removeClass('active');
            $('.nav-categories-overlay').addClass('active');
        },function(){
            $('.nav-categories-overlay').removeClass('active');
        });

        // card-instant-offer
        var swiper = new Swiper('.swiper-suggestion', {
            autoplay: {
                delay: 3000,
                disableOnInteraction: false,
            },
            slidesPerView: 1,
            spaceBetween: 30,
            loop: true,
            navigation: {
              nextEl: '.swiper-button-next',
              prevEl: '.swiper-button-prev',
            },
        });

        // tab
        $(".checkbox-more-handler a").on('click',function(e){
            e.preventDefault();
            $(".checkbox-more").slideToggle(200);
            $(this).find('.show-more').fadeToggle(0);
            $(this).find('.show-less').fadeToggle(0);
        });

        // sidebar-sticky
        if ($('.sticky-sidebar').length) {
            $('.sticky-sidebar').theiaStickySidebar();
        }

        // add-product-wishes
        $(".product .product-info .product-headline .product-wishes .btn-icon-dark").on("click",function () {
            $(this).toggleClass("active");
        });

        //    price-range
        var nonLinearStepSlider = document.getElementById('slider-non-linear-step');

        if($('#slider-non-linear-step').length) {
            noUiSlider.create(nonLinearStepSlider, {
                start: [0, 5000000],
                connect: true,
                direction: 'rtl',
                format: wNumb({
                    decimals: 0,
                    thousand: ','
                }),
                range: {
                    'min': [0],
                    '10%': [500, 500],
                    '50%': [40000, 1000],
                    'max': [10000000]
                }
            });
            var nonLinearStepSliderValueElement = document.getElementById('slider-non-linear-step-value');
            var minPriceInput = document.getElementById('min-price');
            var maxPriceInput = document.getElementById('max-price');

            nonLinearStepSlider.noUiSlider.on('update', function (values) {
                nonLinearStepSliderValueElement.innerHTML = values.join(' - ');

                minPriceInput.value = values[0].replace(',', '');
                maxPriceInput.value = values[1].replace(',', '');
            });
        }

        // slider-main
        var swiper = new Swiper('.swiper-container-main', {
            spaceBetween: 30,
            loop: true,
            responsive: true,
            centeredSlides: true,
            autoplay: {
              delay: 2500,
              disableOnInteraction: false,
            },
            pagination: {
              el: '.swiper-pagination',
              clickable: true,
            },
            navigation: {
              nextEl: '.swiper-button-next',
              prevEl: '.swiper-button-prev',
            },
        });

        // slider-product
        if ($('.swiper-container-product').length) {
          var swiper = new Swiper('.swiper-container-product', {
            slidesPerView: 4,
            loop: false,
            navigation: {
              nextEl: '.swiper-button-next',
              prevEl: '.swiper-button-prev',
            },
            keyboard: {
              enabled: true,
            },
            breakpoints: {
              300: {
                slidesPerView: 1,
                spaceBetween: 1,
                allowSlidePrev: true,
                allowSlideNext: true,
                mousewheel: true,
                keyboard: true
              },
              470: {
                slidesPerView: 1,
                spaceBetween: 5,
                allowSlidePrev: true,
                allowSlideNext: true,
                mousewheel: true,
                keyboard: true
              },
              640: {
                slidesPerView: 2,
                spaceBetween: 10,
                allowSlidePrev: true,
                allowSlideNext: true,
                mousewheel: true,
                keyboard: true
              },
              768: {
                slidesPerView: 3,
                spaceBetween: 30,
                allowSlidePrev: true,
                allowSlideNext: true,
                mousewheel: true,
                keyboard: true
              },
              1024: {
                slidesPerView: 4,
                spaceBetween: 40,
                allowSlidePrev: true,
                allowSlideNext: true,
                mousewheel: true,
                keyboard: true
              },
              1400: {
                slidesPerView: 5,
                spaceBetween: 50,
                allowSlidePrev: true,
                allowSlideNext: true,
                mousewheel: true,
                keyboard: true
              },
            }
          });
        }
        //
        // // product-more
        // var swiper = new Swiper('.swiper-container-more', {
        //     slidesPerView: 1,
        //     spaceBetween: 30,
        //     loop: true,
        //     pagination: {
        //       el: '.swiper-pagination',
        //       clickable: true,
        //     },
        //     navigation: {
        //       nextEl: '.swiper-button-next',
        //       prevEl: '.swiper-button-prev',
        //     },
        // });
            $(document).ready(function() {
            // هنگام باز شدن modal، swiper جدید را برای هر modal راه‌اندازی می‌کنیم.
            $('.modal').on('shown.bs.modal', function() {
                var productId = $(this).attr('id').split('-')[1]; // استخراج id محصول از id modal
                var swiper = new Swiper('#swiper-container-' + productId, {
                    slidesPerView: 1,
                    spaceBetween: 10,
                    loop: true,  // برای گردش دایره‌ای
                    pagination: {
                        el: '.swiper-pagination',
                        clickable: true,
                    },
                    navigation: {
                        nextEl: '.swiper-button-next',
                        prevEl: '.swiper-button-prev',
                    },
                });
            });
        });

        // modalgallery-swiper
        $( function() {
          $( '#gallery' ).jGallery();
        });
        $( function() {
          $('.album').jGallery({
          autostart: true,
          zoomSize: '100%'
          });
        });

        // modal-active-swiper
        $('#exampleModal').on('shown.bs.modal', function(e) {
            swiper.update();
           var $invoker = $(e.relatedTarget);
             swiper.slideTo($invoker.data('slider'));
             swiper.update();
        });

        // gallery
        var galleryThumbs = new Swiper('.product .product-gallery .gallery-thumbs', {
            spaceBetween: 10,
            slidesPerView: 3,
            loop: false,
            freeMode: true,
            loopedSlides: 5, //looped slides should be the same
            watchSlidesVisibility: true,
            watchSlidesProgress: true,
            breakpoints: {
              300: {
                slidesPerView: 1,
                spaceBetween: 1,
                allowSlidePrev: true,
                allowSlideNext: true,
                mousewheel: true,
                keyboard: true
              },
              470: {
                slidesPerView: 1,
                spaceBetween: 5,
                allowSlidePrev: true,
                allowSlideNext: true,
                mousewheel: true,
                keyboard: true
              },
              640: {
                slidesPerView: 2,
                spaceBetween: 10,
                allowSlidePrev: true,
                allowSlideNext: true,
                mousewheel: true,
                keyboard: true
              },
              768: {
                slidesPerView: 2,
                spaceBetween: 3,
                allowSlidePrev: true,
                allowSlideNext: true,
                mousewheel: true,
                keyboard: true
              },
              1024: {
                slidesPerView: 3,
                spaceBetween: 4,
                allowSlidePrev: true,
                allowSlideNext: true,
                mousewheel: true,
                keyboard: true
              },
              1400: {
                slidesPerView: 3,
                spaceBetween: 5,
                allowSlidePrev: true,
                allowSlideNext: true,
                mousewheel: true,
                keyboard: true
              },
            }
        });
        var galleryTop = new Swiper('.product .product-gallery .gallery-top', {
            spaceBetween: 10,
            loop: false,
            loopedSlides: 5, //looped slides should be the same
            navigation: {
              nextEl: '.swiper-button-next',
              prevEl: '.swiper-button-prev',
            },
            thumbs: {
              swiper: galleryThumbs,
            },
        });

        //    verify-phone-number
        if($("#countdown-verify-end").length) {
          var $countdownOptionEnd = $("#countdown-verify-end");
  
          $countdownOptionEnd.countdown({
          date: (new Date()).getTime() + 180 * 1000, // 1 minute later
          text: '<span class="day">%s</span><span class="hour">%s</span><span>: %s</span><span>%s</span>',
          end: function() {
              $countdownOptionEnd.html("<a href='' class='link-border-verify form-account-link'>دریافت مجدد کد تأیید</a>");
          }
          });
          }
          $(".line-number-account").keyup(function(){
              $(this).next().focus();
        });

        // profile
        $(".content-expert-button").click(function (e) {
            e.preventDefault();
            var sumaryBox = $(this).parents('.content-expert-article');
            sumaryBox.find('.content-expert-article').toggleClass('active');
            sumaryBox.find('.content-expert-text').fadeToggle(2);
            $(this).find('.show-more').fadeToggle(0);
            $(this).find('.show-less').fadeToggle(0);
        });

        // kamadatepicker
        kamaDatepicker('test-date-id-one', { buttonsColor: "red", forceFarsiDigits: true });
        kamaDatepicker('test-date-id-two', { buttonsColor: "red", forceFarsiDigits: true });

        // scrolltop
        $(document).on("scroll",function(){
          var st=$(this).scrollTop();
          if(st>200){
              $(".scrolltop").fadeIn(300,"swing");
          }
          else if(st<200){
              $(".scrolltop").fadeOut(300,"swing");
          }
        });
        $(".scrolltop").on("click",function(){
          $("html,body").animate({scrollTop:"0px"},1000,"swing");
        });

});


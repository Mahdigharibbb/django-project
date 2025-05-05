// $(document).ready(function (){
//     $('#add-cart-in').click(function (){
//         var button = $(this);
//         var productId = $(this).data("id");
//
//         $.ajax({
//             type: 'POST',
//             url: 'cart/',
//             data: {'csrfmiddlewaretoken': '{{ csrf_token }}'},
//                 success: function (data) {
//                     $('#item_count').text(data.item_count);
//                     $('#total_price').text(data.total_price);
//             },
//         });
//     });
// });

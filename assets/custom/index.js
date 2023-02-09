$(".inc-btn").click(function (e) {
    e.preventDefault();

    let inc_value = $(".quantity-input").val();
    let value = parseInt(inc_value, 10);
    value = isNaN(value) ? 0 : value;

    if (value < 10) {
      value++;
      $(".quantity-input").val(value);
    }
  });

  $(".dec-btn").click(function (e) {
    e.preventDefault();

    let inc_value = $(".quantity-input").val();
    let value = parseInt(inc_value, 10);
    value = isNaN(value) ? 0 : value;

    if (value > 1) {
      value--;
      $(".quantity-input").val(value);
    }
  });

  $(".addToCart").click(function (e) {
    e.preventDefault();

    let product_id = $(".prod_id").val();
    let product_qty = $(".quantity-input").val();
    let token = $("input[name=csrfmiddlewaretoken]").val();
    $.ajax({
      method: "POST",
      url: "/add-to-cart/",
      data: {
        product_id: product_id,
        product_qty: product_qty,
        csrfmiddlewaretoken: token,
      },
      success: function (response) {
        alertify.notify(response.status, 'custom');
      },
    });
  });

  $(".changeQty").click(function (e) {
    e.preventDefault();

    let product_id = $(".prod_id").val();
    let product_qty = $(".quantity-input").val();
    let token = $("input[name=csrfmiddlewaretoken]").val();
    $.ajax({
      method: "POST",
      url: "/update-cart/",
      data: {
        product_id: product_id,
        product_qty: product_qty,
        csrfmiddlewaretoken: token,
      },
      success: function (response) {
        alertify.notify(response.status, 'custom');
      },
    });
  });

  $(".delete-cart-item").click(function (e) {
    e.preventDefault();

    let product_id = $(".prod_id").val();
    let token = $("input[name=csrfmiddlewaretoken]").val();

    $.ajax({
      method: "POST",
      url: "/delete-cart-item/",
      data: {
        product_id: product_id,
        csrfmiddlewaretoken: token,
      },
      success: function (response) {
        alertify.notify(response.status, 'custom');
        $(".cart-data").load(location.href + " .cart-data");
      },
    });
  });


//   ===================== Verification ===================================
$(".verify").click(function (e) {
    let phone = $(".phone_input").val();
    if (phone === ""){
        alerify.alert("Phone field is empty")
    }
    else{
        $(".checkout").disabled = true;
        $('.spinner').addClass("spinner-grow");
        $('.verify').text("Checking")
        e.preventDefault();

        let token = $("input[name=csrfmiddlewaretoken]").val();
        $.ajax({
          method: "POST",
          url: "/display_name/",
          data: {
            phone: phone,
            csrfmiddlewaretoken: token,
          },
          success: function (response) {
              $('.verify').text("Verify Number")
              $('.spinner').removeClass("spinner-grow");
              alertify.alert('Customer Name', response.status, function(){
                  $('.verify').text("Verify Number")
                  $('.spinner').removeClass("spinner-grow");
              });
          },
        });
    }
  });


$(".check-balance").click(function (e) {
    e.preventDefault();

    let account_number = $(".account-input").val();

    if (account_number === ""){
        alerify.alert("Account number not provided")
    }
    else{
        $(".check-balance").text("Getting Details")
        $('.tv-spinner').addClass("spinner-grow");



        let provider = $(".provider-input").val();
        let token = $("input[name=csrfmiddlewaretoken]").val();

        if (account_number === ""){
            alerify.alert("Account number field is empty")
        }

        $.ajax({
          method: "POST",
          url: "/balance_check/",
          data: {
            account_number: account_number,
            provider: provider,
            csrfmiddlewaretoken: token,
          },
          success: function (response) {
              $('.check-balance').text("Check")
                $('.tv-spinner').removeClass("spinner-grow")
            alertify.alert("Account Details", response.status, function(){
                $('.check-balance').text("Check")
                $('.tv-spinner').removeClass("spinner-grow");
            });
          },
        });
    }

});
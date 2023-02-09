from django.urls import path
from bestPayApp import views
from bestPayApp.authViews import authViews as customAuthViews
from bestPayApp.airtime import airtimeViews
from bestPayApp.airtime import displayViews
from bestPayApp.bundle import bundleViews
from bestPayApp.bundle.other_mtn_bundles import other_mtn_bundles
from bestPayApp.bundle.other_at_bundles import other_at_bundles
from bestPayApp.tv import tvViews
from bestPayApp.dashboard import dashboardViews
from bestPayApp.shop.product import productsViews
from bestPayApp.shop.cart import cartViews
from bestPayApp.shop.checkout import checkoutViews

urlpatterns = [
    path("", views.home, name="home"),
    path("services", views.services, name="services"),
    path("about", views.about, name="about"),
    path("blog", views.blog, name="blog"),
    path("thank_you", views.thank_you, name="thank_you"),
    path("failed", views.failed, name="failed"),

    path("sign-up/", customAuthViews.sign_up, name="signup"),
    path("login/", customAuthViews.login_page, name="login"),
    path("logout/", customAuthViews.logout_user, name="logout"),
    path("password_reset", customAuthViews.password_reset_request, name="password_reset"),

    path("services/airtime", airtimeViews.airtime, name="airtime"),
    path("send_airtime/<str:reference>/<str:phone_number>/<str:amount>/<str:provider>", airtimeViews.send_airtime,
         name="send_airtime"),

    path("services/bundles", bundleViews.bundle, name="bundle"),

    path("services/bundles/vodafone", bundleViews.vodafone, name="voda-bundle"),
    path("send_vodafone_bundle/<str:client_ref>/<str:phone_number>/<str:amount>/<str:value>",
         bundleViews.send_voda_bundle, name="send_voda_bundle"),

    path("services/bundles/mtn", bundleViews.mtn_all_bundles, name="mtn-all-bundles"),
    path("services/bundles/mtn/other-bundles", other_mtn_bundles.other_mtn_bundles, name="other-mtn-bundles"),
    path("services/bundles/mtn-flexi-and-others", bundleViews.mtn, name="mtn-bundle"),
    path("send_mtn_bundle/<str:client_ref>/<str:phone_number>/<str:amount>/<str:value>", bundleViews.send_mtn_bundle,
         name="send_mtn_bundle"),
    path("send_other_mtn_bundle/<str:client_ref>/<str:phone_number>/<str:amount>/<str:value>",
         other_mtn_bundles.send_other_mtn_bundle, name="send_other_mtn_bundle"),

    path("services/bundles/airtel-tigo", bundleViews.at_all_bundles, name="at_all_bundles"),
    path("services/bundles/airtel-tigo/big-time", bundleViews.airtel_tigo, name="at-big-time"),
    path("send_at_bundle/<str:client_ref>/<str:phone_number>/<str:amount>/<str:value>",
         bundleViews.send_at_bundle, name="send_at_bundle"),
    path("services/bundles/airtel-tigo/sika-kokoo", other_at_bundles.sika_kokoo, name="at-sika-kokoo"),
    path("send_sk_bundle/<str:client_ref>/<str:phone_number>/<str:amount>/<str:value>",
         other_at_bundles.send_sk_bundle, name="send_sk_bundle"),
    path("services/bundles/ishare", other_at_bundles.ishare_bundle, name="ishare_bundle"),
    path("send_ishare_bundle/<str:client_ref>/<str:phone_number>/<str:bundle>", other_at_bundles.send_ishare_bundle, name="send_ishare_bundle"),

    path("services/tv", tvViews.tv_all, name="tv"),
    path("services/tv/balance_check", tvViews.tv_check, name="tv_check"),
    path("services/tv-subscriptions", tvViews.tv, name="tv-subscription"),
    path("balance_check/", tvViews.balance_check, name="balance_check"),
    path("add_amount_to_tv_account/<str:reference>/<str:phone_number>/<str:amount>/<str:provider>",
         tvViews.add_amount_to_tv_account, name="add_amount_to_tv_account"),

    path("user-dashboard", dashboardViews.dashboard, name="user-dashboard"),
    path("dashboard/txn_table/<str:keyword>/", dashboardViews.txn_table, name='txn_table'),

    path("display_name/", displayViews.display_name, name="display_name"),

    #     **************************************************** Shop URLS **********************************************
    path("shop/products", productsViews.products, name='products'),
    path("shop/products/<str:product_name>", productsViews.product_detail, name='product_detail'),
    path("add-to-cart/", cartViews.add_to_cart, name="add_to_cart"),
    path("shop/cart", cartViews.view_cart, name="view-cart"),
    path("update-cart/", cartViews.update_cart, name="update-cart"),
    path("delete-cart-item/", cartViews.delete_cart_item, name="delete-cart-item"),

    path("shop/checkout", checkoutViews.checkout, name="checkout"),
    path("shop/place_order", checkoutViews.place_order, name="place-order"),
    path("make-payment/", checkoutViews.make_payment, name="make-payment"),
    path("place_order/<str:client_ref>/<str:first_name>/<str:last_name>/<str:email>/<str:phone>/<str:address>",
         checkoutViews.place_order, name="place-order"),

]

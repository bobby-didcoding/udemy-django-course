# --------------------------------------------------------------
# App imports
# --------------------------------------------------------------
from ecommerce.tests.models import(
    PriceTestCase,
    ProductTestCase,
    CustomerTestCase,
    CartTestCase,
    SessionItemTestCase,
    SessionTestCase,
    InvoiceTestCase
)

from ecommerce.tests.views import(
    CartViewTestCase,
    ManageCartViewTestCase,
    SessionCreateViewTestCase,
    SessionSuccessViewTestCase,
    SessionCancelViewTestCase,
    ProductsViewTestCase,
    ProductViewTestCase
)


__all__ = [

    PriceTestCase,
    ProductTestCase,
    CustomerTestCase,
    CartTestCase,
    SessionItemTestCase,
    SessionTestCase,
    InvoiceTestCase,
    CartViewTestCase,
    ManageCartViewTestCase,
    SessionCreateViewTestCase,
    SessionSuccessViewTestCase,
    SessionCancelViewTestCase,
    ProductViewTestCase,
    ProductsViewTestCase
]

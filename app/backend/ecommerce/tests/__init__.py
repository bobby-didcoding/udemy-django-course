# --------------------------------------------------------------
# App imports
# --------------------------------------------------------------
from ecommerce.tests.models import(
    PriceTestCase,
    ProductTestCase,
    CustomerTestCase,
    CartTestCase
)

from ecommerce.tests.views import (
    CartViewTestCase,
    ProductsViewTestCase,
    ProductViewTestCase,
    ManageCartViewTestCase,
    SessionCreateViewTestCase,
    SessionSuccessViewTestCase,
    SessionCancelViewTestCase
)


__all__ = [

    PriceTestCase,
    ProductTestCase,
    CustomerTestCase,
    CartTestCase,
    CartViewTestCase,
    ProductViewTestCase,
    ProductsViewTestCase,
    ManageCartViewTestCase,
    SessionCreateViewTestCase,
    SessionSuccessViewTestCase,
    SessionCancelViewTestCase
]

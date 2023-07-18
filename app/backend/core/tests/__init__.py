# --------------------------------------------------------------
# App imports
# --------------------------------------------------------------
from core.tests.models import (
    BlogTestCase,
    CertificateTestCase,
    PolicyTestCase,
    PortfolioTestCase,
    ContactTestCase,
    NewsLetterTestCase,
    SkillTestCase,
    TestimonialTestCase
)

from core.tests.forms import (
    ContactFormTestCase,
    GenericNewsLetterFormTestCase
)

from core.tests.views import (
    HomeViewTestCase
)


__all__ = [
    BlogTestCase,
    CertificateTestCase,
    PolicyTestCase,
    PortfolioTestCase,
    ContactTestCase,
    NewsLetterTestCase,
    SkillTestCase,
    TestimonialTestCase,
    ContactFormTestCase,
    GenericNewsLetterFormTestCase,
    HomeViewTestCase
]

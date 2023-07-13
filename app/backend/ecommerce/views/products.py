# --------------------------------------------------------------
# Django imports
# --------------------------------------------------------------
from django.views import generic

# --------------------------------------------------------------
# App imports
# --------------------------------------------------------------
from ecommerce.models import Product



class ProductsView(generic.ListView):
	"""
    ListView used for our products page.

    **Template:**

    :template:`ecommerce/products.html`
    """
	model = Product
	template_name = "products/products.html"
	paginate_by = 100

	def get_queryset(self):
		return self.model.objects.active()
from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.tools import lazy
from odoo.addons.website_sale.controllers.main import TableCompute


class WebsiteSaleInherit(WebsiteSale):
    def shop(self, page=0, category=None, search='', min_price=0.0, max_price=0.0, ppg=False, **post):
        rec = super(WebsiteSaleInherit, self).shop(page=0, category=None, search='', min_price=0.0, max_price=0.0,
                                                      ppg=False, **post)
        products = request.env.user.allowed_product_ids
        category = request.env.user.product_category_ids
        print(products)
        if products or category:
            if category:
                website = request.env['website'].get_current_website()
                print('website', website)
                website_domain = website.website_domain()
                if ppg:
                    try:
                        ppg = int(ppg)
                        post['ppg'] = ppg
                    except ValueError:
                        ppg = False
                if not ppg:
                    ppg = website.shop_ppg or 20
                ppr = website.shop_ppr or 4
                pricelist = website.pricelist_id
                print('pricelist', pricelist)

                categs_domain = [('parent_id', '=', False)] + website_domain
                if search:
                    search_categories = category.search(
                        [('product_tmpl_ids', 'in', products.ids) + website_domain]
                    ).parents_and_self
                    categs_domain.append(('id', 'in', search_categories))
                categs = lazy(lambda: category.search(categs_domain))

                fiscal_position_sudo = website.fiscal_position_id.sudo()
                products_prices = lazy(
                    lambda: products._get_sales_prices(pricelist,
                                                       fiscal_position_sudo))
                rec.qcontext.update({
                    'category': category,
                    'pricelist': pricelist,
                    'fiscal_position': fiscal_position_sudo,
                    'products': products,
                    'bins': lazy(
                        lambda: TableCompute().process(products, ppg, ppr)),
                    'ppg': ppg,
                    'ppr': ppr,
                    'categories': categs,
                    'products_prices': products_prices,
                    'get_product_prices': lambda product: lazy(
                        lambda: products_prices[product.id]),
                })
            print(rec)
        return rec




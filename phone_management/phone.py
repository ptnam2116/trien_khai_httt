# -*- coding: utf-8 -*-
from openerp.osv import fields, osv

class phone_brand(osv.osv):
    _name = 'phone.brand'
    _columns = {
        'code': fields.char('Mã hãng', size=20, required=True),
        'name': fields.char('Tên hãng', size=50, required=True, translate=True),
        'description': fields.text('Mô tả chi tiết'),
    }
    _sql_constraints = [
        ('brand_code_unique', 'unique(code)', 'Ma hang phai la duy nhat!')
    ]

    def unlink(self, cr, uid, ids, context=None):
        phone_obj = self.pool.get('phone.phone')
        for brand in self.browse(cr, uid, ids, context=context):
            phone_ids = phone_obj.search(cr, uid, [('brand_id', '=', brand.id)], context=context)
            if phone_ids:
                raise osv.except_osv(
                    'Canh bao!',
                    'Khong the xoa hang "%s" vi van con san pham lien ket.' % brand.name
                )
        return super(phone_brand, self).unlink(cr, uid, ids, context=context)


class phone(osv.osv):
    _name = 'phone.phone'
    _columns = {
        'code': fields.char('Mã điện thoại', size=20, required=True),
        'name': fields.char('Tên điện thoại', size=50, required=True, translate=True),
        'brand_id': fields.many2one('phone.brand', 'Hãng sản xuất', required=True),
        'import_price': fields.float('Giá nhập'),
        'sale_price': fields.float('Giá bán'),
        'description': fields.text('Mô tả chi tiết'),
        'os': fields.selection([
        ('ios', 'iOS'),
        ('android', 'Android')
    ], 'Hệ điều hành', required=True)
    }
    _defaults = {
        'import_price': 0.0,
        'sale_price': 0.0
    }
    _sql_constraints = [
        ('phone_code_unique', 'unique(code)', 'Ma dien thoai phai la duy nhat!')
    ]

phone_brand()
phone()

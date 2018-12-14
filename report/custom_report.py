from openerp.osv import fields, osv
from openerp import tools
from openerp.tools import file_open


class custom_report(osv.osv):
    _name = "custom.report"
    _description = "Custom project report"
    _auto = False

    _columns = {
        'user_id': fields.many2one('res.users', 'User', readonly=True),
        'project_id': fields.many2one('project.project', 'Project',
                                      readonly=True),
        'target': fields.integer('Target'),
        'state': fields.selection([('template', 'Template'),
                                   ('draft', 'New'),
                                   ('open', 'In Progress'),
                                   ('cancelled', 'Cancelled'),
                                   ('pending', 'Pending'),
                                   ('close', 'Closed')],
                                  'Status', required=True, copy=False),
    }

    def read_group(self, cr, uid, domain, fields, groupby, offset=0,
                   limit=None, context=None, orderby=False, lazy=True):
        res = super(custom_report, self).read_group(cr, uid, domain, fields,
                                                    groupby, offset, limit,
                                                    context, orderby, lazy)
        print '<<<\n res \n\n %s >>>' % res
        return res


def init(self, cr):
    with file_open('diligences_test/sql/custom_report.sql') as f:
        sql_query = f.read()
        tools.drop_view_if_exists(cr, self._table)
        cr.execute("""
                    CREATE or REPLACE VIEW %(table_name)s as (%(sql_query)s)
                        """ % {
            'table_name': self._table,
            'sql_query': sql_query,
        })

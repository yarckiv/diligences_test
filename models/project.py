from openerp.osv import osv, fields


class CustomProject(osv.osv):
    _description = "Custom Project"
    _inherit = 'project.project'

    _columns = {
        'stage_id': fields.many2many('project.project.stage',
                                     'project_project_stage_rel',
                                     'project_id', 'stage_id',
                                     'Project Stages')
    }


class project_project_stage(osv.osv):
    _name = 'project.project.stage'
    _description = 'Project Stage'
    _columns = {
        'name': fields.char('Stage Name', required=True, translate=True),
        'description': fields.text('Description'),
        'sequence': fields.integer('Sequence'),
        'project_ids': fields.many2many('project.project',
                                        'project_project_stage_rel',
                                        'stage_id',
                                        'project_id', 'Projects'),
    }

    def _get_default_project_ids(self, cr, uid, ctx={}):
        project_id = self.pool['project.task']._get_default_project_id(cr, uid,
                                                                       context=ctx)
        if project_id:
            return [project_id]
        return None

    _defaults = {
        'project_ids': _get_default_project_ids,
    }

from flask_admin.contrib.sqla import ModelView


class ModelViewMixin(ModelView):
    can_view_details = True
    create_modal = True
    edit_modal = True
    detials_modal = True
    can_export = True
    page_size = 50


class ExpenditureTypeModelView(ModelViewMixin):
    column_labels = {
        'name': '类别',
    }

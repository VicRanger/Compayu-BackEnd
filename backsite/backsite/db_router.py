from django.conf import settings

DATABASE_MAPPING = settings.DATABASE_APPS_MAPPING

class DbRouter(object):
    def db_for_read(self, model, **hints):
        if model._meta.app_label in DATABASE_MAPPING:
            return DATABASE_MAPPING[model._meta.app_label]
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in DATABASE_MAPPING:
            return DATABASE_MAPPING[model._meta.app_label]
        return None

    def allow_relation(self, obj1, obj2, **hints):
        pass

    def allow_migrate(self, db, app_label, model=None, **hints):
        # print(db,app_label)
        if app_label in DATABASE_MAPPING:
            return db==DATABASE_MAPPING[app_label]
        else:
            return True if db=='default' else False
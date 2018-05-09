import ZODB, ZODB.FileStorage
import transaction


class DataStorage():
    def __init__(self, ref_name):
        self.storage = ZODB.FileStorage.FileStorage('images_inst.fs')
        self.db = ZODB.DB(self.storage)
        self.connection = self.db.open()
        self.db_root = self.connection.root()
        self.ref_name = ref_name
        self.ref = self.db_root[ref_name]

    def __getitem__(self, key):
        return self.ref[key]

    def __setitem__(self, value):
        self.ref = value

    def delete_item(self, ref, key, i):
        del(self.db_root[ref][key][i])

    def delete_key(self, ref, key):
        del(self.db_root[ref][key])

    def finish(self):
        transaction.commit()
        self.connection.close()

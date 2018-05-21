import ZODB, ZODB.FileStorage
from BTrees import OOBTree
import transaction


class DataStorage():
    def __init__(self, ref_name):
        self.storage = ZODB.FileStorage.FileStorage('images_inst.fs')
        self.db = ZODB.DB(self.storage)
        self.connection = self.db.open()
        self.db_root = self.connection.root()
        if ref_name not in self.db_root.keys():
            self.db_root[ref_name] = OOBTree()
        self.ref_name = ref_name
        self.ref = self.db_root[ref_name]

    def __getitem__(self, key):
        return self.ref[key]

    def __setitem__(self, value):
        self.ref = value
        self._p_changed = True

    def delete_item(self, ref, key, i):
        del(self.db_root[ref][key][i])

    def delete_key(self, ref, key):
        del(self.db_root[ref][key])

    def delete_ref(self, ref):
        del(self.db_root[ref])
        ref = None

    def finish(self):
        transaction.commit()
        self.connection.close()
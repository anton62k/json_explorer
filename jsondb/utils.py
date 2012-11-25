# coding: utf8
from jsondb.project import Project
import json
import os
import codecs
import shutil


class DumpsError(Exception):
    pass


def loads(path):
    project = Project()
    return project


def dumps(path, project):

    def clear_dir(path):
        for item in os.listdir(path):
            os.remove(os.path.join(path, item))

    def get_and_create_dir(*args):
        path = os.path.join(*args)

        if os.path.exists(path) and not os.path.isdir(path):
            raise DumpsError('error, path "%s" exist, path is not dir' % path)
        elif not os.path.exists(path):
            os.makedirs(path)
        elif os.path.exists(path):
            clear_dir(path)

        return path

    def save_doc(path, doc):
        path = os.path.join(path, '%s.json' % doc.name)

        if os.path.exists(path) and os.path.isdir(path):
            raise DumpsError('error, path "%s" exist, path is dir' % path)

        json_str = json.dumps(doc.data(), ensure_ascii=False, indent=4)
        f = codecs.open(path, mode='w+', encoding='utf8')
        f.write(json_str)
        f.close()

    dirs = filter(lambda item: os.path.isdir(os.path.join(path, item)),
                                                            os.listdir(path))
    dirs = map(lambda item: os.path.join(path, item), dirs)

    for table in project:
        path_table = get_and_create_dir(path, table.name)

        for doc in table:
            save_doc(path_table, doc)

        try:
            dirs.remove(path_table)
        except:
            pass

    for item in dirs:
        shutil.rmtree(item)

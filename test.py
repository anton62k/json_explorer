# coding: utf8

from jsondb.Document import Project, Document, Pattern


data = {'sub': {'k': {'n': 2}, 't': [1, 2, 3]}, 'f': 'sdf', 'n': 0.1,
        'a': [{'s_f': 1}]}

project = Project()
artifact = project.add('artifact')

pattern = artifact.pattern
sub_dict = pattern.add('sub_dict')
sub_int = pattern.add('sub_int', type='int', default=3)
sub_str = pattern.add('sub_str', type='str', default='text')

data = {'sub_int': 59, 'sub_dict': {}, 'sub_str': 'text'}

doc = artifact.add(1, data=data)
print doc.data()
#doc.get('sub_int').set(56)
#print doc.data()


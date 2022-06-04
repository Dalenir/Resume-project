from aiogram.dispatcher.filters import BaseFilter
from aiogram.types import Message

from DBuse import data_getter, user_look


class type_filter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        types = data_getter('SELECT type_name FROM project.testtype WHERE type_name is not NULL;')
        for test_type in types:
            if message.text == test_type[0]:
                return True
        return False

class severity_filter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        severities = data_getter('SELECT "severity" FROM project.bugseverity WHERE "severity" is not NULL;')
        for severity in severities:
            print (severity[0])
            if message.text == severity[0]:
                return {'severity': message.text}
        return False

class bug_filter(BaseFilter):
    async def __call__(self, message: Message):
        bugs = data_getter('SELECT "id" FROM project.bugreports WHERE "id" is not NULL;')
        for bug_id in bugs:
            try:
                if int(message.text) == bug_id[0]:
                    return {'bug_id': bug_id[0]}
            except:
                print('No such bug, creating new')
        user_id = user_look(message.from_user.id)
        new_bug_id = data_getter(f'INSERT INTO project.bugreports (user_id) VALUES ({user_id}) returning id;')[0][0]
        print (new_bug_id)
        return {'bug_id': new_bug_id}

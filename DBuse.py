from psycopg2 import sql

from bata import all_data

def data_getter(query):
    conn = all_data().get_postg()
    with conn:
        with conn.cursor() as cur:
            cur.execute(query)
            data = cur.fetchall()
    conn.close()
    return data

def safe_data_getter(query, values_dict):
    conn = all_data().get_postg()
    with conn:
        with conn.cursor() as cur:
            cur.execute(query, values_dict)
            data = cur.fetchall()
    conn.close()
    return data


def user_look(telegram_id):
    user_id = data_getter(F'select id from project.users where t_id = {telegram_id};')
    if user_id == []:
        user_id = data_getter(f'insert into project.users (t_id) values ({telegram_id}) returning id;')
    return user_id[0][0]


def testcase_insert_former(FSM_data, telegram_user_id):
    ndata = FSM_data

    bug = False
    if ndata['passed'] == 'PASSED':
        ndata.update({'passed':"True"})
    elif ndata['passed'] == 'NOT PASSED':
        ndata.update({'passed': "False"})
        bug = True

    print (ndata)
    conn = all_data().get_postg()

    user_id = user_look(telegram_user_id)
    ndata.update({'user_id': user_id})

    insert_string = "INSERT INTO project.testcases (title, type_id, steps, expected_result, received_result, passed, " \
                    "bug_id, user_id, initial_state, testdata) VALUES ({title}, (select id from project.testtype " \
                    "where type_name = {type_id}), {steps}, {expected_result}, {received_result}, {passed}, " \
                    "NULL, {user_id}, " \
                    "{initial_state}, {testdata}) returning id;"
    if bug == True:
        insert_string = "with ins1 as (insert into project.bugreports (user_id) VALUES ({user_id}) returning id as new_bug_id)"\
                    "INSERT INTO project.testcases (title, type_id, steps, expected_result, received_result, passed, bug_id, user_id, initial_state, testdata) VALUES ({title}, (select id from project.testtype where type_name = {type_id}), {steps}, {expected_result}, {received_result}, {passed}, (select new_bug_id from ins1), {user_id}, {initial_state}, {testdata})"\
                    "returning id, (select new_bug_id from ins1);"

    query = sql.SQL(insert_string).format(
    title=sql.Placeholder('title'),
    type_id = sql.Placeholder('type_id'),
    steps=sql.Placeholder('steps'),
    expected_result=sql.Placeholder('expected_result'),
    received_result=sql.Placeholder('received_result'),
    passed=sql.Placeholder('passed'),
    user_id=sql.Placeholder('user_id'),
    initial_state=sql.Placeholder('initial_state'),
    testdata=sql.Placeholder('testdata')
    )
    with conn:
        with conn.cursor() as cur:
            cur.execute(query, ndata)
            Dund = cur.fetchall()[0]
    conn.close()

    print(query.as_string(conn))
    print (Dund)
    return Dund


def checklist_insert(FSM_data, telegram_id):
    print (FSM_data, telegram_id)
    new_data = FSM_data
    conn = all_data().get_postg()
    user_id = user_look(telegram_id)
    new_data.update({'user_id': user_id})
    insert_string = 'INSERT INTO project.checklist (object_of_assay, group_id, "test_data", passed, user_id, priority) ' \
                    'VALUES' \
                    '({object_of_assay}, {group_id}, {test_data}, {passed}, {user_id}, (select id from project.bugseverity where severity = {priority})) returning id;'
    if new_data['passed'] == 'False':
        insert_string = 'with killme as (insert into project.bugreports (user_id) VALUES ({user_id}) returning id as new_bug_id)'\
                    'INSERT INTO project.checklist (object_of_assay, group_id, "test_data", passed, user_id, bug_id, priority) ' \
                    'VALUES' \
                    '({object_of_assay}, {group_id}, {test_data}, {passed}, {user_id}, (select new_bug_id from killme), (select id from project.bugseverity where severity = {priority})) returning id, (select new_bug_id from killme);'
    query = sql.SQL(insert_string).format(
        user_id=sql.Placeholder('user_id'),
        object_of_assay=sql.Placeholder('object_of_assay'),
        priority=sql.Placeholder('priority'),
        test_data=sql.Placeholder('test_data'),
        passed=sql.Placeholder('passed'),
        group_id=sql.Placeholder('group_id'),
    )
    with conn:
        with conn.cursor() as cur:
            cur.execute(query, new_data)
            Dund = cur.fetchall()[0]
    conn.close()
    print(query.as_string(conn))
    print (Dund)
    return Dund

def bugreport_insert(FSM_data, telegram_id):
    new_data = FSM_data
    conn = all_data().get_postg()
    user_id = user_look(telegram_id)
    new_data.update({'user_id': user_id})
    print (new_data)
    insert_string = 'UPDATE project.bugreports SET title = {title}, severity_id = (select id from project.bugseverity where severity = {severity}), initial_state={initial_state}, steps_to_reproduce={steps_to_reproduce}, received_result = {received_result}, expected_result = {expected_result},' \
                    'attachments = {attachment}, user_id = {user_id} WHERE id = {id} returning id;'

    query = sql.SQL(insert_string).format(
        id = sql.Placeholder('id'),
        title = sql.Placeholder('title'),
        severity=sql.Placeholder('severity'),
        initial_state=sql.Placeholder('initial_state'),
        steps_to_reproduce=sql.Placeholder('steps_to_reproduce'),
        received_result=sql.Placeholder('received_result'),
        expected_result=sql.Placeholder('expected_result'),
        attachment=sql.Placeholder('attachment'),
        user_id=sql.Placeholder('user_id'),
    )
    print(query.as_string(conn))
    with conn:
        with conn.cursor() as cur:
            cur.execute(query, new_data)
            Dund = cur.fetchall()[0][0]
    conn.close()
    return Dund


def all_tables_dump(path):
    conn = all_data().get_postg()
    testcases = """ 
        copy ( select 
		testcases.id, testcases.title, type_name, initial_state, steps, expected_result, received_result, passed, bug_id, t_id as User_id, testdata
		from project.testcases
		inner join
		project.users on testcases.user_id = users.id
		inner join
		project.testtype on type_id = testtype.id
		)
		to stdout csv header ;
		"""
    bugreports = """ copy (
    	select 
		bugreports.id, bugreports.title, severity, bugreports.steps_to_reproduce, t_id as user, bugreports.initial_state, bugreports.received_result, bugreports.expected_result, bugreports.attachments
		from project.bugreports
		inner join
		project.users on bugreports.user_id = users.id
		inner join
		project.bugseverity on bugreports.severity_id = bugseverity.id
		)
		to stdout csv header ;
        """
    checklist = """ copy (
    select checklist.id, checklist.object_of_assay, "group", checklist.test_data, checklist.passed, checklist.bug_id, t_id, severity
	from project.checklist
	left outer join project.web_check_groups
	on checklist.group_id = web_check_groups.id
	left outer join project.users
	on checklist.user_id = users.id
	left outer join project.bugseverity
	on checklist.priority = bugseverity.id
	)
	to stdout csv header ;
    """
    f1 = open(f'{path}/testcases.csv', 'w', encoding="utf-8")
    f2 = open(f'{path}/bugreports.csv', 'w', encoding="utf-8")
    f3 = open(f'{path}/checklist.csv', 'w', encoding="utf-8")
    with conn:
        with conn.cursor() as cur:
            cur.copy_expert(testcases,f1)
            cur.copy_expert(bugreports, f2)
            cur.copy_expert(checklist, f3)
    conn.close()
    print ('Testcases dumped')

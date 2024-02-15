import ansible_runner


def reset_database(playbook_path, inventory_path):
    r = ansible_runner.run(private_data_dir='/tmp', playbook=playbook_path, inventory=inventory_path)
    print("{}: {}".format(r.status, r.rc))
    # successful: 0
    print("Final status:")
    print(r.stats)


def create_session_on_server(playbook_path, inventory_path, email):
    extra_vars = {"email": email}
    r = ansible_runner.run(private_data_dir='/tmp', playbook=playbook_path, inventory=inventory_path, extravars=extra_vars)
    session_key = r.get_fact_cache('web')['session_key']
    return session_key

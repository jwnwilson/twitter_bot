from fabric.api import local


def run_manage(command):
    local('python ./manage.py %s' % command)


def web():
    """
    Run a server that will be accessable from inside a container on port 8000
    :return:
    """
    run_manage('runserver 0.0.0.0:8000')


def docker_compose(build=None, prod=None):
    """
    Start docker compose with django container and postgres container in develop mode

    :param: build string if 'True' rebuild docker image
    :param: prod Boolean if 'True' then use prod docker compose file
    :return: None
    """
    if build == 'True':
        cmd = "build"
    else:
        cmd = "up"
    if prod is 'True':
        compose_file = ""
    else:
        compose_file = "-f docker-compose-dev.yml"

    local("docker-compose %s %s " % (compose_file, cmd))


def docker_ip(machine_name="default"):
    """
    Print the ip address of docker instance to connect to in a browser
    Run with 'fab docker_ip:$CONTAINER_ID/CONTAINER_NAME'
    :param machine_name: docker image name
    :return: None
    """
    local("docker-machine ip %s" % machine_name)


def docker_bash(machine_name=""):
    """
    Start a shell in the id of the container passed in
    Run with 'fab docker_bash:$CONTAINER_ID/CONTAINER_NAME'
    :param machine_name: docker image name
    :return: ip address of docker instance to connect to in a browser
    """
    if machine_name == "":
        print "No machine name/id passed exiting"
    local("docker exec -i -t %s bash" % machine_name)


def migrate():
    run_manage('migrate')


def make_migrations():
    run_manage('makemigrations')


def requirements():
    local('pip install -r requirements.txt ')


def test():
    run_manage('test')


def create_test_data():
    run_manage('dumpdata stream items auth.user --indent 2 > testsite/test_data.json')


def hash_tag_battle(id):
    """
    Get the results of a hash tag battle
    :param id: battle id of battle created in admin console
    :return: None
    """
    if id:
        local("python ./py_scripts/battle_request.py --id %s" % id)
    else:
        print "No battle id submitted please submit a hash tag battle id."


def clear_load_test():
    # Clear data
    run_manage('flush')
    # Syncdb
    #run_manage('syncdb')
    # Load Data
    run_manage('loaddata testsite/test_data.json')
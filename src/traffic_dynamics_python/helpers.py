import os


def get_working_directory():
    env_var_name = "TRAFFIC_WORKDIR"
    if env_var_name in os.environ:
        directory_name = os.environ[env_var_name]
    else:
        directory_name = os.path.join(
            os.getcwd(),
            "data_directory"
        )
        print("environment variable " + env_var_name + " not set. Using " + directory_name)

    # make sure directory exists
    os.makedirs(directory_name, exist_ok=True)

    return directory_name

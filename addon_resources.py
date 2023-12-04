import os


def get_resources_path(sub_path: str = ""):
    return (
        os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        + os.sep
        + "resources"
        + os.sep
        + sub_path
    )

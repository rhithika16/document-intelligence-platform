from modules.version.repository import (
    create_document_group,
    get_next_version_number,
    mark_previous_versions_not_latest
)


def create_new_document(document_name):

    group_id = create_document_group(document_name)

    return {
        "document_group_id": group_id,
        "version_number": 1
    }


def create_new_version(document_group_id):

    version = get_next_version_number(document_group_id)

    mark_previous_versions_not_latest(document_group_id)

    return {
        "document_group_id": document_group_id,
        "version_number": version
    }
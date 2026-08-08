from modules.version.repository import (
    get_document_group_by_name,
    create_document_group,
    get_next_version_number,
    mark_previous_versions_not_latest
)


def get_version_information(document_name):
    """
    Determines whether the uploaded document is a new document
    or a new version of an existing document.

    The user does not need to provide:
    - is_new_document
    - document_group_id
    """

    existing_group = get_document_group_by_name(document_name)

    # ---------------------------------
    # New document
    # ---------------------------------
    if existing_group is None:

        group_id = create_document_group(document_name)

        return {
            "document_group_id": group_id,
            "version_number": 1,
            "is_new_document": True
        }

    # ---------------------------------
    # Existing document → new version
    # ---------------------------------

    group_id = existing_group["id"]

    next_version = get_next_version_number(group_id)

    # Previous version is no longer latest
    mark_previous_versions_not_latest(group_id)

    return {
        "document_group_id": group_id,
        "version_number": next_version,
        "is_new_document": False
    }
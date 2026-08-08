from database.connection import get_db_connection


def get_document_group_by_name(document_name):
    """
    Finds an existing document group using the logical document name.
    """

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT *
        FROM document_groups
        WHERE group_name = %s
        LIMIT 1
    """

    cursor.execute(query, (document_name,))
    result = cursor.fetchone()

    cursor.close()
    connection.close()

    return result


def create_document_group(document_name):
    """
    Creates a new logical document group.
    """

    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO document_groups (group_name)
        VALUES (%s)
    """

    cursor.execute(query, (document_name,))
    connection.commit()

    group_id = cursor.lastrowid

    cursor.close()
    connection.close()

    return group_id


def get_next_version_number(document_group_id):
    """
    Gets the next version number for a document group.
    """

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT MAX(version_number) AS latest_version
        FROM documents
        WHERE document_group_id = %s
    """

    cursor.execute(query, (document_group_id,))
    result = cursor.fetchone()

    cursor.close()
    connection.close()

    if result["latest_version"] is None:
        return 1

    return result["latest_version"] + 1


def mark_previous_versions_not_latest(document_group_id):
    """
    Marks all existing versions of a document as not latest.
    """

    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
        UPDATE documents
        SET is_latest = FALSE
        WHERE document_group_id = %s
    """

    cursor.execute(query, (document_group_id,))
    connection.commit()

    cursor.close()
    connection.close()
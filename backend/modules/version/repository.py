from database.connection import get_db_connection


def create_document_group(group_name):

    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
    INSERT INTO document_groups (group_name)
    VALUES (%s)
    """

    cursor.execute(query, (group_name,))
    connection.commit()

    group_id = cursor.lastrowid

    cursor.close()
    connection.close()

    return group_id


def get_next_version_number(document_group_id):

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT MAX(version_number) AS latest_version
    FROM documents
    WHERE document_group_id=%s
    """

    cursor.execute(query, (document_group_id,))
    result = cursor.fetchone()

    cursor.close()
    connection.close()

    if result["latest_version"] is None:
        return 1

    return result["latest_version"] + 1


def mark_previous_versions_not_latest(document_group_id):

    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
    UPDATE documents
    SET is_latest = FALSE
    WHERE document_group_id=%s
    """

    cursor.execute(query, (document_group_id,))
    connection.commit()

    cursor.close()
    connection.close()
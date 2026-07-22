from database.connection import get_db_connection


def save_document_metadata(
    file_name,
    file_type,
    file_size,
    cloud_path,
    status="Uploaded"
):

    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO documents
        (file_name, file_type, file_size, cloud_path, status)
        VALUES (%s, %s, %s, %s, %s)
    """

    values = (
        file_name,
        file_type,
        file_size,
        cloud_path,
        status
    )

    cursor.execute(query, values)

    connection.commit()

    document_id = cursor.lastrowid

    cursor.close()
    connection.close()

    return document_id
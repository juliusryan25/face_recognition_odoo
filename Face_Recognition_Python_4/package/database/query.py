from package import *

"""/////////////////////////////////////////////////////////////////////////////////////////////////////////////////"""

def upload_to_database(id, jam_masuk, image_location, conn):

    # Create table hr_attendance_raw if not exists

    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS hr_attendance_raw (
            id SERIAL PRIMARY KEY,
            employee_id INTEGER,
            create_uid INTEGER,
            write_uid INTEGER,
            check_in TIMESTAMP,
            check_out TIMESTAMP,
            create_date TIMESTAMP
        );
    """)

    conn.commit()

    # Query untuk insert data ke hr_attendance_raw

    query_hr_attendance_raw = """

    INSERT INTO hr_attendance_raw (employee_id, create_uid, write_uid, check_in, create_date)

    VALUES (%s, %s, %s, %s, %s)

    """

    try:

        # Eksekusi query

        cur.execute(query_hr_attendance_raw, (id, '1', '1', jam_masuk, jam_masuk))

        conn.commit()

        # Query untuk get earliest check_in from hr_attendance_raw

        query_get_earliest_check_in = """

        SELECT MIN(check_in) AS earliest_check_in

        FROM hr_attendance_raw

        WHERE employee_id = %s AND DATE(check_in) = DATE(%s)

        """

        cur.execute(query_get_earliest_check_in, (id, jam_masuk))

        earliest_check_in = cur.fetchone()[0]

        # Check if employee_id already exists in hr_attendance for the same day

        query_check_employee_id = """

        SELECT id

        FROM hr_attendance

        WHERE employee_id = %s AND DATE(check_in) = DATE(%s)

        """

        cur.execute(query_check_employee_id, (id, jam_masuk))

        if cur.fetchone() is None:

            # Insert new record into hr_attendance

            query_hr_attendance = """

            INSERT INTO hr_attendance (employee_id, create_uid, write_uid, check_in, create_date)

            VALUES (%s, %s, %s, %s, %s)

            RETURNING id

            """

            cur.execute(query_hr_attendance, (id, '1', '1', earliest_check_in, earliest_check_in))

            hr_attendance_id = cur.fetchone()[0]

            conn.commit()

        else:

            # Update existing record in hr_attendance for the same day

            query_update_hr_attendance = """

            UPDATE hr_attendance

            SET check_in = %s, create_date = %s

            WHERE employee_id = %s AND DATE(check_in) = DATE(%s)

            """

            cur.execute(query_update_hr_attendance, (earliest_check_in, earliest_check_in, id, jam_masuk))

            conn.commit()

        # Update last_check_in on hr_employee

        query_update_hr_employee = """

        UPDATE hr_employee

        SET last_check_in = %s

        WHERE id = %s

        """

        cur.execute(query_update_hr_employee, (earliest_check_in, id))

        conn.commit()

    except Exception as e:

        print(f"Terjadi kesalahan: {e}")

    finally:

        # Tutup kursor

        cur.close()

"""/////////////////////////////////////////////////////////////////////////////////////////////////////////////////"""
def upload_to_database_pulang(id, jam_pulang, conn):

    cur = conn.cursor()

    # Query untuk insert data ke hr_attendance_raw

    query_hr_attendance_raw = """

    INSERT INTO hr_attendance_raw (employee_id, create_uid, write_uid, check_out, create_date)

    VALUES (%s, %s, %s, %s, %s)

    """

    try:

        # Eksekusi query

        cur.execute(query_hr_attendance_raw, (id, '1', '1', jam_pulang, jam_pulang))

        conn.commit()

        # Query untuk get latest check_out from hr_attendance_raw

        query_get_latest_check_out = """

        SELECT MAX(check_out) AS latest_check_out

        FROM hr_attendance_raw

        WHERE employee_id = %s

        """

        cur.execute(query_get_latest_check_out, (id))

        latest_check_out = cur.fetchone()[0]

        # Check if employee_id already exists in hr_attendance for the same day

        query_check_employee_id = """

        SELECT id, check_in

        FROM hr_attendance

        WHERE employee_id = %s

        """

        cur.execute(query_check_employee_id, (id))

        attendance_id = cur.fetchone()

        # Update existing record in hr_attendance for the same day

        query_update_hr_attendance = """

        UPDATE hr_attendance

        SET check_out = %s, write_date = %s, worked_hours = EXTRACT(EPOCH FROM (%s - check_in))/3600

        WHERE id = %s

        """

        cur.execute(query_update_hr_attendance, (latest_check_out, latest_check_out, latest_check_out, attendance_id))

        conn.commit()

        # Update last_check_out on hr_employee

        query_update_hr_employee = """

        UPDATE hr_employee

        SET last_check_out = %s, write_date = %s

        WHERE id = %s

        """

        cur.execute(query_update_hr_employee, (latest_check_out, latest_check_out, id))

        conn.commit()

    except Exception as e:

        print(f"Terjadi kesalahan: {e}")

    finally:

        # Tutup kursor

        cur.close()
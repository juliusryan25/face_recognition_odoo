from package import *

# Buat koneksi ke database
"""/////////////////////////////////////////////////////////////////////////////////////////////////////////////////"""
conn = get_connection()
with get_connection() as conn:
    try:
        # Jalankan query untuk mengambil data wajah yang dikenal
        with conn.cursor() as cur:
            cur.execute("""SELECT a.id, a.name, c.store_fname
                        FROM hr_employee AS a
                        JOIN resource_resource AS b
                        ON a.resource_id = b.id
                        JOIN ir_attachment AS c
                        ON c.res_id = b.id
                        WHERE c.res_model = 'hr.employee'
                        AND c.res_field = 'image_1920';
	                    """)
            rows = cur.fetchall()
    except Exception as e:
        # pass
        print(f"Terjadi kesalahan: {e}")

"""/////////////////////////////////////////////////////////////////////////////////////////////////////////////////"""
def upload_to_database(id, jam_masuk, conn):
    # Konversi gambar ke binary
    # foto_absen = convert_to_binary(file_path)

    # Query untuk insert data
    query = """
    INSERT INTO hr_attendance (employee_id, create_uid, write_uid, check_in, create_date)
    VALUES (%s, %s, %s, %s, %s)
    """

    # Buka kursor baru
    cur = conn.cursor()

    try:
        # Eksekusi query
        cur.execute(query, (id,'1','1',jam_masuk,jam_masuk))
        # Commit perubahan
        conn.commit()
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
    finally:
        # Tutup kursor
        cur.close()

"""/////////////////////////////////////////////////////////////////////////////////////////////////////////////////"""
def upload_to_database_pulang(id, conn):
    query= """
    WITH updated_attendance AS (
    UPDATE public.hr_attendance
    SET check_out = CURRENT_TIMESTAMP,
        write_date = CURRENT_TIMESTAMP,
        worked_hours = CAST(EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - check_in))/3600 AS double precision)

    WHERE employee_id = """+str(id)+"""
    AND DATE(check_in) = CURRENT_DATE
    AND check_out IS NULL
    RETURNING id, employee_id, check_in, check_out, write_date
    )
    UPDATE public.hr_employee
    SET write_date = updated_attendance.write_date,
        last_attendance_id = updated_attendance.id,
        last_check_in = updated_attendance.check_in,
        last_check_out = updated_attendance.check_out
    FROM updated_attendance
    WHERE public.hr_employee.id = updated_attendance.employee_id
    AND public.hr_employee.id = """+str(id)+""";
    """

    # Buka kursor baru
    cur = conn.cursor()

    try:
        # Eksekusi query
        cur.execute(query)
        # Commit perubahan
        conn.commit()
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
    finally:
        # Tutup kursor
        cur.close()

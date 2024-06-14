from package import *

UNKNOWN_THRESHOLD = 0.5
data = {}
known_face_encodings = []
known_face_names = []
known_id= []
captured_names = []
data_absen_masuk = []
data_absen_pulang = []

#ambil data wajah
data[f"employee"] = []
for row in rows:
    id, name, store_fname = row
    data[f"employee"].append({"id": id, "nama": name, "image": store_fname})
    
    # Ganti 'binary_file_path' dengan direktori filestore odoo anda 
    binary_file_path = 'C:/Program Files/Odoo_16/sessions/filestore/db_odoo_16'
    image_employee  = store_fname 
    image_address = (f'{binary_file_path}/{image_employee}')

    image_source = face_recognition.load_image_file(image_address)
    face_encodings = face_recognition.face_encodings(image_source)

    if face_encodings:
        known_face_encodings.append(face_encodings[0])
        known_face_names.append(name)
        known_id.append(id)
        print(known_face_names)
    else:
        print(f"Tidak ada wajah yang ditemukan dalam gambar {image_address}.")

# def run_flask_app():
#         web_app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)

class WebcamApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Webcam Preview")

        self.mode = "In"
        self.cap = cv2.VideoCapture(0)

        self.canvas = tk.Canvas(root, width=640, height=480)
        self.canvas.pack()

        self.btn_in = ttk.Button(root, text="In", command=self.set_mode_in)
        self.btn_in.pack(side=tk.LEFT)

        self.btn_out = ttk.Button(root, text="Out", command=self.set_mode_out)
        self.btn_out.pack(side=tk.RIGHT)

        self.update_frame()

    def set_mode_in(self):
        self.mode = "In"

    def set_mode_out(self):
        self.mode = "Out"

    def process_frame(self , frame):
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]
        face_locations = face_recognition.face_locations(rgb_small_frame, model="hog",number_of_times_to_upsample=2)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if face_distances[best_match_index] <= UNKNOWN_THRESHOLD:
                name = known_face_names[best_match_index]
            else:
                name = "Unknown"
            face_names.append(name)

        return face_locations, face_names
    
    def compress_and_save_image_masuk(self, id, image, name, folder_path, quality=70):
        nama_karyawan = name
        id = id
        jam_masuk = datetime.now()

        pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_RGB2XYZ))
        buffer = io.BytesIO()
        pil_image.save(buffer, format="JPEG", quality=quality, optimize=True)
        image_data = buffer.getvalue()
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
        face_filename = f'{name}_{timestamp}.jpg'
        file_path = os.path.join(folder_path, face_filename) 

        with open(file_path, 'wb') as f:
            f.write(image_data)

        # Buat jendela pop-up
        def show_capture_popup():
            popup = tk.Toplevel(self.root)
            popup.title(f"Capture {name}")

            # Load gambar ke dalam label
            img = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_RGB2XYZ))
            imgtk = ImageTk.PhotoImage(image=img)
            label = tk.Label(popup, image=imgtk)
            label.image = imgtk  # Simpan referensi
            label.pack()

            # Tutup jendela setelah 3 detik
            popup.after(1500, popup.destroy)

        # Jalankan fungsi show_capture_popup di thread terpisah
        threading.Thread(target=show_capture_popup).start()

        data_absen_masuk.append(name)
        # known_nik.append(nik)
        upload_to_database(id, jam_masuk, conn)
        print(f"Gambar berhasil disimpan sebagai {face_filename}")
        print(f"Ini data absen masuk : {data_absen_masuk}")
        if nama_karyawan in data_absen_pulang :
            data_absen_pulang.remove(nama_karyawan) 
            # captured_names.remove(nama_karyawan) 
            print(f"ini data absen pulang : {data_absen_pulang}")
        else :
            print(f"ini data absen pulang : {data_absen_pulang}")
            pass
    
    def compress_and_save_image_pulang(self, id, image, name, folder_path, quality=70):
        nama_karyawan = name
       
        pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_RGB2XYZ))
        buffer = io.BytesIO()
        pil_image.save(buffer, format="JPEG", quality=quality, optimize=True)
        image_data = buffer.getvalue()
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
        face_filename = f'{name}_{timestamp}.jpg'
        file_path = os.path.join(folder_path, face_filename)

        with open(file_path, 'wb') as f:
            f.write(image_data)
        
         # Buat jendela pop-up
        def show_capture_popup():
            popup = tk.Toplevel(self.root)
            popup.title(f"Capture {name}")

            # Load gambar ke dalam label
            img = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_RGB2XYZ))
            imgtk = ImageTk.PhotoImage(image=img)
            label = tk.Label(popup, image=imgtk)
            label.image = imgtk  # Simpan referensi
            label.pack()

            # Tutup jendela setelah 3 detik
            popup.after(1500, popup.destroy)

        # Jalankan fungsi show_capture_popup di thread terpisah
        threading.Thread(target=show_capture_popup).start()


        captured_names.append(name)
        data_absen_pulang.append(name)
    
        upload_to_database_pulang(id, conn)
        print(f"Gambar berhasil disimpan sebagai {face_filename}")
        if nama_karyawan in data_absen_masuk :
            data_absen_masuk.remove(nama_karyawan)  
            print(f"ini data absen masuk : {data_absen_masuk}")
        else :
            print(f"ini data absen masuk : {data_absen_masuk}")
            pass
        print(f"ini data absen pulang : {data_absen_pulang}")
        
    
    def adjust_text_size(self, frame, text, max_width, min_font_size=0.5, max_font_size=1.5, step=0.1):
        for font_size in np.arange(max_font_size, min_font_size, -step):
            (text_width, text_height), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_size, 2)
            if text_width <= max_width:
                return font_size, (text_width, text_height)
        return min_font_size, cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, min_font_size, 1)[0]

    #PROSES FRAME / PREVIEW
    def update_frame(self):
        ret, frame = self.cap.read()
        frame = cv2.flip(frame, 1)
        if ret:
            # Convert the frame to RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.face_locations, self.face_names = self.process_frame(frame)

            for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                text_bottom = bottom + 25
                max_text_width = right - left
                font_size, (text_width, text_height) = self.adjust_text_size(frame, name, max_text_width)

                if text_bottom > frame.shape[0]:
                        text_bottom = frame.shape[0] - 10

                rectangle_color = (0, 0, 255) if name == "Unknown" else (0, 255, 0)
                cv2.rectangle(frame, (left, top), (right, bottom), rectangle_color, 2)
                cv2.rectangle(frame, (left, text_bottom - text_height + 3), (left + text_width, text_bottom + 3), rectangle_color, cv2.FILLED)
                cv2.putText(frame, name, (left + 1, bottom + 20), cv2.FONT_HERSHEY_SIMPLEX, font_size, (255, 255, 255), 2)
                
                folder_path = 'package/capture'
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                
                if self.mode == "In" :
                     if name in known_face_names:
                        face_image = frame[top:bottom + 25, left:right]
                        index = known_face_names.index(name)
                        id = known_id[index]

                        if name not in data_absen_masuk:
                            self.compress_and_save_image_masuk(id, face_image, name, folder_path)
                                                  
                if self.mode == "Out" :
                    if name in known_face_names:
                        face_image = frame[top:bottom + 25, left:right]
                        index = known_face_names.index(name)
                        id = known_id[index]

                        if name in data_absen_masuk and name not in data_absen_pulang:
                                self.compress_and_save_image_pulang(id, face_image, name, folder_path)
                                                                                       
            # MENAMPILKAN MODE PADA FRAME / PREVIEW
            cv2.putText(frame, f"Mode: {self.mode}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

            # KONFERSI FRAME KE FORMAT IMAGE TK 
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=imgtk)
            self.canvas.image = imgtk

        self.root.after(10, self.update_frame)

    def on_closing(self):
        self.cap.release()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = WebcamApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
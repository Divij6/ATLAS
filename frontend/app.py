# # app.py
# from flask import Flask, render_template, send_from_directory, jsonify, request
# from pymongo import MongoClient
# from bson.objectid import ObjectId
# import os, shutil, time
#
# # Try to load encryption key if provided (optional)
# try:
#     import EncryptionConfig
#     from cryptography.fernet import Fernet
#     cipher = Fernet(EncryptionConfig.ENCRYPTION_KEY)
# except Exception:
#     cipher = None
#
# # === CONFIG - adjust if you prefer env vars instead ===
# MONGO_CONNECTION_STRING = "mongodb+srv://gujarathibond:Divij&9475@atlas.i0mvluo.mongodb.net/?retryWrites=true&w=majority&appName=ATLAS"
# DETECTION_DIR = r"D:\DRDO\WeaponDetection(ATLAS)\detection_clips"
# NEUTRALIZED_DIR = "neutralized_clips"
#
# app = Flask(__name__, static_folder="static")
#
# # === Mongo setup ===
# client = MongoClient(MONGO_CONNECTION_STRING)
# db = client["security_events"]
# collection = db["threat_logs"]
#
# # === Helpers for (optional) encryption ===
# def decrypt_if_possible(val):
#     if val is None:
#         return None
#     try:
#         if cipher:
#             # val could be bytes, str, or pymongo Binary
#             if isinstance(val, (bytes, bytearray)):
#                 return cipher.decrypt(bytes(val)).decode()
#             if isinstance(val, str):
#                 return cipher.decrypt(val.encode()).decode()
#     except Exception:
#         # if decrypt fails, return original
#         return val
#     return val
#
# def encrypt_if_possible(s):
#     if cipher and isinstance(s, str):
#         return cipher.encrypt(s.encode())
#     return s
#
# # === Routes / Pages ===
# @app.route("/")
# def index():
#     return render_template("live_feed.html")
#
# @app.route("/live_threats")
# def live_threats_page():
#     return render_template("live_threats.html")
#
# @app.route("/neutralized")
# def neutralized_page():
#     return render_template("neutralized.html")
#
# @app.route("/police_stations")
# def police_page():
#     return render_template("police_stations.html")
#
# # === API Endpoints ===
# @app.route("/api/threats")
# def api_threats():
#     # returns recent threats NOT neutralized
#     docs = collection.find().sort("timestamp", -1).limit(200)
#     out = []
#     for d in docs:
#         status = decrypt_if_possible(d.get("status"))
#         if status and "Neutral" in str(status):
#             continue
#         description = decrypt_if_possible(d.get("description")) or "No description"
#         clip_name = d.get("clip_name") or d.get("clip") or None
#         out.append({
#             "id": str(d["_id"]),
#             "description": description,
#             "status": str(status),
#             "clip_name": clip_name,
#             "timestamp": d.get("timestamp").isoformat() if d.get("timestamp") else None
#         })
#     return jsonify(out)
#
# @app.route("/api/neutralized")
# def api_neutralized_list():
#     docs = collection.find().sort("timestamp", -1).limit(500)
#     out = []
#     for d in docs:
#         status = decrypt_if_possible(d.get("status"))
#         if status and "Neutral" in str(status):
#             description = decrypt_if_possible(d.get("description")) or "No description"
#             clip_name = d.get("clip_name") or d.get("clip") or None
#             out.append({
#                 "id": str(d["_id"]),
#                 "description": description,
#                 "status": str(status),
#                 "clip_name": clip_name,
#                 "timestamp": d.get("timestamp").isoformat() if d.get("timestamp") else None
#             })
#     return jsonify(out)
#
# @app.route("/api/neutralize/<id>", methods=["POST"])
# def api_neutralize(id):
#     try:
#         doc = collection.find_one({"_id": ObjectId(id)})
#     except Exception:
#         return jsonify({"error": "invalid id"}), 400
#     if not doc:
#         return jsonify({"error": "not found"}), 404
#
#     clip_name = doc.get("clip_name") or doc.get("clip")
#     if clip_name:
#         os.makedirs(NEUTRALIZED_DIR, exist_ok=True)
#         src = os.path.join(DETECTION_DIR, clip_name)
#         dst = os.path.join(NEUTRALIZED_DIR, clip_name)
#         # move file if present
#         if os.path.exists(src):
#             shutil.move(src, dst)
#
#     # update DB status (encrypt if possible)
#     collection.update_one({"_id": ObjectId(id)}, {"$set": {"status": encrypt_if_possible("Neutralized"), "neutralized_at": time.time()}})
#     return jsonify({"ok": True})
#
# @app.route("/api/clip_file/<path:filename>")
# def api_clip_file(filename):
#     # serve clip from detection or neutralized folders
#     det_path = os.path.join(DETECTION_DIR, filename)
#     neu_path = os.path.join(NEUTRALIZED_DIR, filename)
#     if os.path.exists(det_path):
#         return send_from_directory(DETECTION_DIR, filename)
#     if os.path.exists(neu_path):
#         return send_from_directory(NEUTRALIZED_DIR, filename)
#     return ("", 404)
#
# if __name__ == "__main__":
#     os.makedirs(DETECTION_DIR, exist_ok=True)
#     app.run(host="0.0.0.0", port=5000, debug=True)

# app.py
# from flask import Flask, render_template, send_from_directory, jsonify, request
# from pymongo import MongoClient
# from bson.objectid import ObjectId
# import os, shutil, time
# import datetime # Make sure this import is present
#
# # Try to load encryption key if provided (optional)
# try:
#     # IMPORTANT: Your file is named EncryptionConfig.py, ensure it's in the same directory
#     import EncryptionConfig
#     from cryptography.fernet import Fernet
#
#     cipher = Fernet(EncryptionConfig.ENCRYPTION_KEY)
# except Exception:
#     cipher = None
#     print("⚠️ Warning: EncryptionConfig.py not found or key is invalid. Data will not be decrypted.")
#
# # === CONFIG - adjust if you prefer env vars instead ===
# MONGO_CONNECTION_STRING = "mongodb+srv://gujarathibond:Divij&9475@atlas.i0mvluo.mongodb.net/?retryWrites=true&w=majority&appName=ATLAS"
# DETECTION_DIR = r"D:\DRDO\WeaponDetection(ATLAS)\detection_clips"
# NEUTRALIZED_DIR = "neutralized_clips"
#
# app = Flask(__name__, static_folder="static")
#
# # === Mongo setup ===
# client = MongoClient(MONGO_CONNECTION_STRING)
# db = client["security_events"]
# collection = db["threat_logs"]
#
#
# # === Helpers for (optional) encryption ===
# def decrypt_if_possible(val):
#     if val is None: return None
#     try:
#         if cipher:
#             if isinstance(val, (bytes, bytearray)):
#                 return cipher.decrypt(bytes(val)).decode()
#             # Handle cases where data might be stored as a string representation of bytes
#             if isinstance(val, str):
#                 return cipher.decrypt(val.encode()).decode()
#     except Exception:
#         # if decrypt fails, return original value to avoid crashing
#         return str(val)  # Return as a string to be safe
#     return val
#
#
# def encrypt_if_possible(s):
#     if cipher and isinstance(s, str):
#         return cipher.encrypt(s.encode())
#     return s
#
#
# # === Routes / Pages ===
# @app.route("/")
# def index():
#     return render_template("live_feed.html")
#
#
# @app.route("/live_threats")
# def live_threats_page():
#     return render_template("live_threats.html")
#
#
# @app.route("/neutralized")
# def neutralized_page():
#     return render_template("neutralized.html")
#
#
# @app.route("/police_stations")
# def police_page():
#     return render_template("police_stations.html")
#
#
# # === API Endpoints ===
# @app.route("/api/threats")
# def api_threats():
#     docs = collection.find().sort("timestamp", -1).limit(200)
#     out = []
#     for d in docs:
#         status = decrypt_if_possible(d.get("status"))
#         if status and "Neutral" in str(status):
#             continue
#
#         # --- MODIFIED SECTION: Fetching and decrypting all fields ---
#         out.append({
#             "id": str(d["_id"]),
#             "description": decrypt_if_possible(d.get("description")) or "No description",
#             "status": status,
#             "officer": decrypt_if_possible(d.get("officer")),
#             "location": d.get("location"), # Location is not encrypted in the detection script
#             "camera": d.get("camera"),  # Camera is not encrypted
#             "clip_name": d.get("clip_name"),
#             "timestamp": d.get("timestamp").isoformat() if d.get("timestamp") else None
#         })
#     return jsonify(out)
#
#
# @app.route("/api/neutralized")
# def api_neutralized_list():
#     docs = collection.find().sort("timestamp", -1).limit(500)
#     out = []
#     for d in docs:
#         status = decrypt_if_possible(d.get("status"))
#         if status and "Neutral" in str(status):
#             out.append({
#                 "id": str(d["_id"]),
#                 "description": decrypt_if_possible(d.get("description")) or "No description",
#                 "status": status,
#                 "officer": decrypt_if_possible(d.get("officer")),
#                 "location": d.get("location"),
#                 "camera": d.get("camera"),
#                 "clip_name": d.get("clip_name"),
#                 "timestamp": d.get("timestamp").isoformat() if d.get("timestamp") else None
#             })
#     return jsonify(out)
#
#
# @app.route("/api/neutralize/<id>", methods=["POST"])
# def api_neutralize(id):
#     try:
#         doc = collection.find_one({"_id": ObjectId(id)})
#     except Exception:
#         return jsonify({"error": "invalid id"}), 400
#     if not doc:
#         return jsonify({"error": "not found"}), 404
#
#     clip_name = doc.get("clip_name")
#     if clip_name:
#         os.makedirs(NEUTRALIZED_DIR, exist_ok=True)
#         src = os.path.join(DETECTION_DIR, clip_name)
#         dst = os.path.join(NEUTRALIZED_DIR, clip_name)
#         if os.path.exists(src):
#             try:
#                 shutil.move(src, dst)
#             except Exception as e:
#                 print(f"Could not move file {src} to {dst}: {e}")
#
#     # --- FIX: Changed datetime.now() to datetime.datetime.now() ---
#     collection.update_one({"_id": ObjectId(id)},
#                           {"$set": {"status": encrypt_if_possible("Neutralized"), "neutralized_at": datetime.datetime.now()}})
#     return jsonify({"ok": True})
#
#
# @app.route("/api/clip_file/<path:filename>")
# def api_clip_file(filename):
#     # serve clip from detection or neutralized folders
#     det_path = os.path.join(DETECTION_DIR, filename)
#     neu_path = os.path.join(NEUTRALIZED_DIR, filename)
#     if os.path.exists(det_path):
#         return send_from_directory(DETECTION_DIR, filename)
#     if os.path.exists(neu_path):
#         return send_from_directory(NEUTRALIZED_DIR, filename)
#     print(f"Clip not found: {filename}")
#     return ("", 404)
#
#
# if __name__ == "__main__":
#     os.makedirs(DETECTION_DIR, exist_ok=True)
#     os.makedirs(NEUTRALIZED_DIR, exist_ok=True)
#     app.run(host="0.0.0.0", port=5000, debug=True)

# app.py
from flask import Flask, render_template, jsonify, request, Response
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
import datetime
import gridfs

try:
    import EncryptionConfig
    from cryptography.fernet import Fernet

    cipher = Fernet(EncryptionConfig.ENCRYPTION_KEY)
except Exception:
    cipher = None
    print("⚠️ Warning: EncryptionConfig not found or invalid. Data will not be decrypted.")

# === CONFIG ===
MONGO_CONNECTION_STRING = "mongodb+srv://gujarathibond:Divij&9475@atlas.i0mvluo.mongodb.net/?retryWrites=true&w=majority&appName=ATLAS"
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
NEUTRALIZED_DIR = os.path.join(BASE_DIR, "neutralized_clips")

app = Flask(__name__, static_folder="static")

# === Mongo & GridFS setup ===
client = MongoClient(MONGO_CONNECTION_STRING)
db = client["security_events"]
collection = db["threat_logs"]
fs = gridfs.GridFS(db)


# === Helper Functions ===
def decrypt_if_possible(val):
    if val is None:
        return None
    try:
        if cipher and isinstance(val, (bytes, bytearray)):
            return cipher.decrypt(bytes(val)).decode()
    except Exception:
        return str(val)
    return val


def encrypt_if_possible(s):
    if cipher and isinstance(s, str):
        return cipher.encrypt(s.encode())
    return s


# === Routes / Pages ===
@app.route("/")
def index():
    return render_template("live_feed.html")


@app.route("/live_threats")
def live_threats_page():
    return render_template("live_threats.html")


@app.route("/neutralized")
def neutralized_page():
    return render_template("neutralized.html")


@app.route("/police_stations")
def police_page():
    return render_template("police_stations.html")


# === API Endpoints ===
@app.route("/api/threats")
def api_threats():
    docs = collection.find().sort("timestamp", -1).limit(200)
    out = []
    for d in docs:
        status = decrypt_if_possible(d.get("status"))
        if status and "Neutral" in str(status):
            continue

        out.append({
            "id": str(d["_id"]),
            "description": decrypt_if_possible(d.get("description")) or "N/A",
            "status": status,
            "officer": decrypt_if_possible(d.get("officer")),
            "location": d.get("location"),
            "camera": d.get("camera"),
            "clip_gridfs_id": str(d.get("clip_gridfs_id")) if d.get("clip_gridfs_id") else None,
            "gridfs_snapshot_id": str(d.get("gridfs_snapshot_id")) if d.get("gridfs_snapshot_id") else None,
            "snapshot_path": d.get("snapshot_path"),  # local path backup (if exists)
            "clip_name": d.get("clip_name"),
            "timestamp": d.get("timestamp").isoformat() if d.get("timestamp") else None
        })
    return jsonify(out)


@app.route("/api/neutralized")
def api_neutralized_list():
    docs = collection.find().sort("timestamp", -1).limit(500)
    out = []
    for d in docs:
        status = decrypt_if_possible(d.get("status"))
        if status and "Neutral" in str(status):
            out.append({
                "id": str(d["_id"]),
                "description": decrypt_if_possible(d.get("description")) or "N/A",
                "status": status,
                "officer": decrypt_if_possible(d.get("officer")),
                "location": d.get("location"),
                "camera": d.get("camera"),
                "clip_gridfs_id": str(d.get("clip_gridfs_id")) if d.get("clip_gridfs_id") else None,
                "gridfs_snapshot_id": str(d.get("gridfs_snapshot_id")) if d.get("gridfs_snapshot_id") else None,
                "snapshot_path": d.get("snapshot_path"),
                "clip_name": d.get("clip_name"),
                "timestamp": d.get("timestamp").isoformat() if d.get("timestamp") else None
            })
    return jsonify(out)


@app.route("/api/neutralize/<id>", methods=["POST"])
def api_neutralize(id):
    try:
        doc = collection.find_one({"_id": ObjectId(id)})
    except Exception:
        return jsonify({"error": "invalid id"}), 400
    if not doc:
        return jsonify({"error": "not found"}), 404

    # delete video if in GridFS
    gridfs_id = doc.get("clip_gridfs_id")
    if gridfs_id and fs.exists(ObjectId(gridfs_id)):
        fs.delete(ObjectId(gridfs_id))
        print(f"Deleted clip from GridFS with ID: {gridfs_id}")

    # delete snapshot if in GridFS
    snap_id = doc.get("gridfs_snapshot_id")
    if snap_id and fs.exists(ObjectId(snap_id)):
        fs.delete(ObjectId(snap_id))
        print(f"Deleted snapshot from GridFS with ID: {snap_id}")

    collection.update_one({"_id": ObjectId(id)},
                          {"$set": {"status": encrypt_if_possible("Neutralized"),
                                    "neutralized_at": datetime.datetime.now()}})
    return jsonify({"ok": True})


# === Routes to serve GridFS files ===
@app.route("/gridfs/<file_id>")
def get_file(file_id):
    """Serve video files from GridFS"""
    try:
        file_obj = fs.get(ObjectId(file_id))
        return Response(file_obj.read(), mimetype="video/mp4")
    except Exception as e:
        return jsonify({"error": f"File not found: {e}"}), 404


@app.route("/gridfs_image/<file_id>")
def get_image(file_id):
    """Serve snapshot images from GridFS"""
    try:
        file_obj = fs.get(ObjectId(file_id))
        return Response(file_obj.read(), mimetype="image/jpeg")
    except Exception as e:
        return jsonify({"error": f"Image not found: {e}"}), 404


if __name__ == "__main__":
    os.makedirs(NEUTRALIZED_DIR, exist_ok=True)
    app.run(host="0.0.0.0", port=5000, debug=True)



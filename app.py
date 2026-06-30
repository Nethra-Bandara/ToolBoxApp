
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import send_from_directory
import os

from detector import process_image
from database import *

app = Flask(__name__)

UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER", "data/uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

init_db()


@app.route("/")
def home():
    box_count = get_box_count()
    item_count = get_item_count()

    return render_template(
        "index.html",
        box_count=box_count,
        item_count=item_count,
    )


#######################################################
# HANDOVER
#######################################################

@app.route("/handover", methods=["GET", "POST"])
def handover():

    if request.method == "POST":

        image = request.files["image"]

        filepath = os.path.join(
            UPLOAD_FOLDER,
            image.filename
        )

        image.save(filepath)

        box_no, items, segmented_path = process_image(filepath)

        add_items(box_no, items)

        return render_template(
            "inventory.html",
            title="Handover",
            box_no=box_no,
            items=items,
            cleared=False,
            segmented_path=segmented_path
        )

    return render_template(
        "upload.html",
        action="Handover"
    )


#######################################################
# RECEIVE
#######################################################

@app.route("/receive", methods=["GET", "POST"])
def receive():

    if request.method == "POST":

        image = request.files["image"]

        filepath = os.path.join(
            UPLOAD_FOLDER,
            image.filename
        )

        image.save(filepath)

        box_no, items, segmented_path = process_image(filepath)

        stored = get_items(box_no)

        missing = list(
            set(stored) - set(items)
        )

        update_missing(box_no, missing)

        cleared = False

        if len(missing) == 0:
            cleared = True

        return render_template(
            "inventory.html",
            title="Receive",
            box_no=box_no,
            items=missing,
            cleared=cleared,
            segmented_path=segmented_path
        )

    return render_template(
        "upload.html",
        action="Receive"
    )


#######################################################
# INVENTORY PAGE
#######################################################

@app.route("/inventory")
def inventory():

    rows = get_all_boxes()

    data = {}

    for box_no, item in rows:

        if box_no not in data:
            data[box_no] = []

        data[box_no].append(item)

    return render_template(
        "inventory_table.html",
        data=data
    )


@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


@app.route("/clear_box", methods=["POST"])
def clear_box():
    box_no = request.form.get("box_no")

    if box_no:
        delete_box(box_no)

    return redirect("/inventory")


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=False
    )
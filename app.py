from flask import Flask, render_template, request, redirect, session, jsonify
import sqlite3
import os

if not os.path.exists("players.db"):
    import init_db
app = Flask(__name__)
app.secret_key = "iplauctionsecret"


def get_db():
    conn = sqlite3.connect("players.db")
    conn.row_factory = sqlite3.Row
    return conn


# LOGIN PAGE
@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()

        user = conn.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username,password)
        ).fetchone()

        conn.close()

        if user:
            session["user_id"] = user["id"]
            session["username"] = user["username"]

            return redirect("/")

    return render_template("login.html")


# LOGOUT
@app.route("/logout")
def logout():

    session.clear()
    return redirect("/login")


# HOME PAGE (AUCTION)
@app.route("/")
def home():

    if "user_id" not in session:
        return redirect("/login")

    conn = get_db()

    country = request.args.get("country")
    role = request.args.get("role")

    query = "SELECT * FROM players WHERE 1=1"
    params = []

    if country:
        query += " AND country=?"
        params.append(country)

    if role:
        query += " AND role=?"
        params.append(role)

    query += " ORDER BY current_price DESC"

    players = conn.execute(query, params).fetchall()

    conn.close()

    return render_template(
        "index.html",
        players=players,
        username=session["username"]
    )


# PLACE BID
@app.route("/bid", methods=["POST"])
def bid():

    if "user_id" not in session:
        return jsonify({"status":"login required"})

    data = request.json

    player_id = data["player_id"]
    bid_amount = data["bid_amount"]
    user_id = session["user_id"]

    conn = get_db()

    player = conn.execute(
        "SELECT current_price FROM players WHERE id=?",
        (player_id,)
    ).fetchone()

    if bid_amount <= player["current_price"]:
        return jsonify({"status":"invalid bid"})

    conn.execute(
        "UPDATE players SET current_price=? WHERE id=?",
        (bid_amount,player_id)
    )

    conn.execute(
        "INSERT INTO bids(player_id,user_id,bid_amount) VALUES(?,?,?)",
        (player_id,user_id,bid_amount)
    )

    conn.commit()
    conn.close()

    return jsonify({"status":"success"})


# BID HISTORY (for later graphs)
@app.route("/bids/<int:player_id>")
def bids(player_id):

    conn = get_db()

    rows = conn.execute(
    """
    SELECT users.username,bids.bid_amount,bids.bid_time
    FROM bids
    JOIN users ON bids.user_id = users.id
    WHERE player_id=?
    ORDER BY bid_time
    """,
    (player_id,)
    ).fetchall()

    conn.close()

    data = []

    for r in rows:
        data.append({
            "team": r["username"],
            "price": r["bid_amount"],
            "time": r["bid_time"]
        })

    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)


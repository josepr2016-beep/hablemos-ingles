import os
from datetime import date, timedelta

from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy

from content import PAIRS, UNITS

app = Flask(__name__)

db_url = os.environ.get("DATABASE_URL", "sqlite:///hablemos.db")
# Render entrega postgres:// o postgresql://; se fija el conector psycopg2 de forma explícita.
for prefix in ("postgres://", "postgresql://"):
    if db_url.startswith(prefix):
        db_url = "postgresql+psycopg2://" + db_url[len(prefix):]
        break
app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"pool_pre_ping": True}
db = SQLAlchemy(app)

# Repaso espaciado (cajas de Leitner): días hasta el próximo repaso según la caja.
INTERVALS = {1: 1, 2: 2, 3: 4, 4: 7, 5: 15}
PHRASE_IDS = [p["id"] for u in UNITS for p in u["phrases"]]


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    avatar = db.Column(db.String(8), nullable=False, default="🙂")


class Progress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey("profile.id"), nullable=False, index=True)
    item_id = db.Column(db.String(20), nullable=False)
    box = db.Column(db.Integer, nullable=False, default=0)
    due = db.Column(db.Date)
    best = db.Column(db.Integer, nullable=False, default=0)
    attempts = db.Column(db.Integer, nullable=False, default=0)
    __table_args__ = (db.UniqueConstraint("profile_id", "item_id"),)


class DayLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey("profile.id"), nullable=False, index=True)
    day = db.Column(db.Date, nullable=False)
    points = db.Column(db.Integer, nullable=False, default=0)
    __table_args__ = (db.UniqueConstraint("profile_id", "day"),)


with app.app_context():
    db.create_all()


def get_day(value):
    """El navegador envía su fecha local para que la racha no dependa de la hora del servidor."""
    try:
        return date.fromisoformat(value)
    except (TypeError, ValueError):
        return date.today()


def summary(profile, day):
    logs = DayLog.query.filter_by(profile_id=profile.id).all()
    days = {log.day: log.points for log in logs}
    d = day if day in days else day - timedelta(days=1)
    streak = 0
    while d in days:
        streak += 1
        d -= timedelta(days=1)
    return {
        "id": profile.id,
        "name": profile.name,
        "avatar": profile.avatar,
        "streak": streak,
        "today_points": days.get(day, 0),
        "total_points": sum(days.values()),
    }


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/content")
def content():
    return jsonify({"units": UNITS, "pairs": PAIRS})


@app.route("/api/profiles", methods=["GET", "POST"])
def profiles():
    day = get_day(request.args.get("day"))
    if request.method == "POST":
        data = request.get_json(silent=True) or {}
        name = str(data.get("name", "")).strip()[:40]
        if not name:
            return jsonify({"error": "Escribe un nombre"}), 400
        p = Profile(name=name, avatar=str(data.get("avatar", "🙂"))[:8] or "🙂")
        db.session.add(p)
        db.session.commit()
        return jsonify(summary(p, day))
    return jsonify([summary(p, day) for p in Profile.query.order_by(Profile.id).all()])


@app.route("/api/profiles/<int:pid>", methods=["DELETE"])
def delete_profile(pid):
    p = db.get_or_404(Profile, pid)
    Progress.query.filter_by(profile_id=pid).delete()
    DayLog.query.filter_by(profile_id=pid).delete()
    db.session.delete(p)
    db.session.commit()
    return jsonify({"ok": True})


@app.route("/api/profiles/<int:pid>/state")
def state(pid):
    p = db.get_or_404(Profile, pid)
    day = get_day(request.args.get("day"))
    rows = Progress.query.filter_by(profile_id=pid).all()
    out = summary(p, day)
    out["progress"] = {r.item_id: {"box": r.box, "best": r.best} for r in rows}
    out["due_count"] = sum(1 for r in rows if r.item_id in PHRASE_IDS and r.due and r.due <= day)
    return jsonify(out)


@app.route("/api/profiles/<int:pid>/daily")
def daily(pid):
    db.get_or_404(Profile, pid)
    day = get_day(request.args.get("day"))
    rows = Progress.query.filter_by(profile_id=pid).all()
    seen = {r.item_id for r in rows}
    due = sorted(
        (r for r in rows if r.item_id in PHRASE_IDS and r.due and r.due <= day),
        key=lambda r: r.due,
    )[:6]
    new = [i for i in PHRASE_IDS if i not in seen][: 10 - len(due) if len(due) < 6 else 4]
    return jsonify([r.item_id for r in due] + new)


@app.route("/api/profiles/<int:pid>/result", methods=["POST"])
def result(pid):
    db.get_or_404(Profile, pid)
    data = request.get_json(silent=True) or {}
    item_id = str(data.get("item_id", ""))[:20]
    try:
        score = max(0, min(100, int(data.get("score", 0))))
    except (TypeError, ValueError):
        score = 0
    day = get_day(data.get("day"))

    pr = Progress.query.filter_by(profile_id=pid, item_id=item_id).first()
    if not pr:
        pr = Progress(profile_id=pid, item_id=item_id, box=0, best=0, attempts=0)
        db.session.add(pr)
    pr.attempts += 1
    pr.best = max(pr.best, score)
    if score >= 80:
        pr.box = min(5, pr.box + 1)
        pr.due = day + timedelta(days=INTERVALS[pr.box])
    elif score >= 50:
        pr.box = max(1, pr.box)
        pr.due = day + timedelta(days=1)
    else:
        pr.box = 1
        pr.due = day

    log = DayLog.query.filter_by(profile_id=pid, day=day).first()
    if not log:
        log = DayLog(profile_id=pid, day=day, points=0)
        db.session.add(log)
    log.points += max(1, round(score / 10))
    db.session.commit()
    return jsonify({"ok": True, "box": pr.box})


if __name__ == "__main__":
    app.run(debug=True, port=5000)

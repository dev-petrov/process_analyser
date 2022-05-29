import json
from datetime import datetime, timedelta
from io import BytesIO

import pandas as pd
from flask import Flask, Response, jsonify, request, send_from_directory
from sqlalchemy import desc

from detector.aggregator import Aggregator
from detector.db import AnomalyLog, RawValue, Session, get_engine, session_scope
from detector.settings import API_TOKEN

from .json_encoder import CustomJSONEncoder

assert API_TOKEN, "API_TOKEN should be defined"

app = Flask(__name__, static_url_path="")

app.json_encoder = CustomJSONEncoder

Session.configure(bind=get_engine())


def row_as_dict(row):
    d = row.__dict__
    d.pop("_sa_instance_state")
    if "reason" in d:
        d["reason"] = json.loads(d["reason"])
    return d


@app.route("/", endpoint="index")
def index():
    return send_from_directory("static", "", "index.html")


@app.route("/check_token")
def check_token():
    return jsonify(detail="Correct")


@app.route("/api/anomaly/")
def anomaly_list():
    with session_scope() as session:
        return jsonify([row_as_dict(r) for r in session.query(AnomalyLog).order_by(desc(AnomalyLog.dttm))])


@app.route("/api/anomaly/<int:id>/")
def anomaly(id):
    with session_scope() as session:
        log = session.query(AnomalyLog).get(id)
        if log is None:
            response = jsonify(detail="Not found")
            response.status_code = 404
            return response
        return jsonify(row_as_dict(log))


@app.route("/api/closest_raw_values/")
def closest_raw_values():
    dttm = request.args.get("dttm")
    if not dttm:
        response = jsonify(detail="dttm is required")
        response.status_code = 400
        return response

    dttm = datetime.fromisoformat(dttm)

    dttm_from = dttm - timedelta(minutes=Aggregator.period_length)
    dttm_to = dttm

    with session_scope() as session:
        return jsonify(
            [
                row_as_dict(r)
                for r in session.query(RawValue)
                .filter(
                    RawValue.dttm > dttm_from,
                    RawValue.dttm <= dttm_to,
                )
                .order_by(desc(RawValue.dttm))
            ]
        )


@app.route("/api/closest_raw_values_report/")
def closest_raw_values_excel():
    dttm = request.args.get("dttm")
    if not dttm:
        response = jsonify(detail="dttm is required")
        response.status_code = 400
        return response

    dttm = datetime.fromisoformat(dttm)

    dttm_from = dttm - timedelta(minutes=Aggregator.period_length)
    dttm_to = dttm

    with session_scope() as session:
        raw_values = [
            row_as_dict(r)
            for r in session.query(RawValue)
            .filter(
                RawValue.dttm > dttm_from,
                RawValue.dttm <= dttm_to,
            )
            .order_by(desc(RawValue.dttm))
        ]
        output = BytesIO()
        df = pd.DataFrame(data=raw_values)
        df.to_excel(output, index=False)
        output.seek(0)
        return Response(
            output,
            headers={
                "Content-Disposition": f"attachment; filename=Raw values for anomaly {dttm}.xlsx",
                "Content-type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            },
        )


@app.before_request
def before_request_callback():
    if request.endpoint not in ["index", "static"]:
        token = request.headers.get("Authorization")

        if not token:
            response = jsonify(detail="Авторизация обязательна")
            response.status_code = 403
            return response

        try:
            method, token = token.split()
        except Exception:
            response = jsonify(detail="Некорректный формат токена")
            response.status_code = 401
            return response

        try:
            assert method == "Token", "Метод авторизации должен быть Token"
            assert token == API_TOKEN, "Некорректный токен"
        except AssertionError as e:
            response = jsonify(detail=str(e))
            response.status_code = 401
            return response

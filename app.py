from typing import List

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.sql.expression import any_
from sqlalchemy.orm import sessionmaker
from models import Intonation, Semantics, SpeechAct, DF

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

engine = create_engine('postgres+psycopg2://wnishjci:JtKBFR-ksN92wn6JS1PX9ZdG1Y3pj9DN@ziggy.db.elephantsql.com:5432'
                       '/wnishjci')
db.Model.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def merge_dfs(dfs: List["DF"]):
    merged = {}
    for df in dfs:
        if df.df in merged:
            check = merged[df.df]
            if df.language == check['language'] and df.primary_semantics_id == check['primary_semantics_id'] \
                    and df.speech_act_1_id == check['speech_act_1_id'] and df.speech_act_id == check['speech_act_id']:
                check['additional_semantics'].append(df.additional_semantics.semantics)
        else:
            merged[df.df] = df.__dict__
            merged[df.df]['additional_semantics'] = [df.additional_semantics.semantics]
            merged[df.df]['primary_semantics'] = df.primary_semantics
            merged[df.df]['speech_act'] = df.speech_act
    return list(merged.values())


@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/result', methods=['get'])
def result():
    if not request.args:
        return redirect(url_for('hello'))
    all_languages = any_(['ru', 'sr'])
    all_semantics = any_([x.semantics for x in session.query(Semantics).all()])
    all_speech_acts = any_([x.speech_act for x in session.query(SpeechAct).all()])
    word = request.args.get('word')
    language = request.args.get('language')
    if not language:
        language = all_languages
    pr_sem = request.args.get('pr_sem')
    if not pr_sem:
        pr_sem = all_semantics
    speech_act = request.args.get('speech_act')
    if not speech_act:
        speech_act = all_speech_acts
    add_sem = request.args.getlist('add_sem')
    if not add_sem:
        add_sem = all_semantics
    else:
        add_sem = any_(add_sem)

    new_query = session.query(DF)
    records = new_query.filter(DF.language == language,
                               DF.primary_semantics.has(Semantics.semantics == pr_sem),
                               DF.speech_act.has(SpeechAct.speech_act == speech_act),
                               DF.additional_semantics.has(Semantics.semantics == add_sem)).all()

    records = merge_dfs(records)

    return render_template('result.html', records=records)


if __name__ == '__main__':
    app.run()

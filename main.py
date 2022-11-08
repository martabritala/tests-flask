import datetime
import os
import psycopg2
from flask import Flask, g, render_template
from data import varda_diena, menesa_vardi, diena, filma_no_id, filmas_vecakas_par

app = Flask('app')


@app.route('/')
def index_lapa():
    return render_template('vardadienas.html')


@app.route('/healthcheck')
def hc():
    return "OK"


# vardadienu routes
@app.route('/vd/<vards>')
def vd_kad(vards):
    atbilde = varda_diena(vards)
    print(type(atbilde))
    resultats = {
        "vards": atbilde[0],
        "m": "{:02d}".format(atbilde[2]),
        "d": atbilde[1]
    }
    return render_template('vardadienas.html', vardi=[resultats])


@app.route('/vd/satur/<teksts>')
def vd_satur(teksts):
    atbilde = varda_dala(teksts)
    print(type(atbilde))
    resultats = []
    for v in atbilde:
        print(v)
        resultats.append({
            "vards": v[0],
            "m": "{:02d}".format(v[2]),
            "d": v[1]
        })
    return render_template('vardadienas.html', vardi=resultats)


@app.route('/vd/menesis/<menesis>')
def vd_diena(menesis):
    atbilde = menesa_vardi(menesis)
    resultats = []
    for v in atbilde:
        print(v)
        resultats.append({
            "vards": v[0],
            "m": "{:02d}".format(v[2]),
            "d": v[1]
        })
    return render_template('vardadienas.html', vardi=resultats)


@app.route('/vd/sodien')
def vd_sodien():
    sodiena = datetime.date.today()
    #ritdiena = datetime.date.today() + datetime.timedelta(days=1)
    atbilde = diena(sodiena.month, sodiena.day)
    resultats = []
    for v in atbilde:
        resultats.append({
            "vards": v[0],
            "m": "{:02d}".format(v[2]),
            "d": v[1]
        })
    return render_template('vardadienas.html', vardi=resultats)


# Filmu routes
@app.route('/filma/<fid>')
def filmas_info(fid):
    atbilde = filma_no_id(fid)
    return render_template('filma.html', filma=atbilde)


# Kad pieprasījums beidzies, aizver savienojumu ar datubāzi
@app.teardown_appcontext
def close_db(error):
    """Close the db connection when the current request ends
    """
    db_conn = g.pop('db', None)

    if db_conn is not None:
        db_conn.close()


app.run(host='0.0.0.0', port=8020)

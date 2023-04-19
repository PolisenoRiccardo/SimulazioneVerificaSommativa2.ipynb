import io
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from flask import Flask, render_template, request, Response
app = Flask(__name__)

import pandas as pd
df = pd.read_excel("https://github.com/wtitze/3E/blob/main/BikeStores.xls?raw=true", sheet_name='customers')
groupby = df.groupby('state').count()['customer_id'].reset_index().sort_values(by='customer_id', ascending=False)
@app.route('/', methods=['GET'])
def form():
    return render_template('home.html')

@app.route('/nome', methods=['GET'])
def nome1(): 
    return render_template('input1.html')

@app.route('/risultatonome', methods=['GET'])
def nome():
    nome = request.args.get('box')
    cognome = request.args.get('box1')
    table = df[(df['first_name'].str.contains(nome)) & (df['last_name'].str.contains(cognome))]
    return render_template('risultato.html', table = table.to_html())

@app.route('/citta', methods=['GET'])
def citta():
    cities = df['city'].tolist()
    return render_template('input2.html', cities = list(set(cities)))

@app.route('/citta/<city>', methods=['GET'])
def città1(city):
    table = df[df['city'].str.contains(city)]
    return render_template('risultato.html', table = table.to_html())

@app.route('/numeroclienti', methods=['GET'])
def numeroclienti():
    return render_template('risultato.html', table = groupby.to_html())

@app.route('/statoclienti', methods=['GET'])
def statoclienti():
    table = groupby[groupby['customer_id'] == groupby['customer_id'].max()]['state']
    return render_template('risultato.html', table = table.tolist())

@app.route('/grafici', methods=['GET'])
def grafici():   
    dati = groupby['customer_id']
    labels = groupby['state']
    
    fig, ax = plt.subplots()   
    ax.bar(labels, dati)
    plt.xticks(rotation=45)
    plt.title('Numero di prodotti per categoria')
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/grafici1', methods=['GET'])
def grafici1():   
    dati = groupby['customer_id']
    labels = groupby['state']
    
    fig, ax = plt.subplots()   
    ax.barh(labels, dati)
    plt.xticks(rotation=45)
    plt.title('Numero di prodotti per categoria')
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/grafici2', methods=['GET'])
def grafici2():   
    dati = groupby['customer_id']
    labels = groupby['state']
    
    fig, ax = plt.subplots()
    ax.pie(dati, labels=labels)
    plt.xticks(rotation=45)
    plt.title('Numero di prodotti per categoria')
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


@app.route('/noMail', methods=['GET'])
def risultatonoMail():
    table =df[df['email'].isna()][['first_name','last_name', 'phone']]
    return render_template('risultato.html', table = table.to_html())

@app.route('/provider', methods=['GET'])
def provider():
    return render_template('input3.html')

@app.route('/risultatoprovider', methods=['GET'])
def risultatoprovider():
    provider = request.args.get('provider')
    risultato = df[df['email'].str.endswith(f'@{provider}', na=False)][['first_name', 'last_name']]
    if len(risultato) == 0:
        return  ('<h1>Nessun cliente trovato</h1>')
    else:
        return render_template('risultato.html', table = risultato.to_html())




if __name__ == '__main__':
  app.run(host='0.0.0.0', port=32245, debug=True)
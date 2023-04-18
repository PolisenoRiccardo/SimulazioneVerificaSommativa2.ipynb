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
def città():
    return render_template('input2.html')

@app.route('/risultatocitta', methods=['GET'])
def città1():
    citta = request.args.get('citta')
    table = df[df['city'].str.contains(citta)]
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
    import io
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    
    dati = groupby['state']
    labels = dati.index
    
    fig, ax = plt.subplots()   
    ax.bar(dati, labels)
    plt.xticks(rotation=45)
    plt.title('Numero di prodotti per categoria')
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')
    return render_template('input.html')

@app.route('/noMail', methods=['GET'])
def noMail():
    return render_template('input.html')

@app.route('/provider', methods=['GET'])
def provider():
    return render_template('input.html')




if __name__ == '__main__':
  app.run(host='0.0.0.0', port=32245, debug=True)
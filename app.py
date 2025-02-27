from flask import Flask, render_template, request

app = Flask(__name__)

class ConsumoEnergetico:
    def __init__(self, nome, potencia, tempo, unidade, tarifa_kwh):
        self.nome = nome
        self.potencia = potencia
        self.tempo = tempo / 60 if unidade == 'm' else tempo
        self.tarifa_kwh = tarifa_kwh

    def calcular_consumo_diario(self):
        return (self.potencia * self.tempo) / 1000  # kWh/dia

    def calcular_consumo_mensal(self):
        return self.calcular_consumo_diario() * 30

    def calcular_custo_mensal(self):
        return round(self.calcular_consumo_mensal() * self.tarifa_kwh, 2)

    def sugestao_reducao(self, percentual=20):
        reducao_minutos = round((self.tempo * (percentual / 100)) * 60)  # Redução em minutos
        horas = reducao_minutos // 60
        minutos = reducao_minutos % 60
        novo_tempo = self.tempo - (reducao_minutos / 60)
        novo_consumo = (self.potencia * novo_tempo) / 1000 * 30
        novo_custo_mensal = round(novo_consumo * self.tarifa_kwh, 2)
        economia = round(self.calcular_custo_mensal() - novo_custo_mensal, 2)

        if horas > 0 and minutos > 0:
            reducao_texto = f"{horas} hora e {minutos} minutos"
        elif horas > 0:
            reducao_texto = f"{horas} hora" if horas == 1 else f"{horas} horas"
        else:
            reducao_texto = f"{minutos} minutos"

        return f"Se reduzir {reducao_texto} por dia, economizará R$ {economia} por mês."

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nome = request.form['nome']
        potencia = float(request.form['potencia'])
        unidade = request.form['unidade']
        tempo = float(request.form['tempo'])
        tarifa_kwh = 0.95  # Tarifa média de energia (R$/kWh)

        consumo = ConsumoEnergetico(nome, potencia, tempo, unidade, tarifa_kwh)
        consumo_mensal = consumo.calcular_consumo_mensal()
        custo_mensal = consumo.calcular_custo_mensal()
        sugestao = consumo.sugestao_reducao()

        return render_template('index.html', consumo_mensal=consumo_mensal, custo_mensal=custo_mensal, sugestao=sugestao)

    return render_template('index.html', consumo_mensal=None, custo_mensal=None, sugestao=None)

if __name__ == '__main__':
    app.run(debug=True)
import flet as ft
import uuid
from datetime import datetime


class Cliente:
    def __init__(self, nome, telefone, email):
        self.id = str(uuid.uuid4())
        self.nome = nome
        self.telefone = telefone
        self.email = email

    def __str__(self):
        return f"{self.nome} ({self.email})"

class Quarto:
    def __init__(self, numero, tipo, preco_diaria):
        self.numero = numero
        self.tipo = tipo
        self.preco_diaria = preco_diaria
        self.disponivel = True

    def __str__(self):
        status = "Disponível" if self.disponivel else "Ocupado"
        return f"Quarto {self.numero} - {self.tipo} - R${self.preco_diaria:.2f} - {status}"

class Reserva:
    def __init__(self, cliente, quarto, check_in, check_out):
        self.id = str(uuid.uuid4())
        self.cliente = cliente
        self.quarto = quarto
        self.check_in = check_in
        self.check_out = check_out
        self.status = "Ativa"

    def __str__(self):
        return f"Reserva {self.id[:8]} - {self.cliente.nome} - Quarto {self.quarto.numero} - {self.check_in} a {self.check_out} - {self.status}"

class GerenciadorDeReservas:
    def __init__(self):
        self.clientes = []
        self.quartos = []
        self.reservas = []

    def adicionar_cliente(self, cliente):
        self.clientes.append(cliente)

    def adicionar_quarto(self, quarto):
        self.quartos.append(quarto)

    def criar_reserva(self, cliente_id, numero_quarto, check_in, check_out):
        cliente = next((c for c in self.clientes if c.id == cliente_id), None)
        quarto = next((q for q in self.quartos if q.numero == numero_quarto and q.disponivel), None)

        if cliente and quarto:
            reserva = Reserva(cliente, quarto, check_in, check_out)
            self.reservas.append(reserva)
            quarto.disponivel = False
            return reserva
        return None

    def cancelar_reserva(self, reserva_id):
        for reserva in self.reservas:
            if reserva.id == reserva_id and reserva.status == "Ativa":
                reserva.status = "Cancelada"
                reserva.quarto.disponivel = True
                return True
        return False

    def listar_reservas(self):
        return self.reservas

    def listar_clientes(self):
        return self.clientes



gerenciador = GerenciadorDeReservas()

gerenciador.adicionar_quarto(Quarto(101, "single", 200.0))
gerenciador.adicionar_quarto(Quarto(102, "double", 300.0))
gerenciador.adicionar_quarto(Quarto(103, "suite", 500.0))



def main(pagina: ft.Page):
    pagina.title = "Refúgio dos Sonhos - Sistema de Reservas"
    pagina.window_width = 800
    pagina.window_height = 600

    def ir_para_inicio(e=None):
        pagina.controls.clear()
        pagina.add(
            ft.Text("Refúgio dos Sonhos - Quartos Disponíveis", size=24, weight="bold"),
        )
        lista = ft.Column()
        for quarto in gerenciador.quartos:
            status = "✅ Disponível" if quarto.disponivel else "❌ Ocupado"
            lista.controls.append(ft.Text(f"{quarto.numero} - {quarto.tipo} - R${quarto.preco_diaria:.2f} - {status}"))
        pagina.add(lista)
        pagina.add(
            ft.Row([
                ft.ElevatedButton("Fazer Reserva", on_click=ir_para_reserva),
                ft.ElevatedButton("Gerenciar Clientes", on_click=ir_para_clientes),
                ft.ElevatedButton("Visualizar Reservas", on_click=ir_para_visualizar_reservas)
            ])
        )
        pagina.update()

    def ir_para_clientes(e=None):
        pagina.controls.clear()
        titulo = ft.Text("Gerenciamento de Clientes", size=22, weight="bold")

        lista_clientes = ft.Column()
        for c in gerenciador.clientes:
            lista_clientes.controls.append(ft.Text(f"{c.nome} - {c.email} - {c.telefone}"))

        nome = ft.TextField(label="Nome")
        telefone = ft.TextField(label="Telefone")
        email = ft.TextField(label="E-mail")

        def adicionar_cliente(e):
            if nome.value and email.value:
                novo = Cliente(nome.value, telefone.value, email.value)
                gerenciador.adicionar_cliente(novo)
                ir_para_clientes()

        pagina.add(
            titulo,
            lista_clientes,
            ft.Text("Novo Cliente", size=16, weight="bold"),
            nome, telefone, email,
            ft.ElevatedButton("Salvar", on_click=adicionar_cliente),
            ft.ElevatedButton("Voltar", on_click=ir_para_inicio)
        )
        pagina.update()

    def ir_para_reserva(e=None):
        pagina.controls.clear()
        titulo = ft.Text("Nova Reserva", size=22, weight="bold")

        dropdown_clientes = ft.Dropdown(label="Cliente")
        for c in gerenciador.clientes:
            dropdown_clientes.options.append(ft.dropdown.Option(c.id, text=c.nome))

        dropdown_quartos = ft.Dropdown(label="Quarto")
        for q in gerenciador.quartos:
            if q.disponivel:
                dropdown_quartos.options.append(ft.dropdown.Option(q.numero, text=f"{q.numero} - {q.tipo}"))

        data_checkin = ft.TextField(label="Check-in (AAAA-MM-DD)")
        data_checkout = ft.TextField(label="Check-out (AAAA-MM-DD)")

        msg = ft.Text("", color="red")

        def reservar(e):
            try:
                checkin = datetime.strptime(data_checkin.value, "%Y-%m-%d").date()
                checkout = datetime.strptime(data_checkout.value, "%Y-%m-%d").date()
                res = gerenciador.criar_reserva(dropdown_clientes.value, int(dropdown_quartos.value), checkin, checkout)
                if res:
                    msg.value = "✅ Reserva feita com sucesso!"
                else:
                    msg.value = "❌ Erro ao criar reserva."
            except:
                msg.value = "❌ Datas inválidas!"
            pagina.update()

        pagina.add(
            titulo,
            dropdown_clientes,
            dropdown_quartos,
            data_checkin,
            data_checkout,
            ft.ElevatedButton("Confirmar Reserva", on_click=reservar),
            msg,
            ft.ElevatedButton("Voltar", on_click=ir_para_inicio)
        )
        pagina.update()

    def ir_para_visualizar_reservas(e=None):
        pagina.controls.clear()
        titulo = ft.Text("Reservas Atuais", size=22, weight="bold")

        lista_reservas = ft.Column()
        for r in gerenciador.listar_reservas():
            texto = ft.Text(f"{r.cliente.nome} - Quarto {r.quarto.numero} - {r.check_in} a {r.check_out} - {r.status}")
            btn = ft.ElevatedButton("Cancelar", disabled=(r.status != "Ativa"))

            def cancelar_reserva(e, r=r):
                gerenciador.cancelar_reserva(r.id)
                ir_para_visualizar_reservas()

            btn.on_click = cancelar_reserva
            lista_reservas.controls.append(ft.Row([texto, btn]))

        pagina.add(
            titulo,
            lista_reservas,
            ft.ElevatedButton("Voltar", on_click=ir_para_inicio)
        )
        pagina.update()

    ir_para_inicio()

ft.app(target=main)
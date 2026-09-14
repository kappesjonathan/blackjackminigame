import tkinter as tk
from tkinter import ttk
from pathlib import Path
from blackjack import calcular_puntos, repartir_carta


class Aplicacion:
    def __init__(self):
        self.saldo = 500
        self.apuesta = 0
        self.raiz = tk.Tk()
        self.raiz.geometry('700x500')
        self.raiz.configure(bg='green')
        self.raiz.title('Blackjack')
        self.mostrar_menu()
        self.raiz.mainloop()

    def limpiar_ventana(self):
        for widget in self.raiz.winfo_children():
            widget.destroy()

    def mostrar_menu(self):
        self.limpiar_ventana()

        marco_centro = tk.Frame(self.raiz, bg='green')
        marco_centro.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        ruta_logo = Path(__file__).parent / 'images' / 'bjlogo.png'
        self.logo = tk.PhotoImage(file=str(ruta_logo)).subsample(10, 10)
        tk.Label(marco_centro, image=self.logo, bg='green').pack(pady=5)

        ttk.Button(
            marco_centro,
            text='Jugar',
            command=self.mostrar_juego
        ).pack(pady=5)
        ttk.Button(
            marco_centro,
            text='Reiniciar',
            command=self.mostrar_juego
        ).pack(pady=5)
        ttk.Button(
            marco_centro,
            text='Salir',
            command=self.raiz.destroy
        ).pack(pady=5)

    def mostrar_juego(self):
        self.limpiar_ventana()
        self.dealer_hand = []
        self.user_hand = []

        self.marco_juego_mesa = tk.Frame(self.raiz, bg='green')
        self.marco_juego_mesa.pack(fill=tk.BOTH, expand=True)

        ruta_mesa = Path(__file__).parent / 'images' / 'bjtable.png'
        self.logo_mesa = tk.PhotoImage(file=str(ruta_mesa)).subsample(3, 3)
        ruta_cartas = Path(__file__).parent / 'images' / 'deckofcards.png'
        self.baraja_imagen = tk.PhotoImage(file=str(ruta_cartas))
        self.cartas_visibles = []
        self.animacion = 0

        # La imagen ocupa todo el marco como fondo.
        fondo = tk.Label(self.marco_juego_mesa, image=self.logo_mesa)
        fondo.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.estado = tk.StringVar()
        tk.Label(
            self.marco_juego_mesa,
            textvariable=self.estado,
            bg='green',
            fg='white',
            font=('Arial', 14, 'bold')
        ).place(relx=0.5, rely=0.15, anchor=tk.CENTER)

        self.saldo_texto = tk.StringVar(value=f'Saldo disponible: ${self.saldo}')
        tk.Label(
            self.marco_juego_mesa,
            textvariable=self.saldo_texto,
            bg='green',
            fg='white',
            font=('Arial', 12, 'bold')
        ).place(relx=0.5, rely=0.23, anchor=tk.CENTER)

        tk.Label(
            self.marco_juego_mesa,
            text='Apuesta:',
            bg='green',
            fg='white'
        ).place(relx=0.4, rely=0.65, anchor=tk.CENTER)
        self.entrada_apuesta = ttk.Entry(self.marco_juego_mesa, width=10)
        self.entrada_apuesta.place(relx=0.5, rely=0.65, anchor=tk.CENTER)
        self.boton_apostar = ttk.Button(
            self.marco_juego_mesa,
            text='Apostar y repartir',
            command=self.iniciar_partida
        )
        self.boton_apostar.place(relx=0.65, rely=0.65, anchor=tk.CENTER)

        self.mano_usuario = tk.Frame(
            self.marco_juego_mesa,
            bg='green',
        )
        self.mano_usuario.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.mano_dealer = tk.Frame(
            self.marco_juego_mesa,
            bg='green'
        )
        self.mano_dealer.place(relx=0.5, rely=0.32, anchor=tk.CENTER)

        self.boton_pedir = ttk.Button(
            self.marco_juego_mesa,
            text='Pedir carta',
            command=self.pedir_carta
        )
        self.boton_pedir.place(relx=0.4, rely=0.8, anchor=tk.CENTER)
        self.boton_pedir.config(state=tk.DISABLED)

        self.boton_quedarse = ttk.Button(
            self.marco_juego_mesa,
            text='Quedarse',
            command=self.quedarse
        )
        self.boton_quedarse.place(relx=0.6, rely=0.8, anchor=tk.CENTER)
        self.boton_quedarse.config(state=tk.DISABLED)

        self.boton_nueva_mano = ttk.Button(
            self.marco_juego_mesa,
            text='Nueva mano',
            command=self.mostrar_juego
        )
        self.boton_nueva_mano.place(relx=0.5, rely=0.86, anchor=tk.CENTER)
        self.boton_nueva_mano.config(state=tk.DISABLED)

        ttk.Button(
            self.marco_juego_mesa,
            text='Volver al menú',
            command=self.mostrar_menu
        ).place(relx=0.5, rely=0.94, anchor=tk.CENTER)

        self.actualizar_tablero()

    def iniciar_partida(self):
        try:
            apuesta = int(self.entrada_apuesta.get())
        except ValueError:
            self.estado.set('Introduce una apuesta válida.')
            return

        if apuesta <= 0:
            self.estado.set('La apuesta debe ser mayor que cero.')
            return
        if apuesta > self.saldo:
            self.estado.set('No tienes saldo suficiente para esa apuesta.')
            return

        self.apuesta = apuesta
        self.saldo -= apuesta
        self.saldo_texto.set(f'Saldo disponible: ${self.saldo}')
        self.dealer_hand = [repartir_carta(), repartir_carta()]
        self.user_hand = [repartir_carta(), repartir_carta()]
        self.entrada_apuesta.config(state=tk.DISABLED)
        self.boton_apostar.config(state=tk.DISABLED)
        self.boton_pedir.config(state=tk.NORMAL)
        self.boton_quedarse.config(state=tk.NORMAL)
        self.boton_nueva_mano.config(state=tk.DISABLED)
        self.actualizar_tablero()

    def actualizar_tablero(self):
        puntos_usuario = calcular_puntos(self.user_hand)
        puntos_dealer = calcular_puntos(self.dealer_hand)
        self.estado.set(
            f'Tu puntuación: {puntos_usuario} | Dealer: {puntos_dealer}'
        )
        self.animacion += 1
        self.cartas_visibles = []
        self.mostrar_cartas(self.mano_usuario, self.user_hand)
        self.mostrar_cartas(self.mano_dealer, self.dealer_hand)

    def mostrar_cartas(self, marco, mano):
        for widget in marco.winfo_children():
            widget.destroy()

        if not mano:
            marco.configure(width=1, height=1)
            return

        ancho = self.baraja_imagen.width() // 13
        alto = self.baraja_imagen.height() // 4
        separacion = 6
        marco.configure(
            width=ancho * len(mano) + separacion * (len(mano) - 1),
            height=alto
        )
        marco.pack_propagate(False)

        animacion = self.animacion
        for indice, carta in enumerate(mano):
            imagen = self.recortar_carta(carta)
            self.cartas_visibles.append(imagen)
            etiqueta = tk.Label(marco, image=imagen, bg='green')
            posicion_x = indice * (ancho + separacion)
            etiqueta.place(x=posicion_x, y=-alto)
            self.animar_carta(
                etiqueta,
                posicion_x,
                -alto,
                0,
                animacion
            )

    def animar_carta(self, etiqueta, posicion_x, posicion_y, destino, animacion):
        if animacion != self.animacion or not etiqueta.winfo_exists():
            return

        siguiente_y = min(posicion_y + 12, destino)
        etiqueta.place(x=posicion_x, y=siguiente_y)
        if siguiente_y < destino:
            self.raiz.after(
                15,
                self.animar_carta,
                etiqueta,
                posicion_x,
                siguiente_y,
                destino,
                animacion
            )

    def recortar_carta(self, carta):
        rangos = ['A'] + list(range(2, 11)) + ['J', 'Q', 'K']
        filas = {
            'Treboles': 0,
            'Corazones': 1,
            'Diamantes': 2,
            'Picas': 3,
        }
        columna = rangos.index(carta[0])
        fila = filas[carta[1]]
        ancho = self.baraja_imagen.width() // 13
        alto = self.baraja_imagen.height() // 4

        imagen = tk.PhotoImage(width=ancho, height=alto)
        self.raiz.tk.call(
            str(imagen),
            'copy',
            str(self.baraja_imagen),
            '-from',
            columna * ancho,
            fila * alto,
            (columna + 1) * ancho,
            (fila + 1) * alto,
            '-to',
            0,
            0
        )
        return imagen

    def pedir_carta(self):
        self.user_hand.append(repartir_carta())
        self.actualizar_tablero()

        if calcular_puntos(self.user_hand) > 21:
            self.estado.set('Te pasaste de 21. Has perdido.')
            self.finalizar_partida()
            self.boton_pedir.config(state=tk.DISABLED)
            self.boton_quedarse.config(state=tk.DISABLED)

    def quedarse(self):
        while calcular_puntos(self.dealer_hand) < 17:
            self.dealer_hand.append(repartir_carta())

        puntos_usuario = calcular_puntos(self.user_hand)
        puntos_dealer = calcular_puntos(self.dealer_hand)
        self.actualizar_tablero()

        if puntos_dealer > 21 or puntos_usuario > puntos_dealer:
            resultado = 'Has ganado.'
            self.saldo += self.apuesta * 2
        elif puntos_usuario == puntos_dealer:
            resultado = 'Empate.'
            self.saldo += self.apuesta
        else:
            resultado = 'El dealer gana.'

        self.estado.set(
            f'{resultado} Tú: {puntos_usuario} | Dealer: {puntos_dealer}'
        )
        self.saldo_texto.set(f'Saldo disponible: ${self.saldo}')
        self.finalizar_partida()

    def finalizar_partida(self):
        self.saldo_texto.set(f'Saldo disponible: ${self.saldo}')
        self.boton_pedir.config(state=tk.DISABLED)
        self.boton_quedarse.config(state=tk.DISABLED)
        self.boton_nueva_mano.config(state=tk.NORMAL)


def main():
    Aplicacion()
    return 0


if __name__ == '__main__':
    main()

import tkinter as tk
from tkinter import ttk
from pathlib import Path
from blackjack import calcular_puntos, repartir_carta


class Aplicacion:
    def __init__(self):
        self.saldo = 500
        self.apuesta = 0
        self.opciones = {
            'sonido': True,
            'pantalla_completa': False,
        }
        self.raiz = tk.Tk()
        self.raiz.geometry('700x500')
        self.raiz.attributes('-fullscreen', True)
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
        tk.Label(marco_centro, image=self.logo, bg='green').pack(pady=10)

        tk.Label(
            marco_centro,
            text='BLACKJACK',
            bg='green',
            fg='white',
            font=('Arial', 20, 'bold')
        ).pack(pady=(0, 15))

        ttk.Button(
            marco_centro,
            text='Jugar',
            width=18,
            command=self.mostrar_juego
        ).pack(pady=6)
        ttk.Button(
            marco_centro,
            text='Opciones',
            width=18,
            command=self.mostrar_opciones
        ).pack(pady=6)
        ttk.Button(
            marco_centro,
            text='Salir',
            width=18,
            command=self.raiz.destroy
        ).pack(pady=6)

    def mostrar_opciones(self):
        self.limpiar_ventana()

        marco = tk.Frame(self.raiz, bg='green')
        marco.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        tk.Label(
            marco,
            text='Opciones',
            bg='green',
            fg='white',
            font=('Arial', 18, 'bold')
        ).pack(pady=(0, 20))

        self.var_sonido = tk.BooleanVar(value=self.opciones['sonido'])
        self.var_pantalla_completa = tk.BooleanVar(
            value=self.opciones['pantalla_completa']
        )

        tk.Checkbutton(
            marco,
            text='Sonido activado',
            variable=self.var_sonido,
            bg='green',
            fg='white',
            activebackground='green',
            selectcolor='darkgreen',
            command=self.aplicar_opciones
        ).pack(pady=6, anchor='w')

        tk.Checkbutton(
            marco,
            text='Pantalla completa',
            variable=self.var_pantalla_completa,
            bg='green',
            fg='white',
            activebackground='green',
            selectcolor='darkgreen',
            command=self.aplicar_opciones
        ).pack(pady=6, anchor='w')

        ttk.Button(
            marco,
            text='Volver al menú',
            width=18,
            command=self.mostrar_menu
        ).pack(pady=16)

    def aplicar_opciones(self):
        self.opciones['sonido'] = self.var_sonido.get()
        self.opciones['pantalla_completa'] = self.var_pantalla_completa.get()

        if self.opciones['pantalla_completa']:
            self.raiz.attributes('-fullscreen', True)
        else:
            self.raiz.attributes('-fullscreen', False)
            self.raiz.geometry('700x500')

    def mostrar_juego(self):
        self.limpiar_ventana()
        self.dealer_hand = []
        self.user_hand = []
        self.dealer_revelado = False

        self.marco_juego_mesa = tk.Frame(self.raiz, bg='green')
        self.marco_juego_mesa.pack(fill=tk.BOTH, expand=True)

        ruta_mesa = Path(__file__).parent / 'images' / 'bjtable.png'
        self.logo_mesa = tk.PhotoImage(file=str(ruta_mesa)).subsample(3, 3)
        ruta_cartas = Path(__file__).parent / 'images' / 'deckofcards.png'
        self.baraja_imagen = tk.PhotoImage(file=str(ruta_cartas))
        self.cartas_visibles = []
        self.animacion = 0

        fondo = tk.Label(self.marco_juego_mesa, image=self.logo_mesa)
        fondo.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.estado = tk.StringVar(value='Haz tu apuesta para empezar.')
        tk.Label(
            self.marco_juego_mesa,
            textvariable=self.estado,
            bg='green',
            fg='white',
            font=('Arial', 14, 'bold')
        ).place(relx=0.5, rely=0.12, anchor=tk.CENTER)

        self.saldo_texto = tk.StringVar(value=f'Saldo disponible: ${self.saldo}')
        tk.Label(
            self.marco_juego_mesa,
            textvariable=self.saldo_texto,
            bg='green',
            fg='white',
            font=('Arial', 12, 'bold')
        ).place(relx=0.5, rely=0.2, anchor=tk.CENTER)

        self.mano_dealer = tk.Frame(self.marco_juego_mesa, bg='green')
        self.mano_dealer.place(relx=0.5, rely=0.34, anchor=tk.CENTER)

        self.mano_usuario = tk.Frame(self.marco_juego_mesa, bg='green')
        self.mano_usuario.place(relx=0.5, rely=0.58, anchor=tk.CENTER)

        self.panel_apuesta = tk.Frame(self.marco_juego_mesa, bg='green')
        self.panel_apuesta.place(relx=0.5, rely=0.75, anchor=tk.CENTER)

        tk.Label(
            self.panel_apuesta,
            text='Apuesta:',
            bg='green',
            fg='white',
            font=('Arial', 11, 'bold')
        ).grid(row=0, column=0, padx=(0, 8), pady=4)

        self.entrada_apuesta = ttk.Entry(self.panel_apuesta, width=10)
        self.entrada_apuesta.grid(row=0, column=1, padx=8, pady=4)

        self.boton_apostar = ttk.Button(
            self.panel_apuesta,
            text='Apostar',
            command=self.iniciar_partida
        )
        self.boton_apostar.grid(row=0, column=2, padx=8, pady=4)

        self.controles = tk.Frame(self.marco_juego_mesa, bg='green')
        self.controles.place(relx=0.5, rely=0.87, anchor=tk.CENTER)

        self.boton_pedir = ttk.Button(
            self.controles,
            text='Pedir',
            command=self.pedir_carta
        )
        self.boton_pedir.grid(row=0, column=0, padx=8, pady=6)
        self.boton_pedir.config(state=tk.DISABLED)

        self.boton_quedarse = ttk.Button(
            self.controles,
            text='Quedarse',
            command=self.quedarse
        )
        self.boton_quedarse.grid(row=0, column=1, padx=8, pady=6)
        self.boton_quedarse.config(state=tk.DISABLED)

        self.boton_doblar = ttk.Button(
            self.controles,
            text='Doblar',
            command=self.doblar
        )
        self.boton_doblar.grid(row=0, column=2, padx=8, pady=6)
        self.boton_doblar.config(state=tk.DISABLED)

        ttk.Button(
            self.marco_juego_mesa,
            text='Volver al menú',
            command=self.mostrar_menu
        ).place(relx=0.5, rely=0.96, anchor=tk.CENTER)

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

        self.dealer_hand = [repartir_carta()]
        self.user_hand = [repartir_carta()]
        self.dealer_hand.append(repartir_carta())
        self.user_hand.append(repartir_carta())
        self.dealer_revelado = False

        self.entrada_apuesta.config(state=tk.DISABLED)
        self.boton_apostar.config(state=tk.DISABLED)
        self.boton_pedir.config(state=tk.NORMAL)
        self.boton_quedarse.config(state=tk.NORMAL)
        self.boton_doblar.config(state=tk.NORMAL)
        self.actualizar_tablero()

    def actualizar_tablero(self):
        puntos_usuario = calcular_puntos(self.user_hand)
        if not self.dealer_revelado and len(self.dealer_hand) > 1:
            puntos_dealer = calcular_puntos(self.dealer_hand[:1])
        else:
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
        total_cartas = len(mano)
        if marco is self.mano_dealer and not self.dealer_revelado and len(mano) > 1:
            total_cartas = len(mano)
        marco.configure(
            width=ancho * total_cartas + separacion * (total_cartas - 1),
            height=alto
        )
        marco.pack_propagate(False)

        animacion = self.animacion
        for indice, carta in enumerate(mano):
            if marco is self.mano_dealer and not self.dealer_revelado and indice == 1:
                etiqueta = tk.Label(
                    marco,
                    text='?',
                    bg='darkgreen',
                    fg='white',
                    font=('Arial', 11, 'bold'),
                    width=6,
                    height=3,
                    relief='solid',
                    borderwidth=2
                )
                posicion_x = indice * (ancho + separacion)
                etiqueta.place(x=posicion_x, y=0)
                continue

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
        self.dealer_revelado = True
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

    def doblar(self):
        if len(self.user_hand) != 2:
            self.estado.set('Solo puedes doblar con dos cartas.')
            return
        if self.saldo < self.apuesta:
            self.estado.set('No tienes saldo suficiente para doblar.')
            return

        self.saldo -= self.apuesta
        self.apuesta *= 2
        self.saldo_texto.set(f'Saldo disponible: ${self.saldo}')
        self.user_hand.append(repartir_carta())
        self.actualizar_tablero()

        if calcular_puntos(self.user_hand) > 21:
            self.estado.set('Te pasaste de 21 con el doble. Has perdido.')
            self.finalizar_partida()
            return

        self.quedarse()

    def finalizar_partida(self):
        self.saldo_texto.set(f'Saldo disponible: ${self.saldo}')
        self.boton_pedir.config(state=tk.DISABLED)
        self.boton_quedarse.config(state=tk.DISABLED)
        self.boton_doblar.config(state=tk.DISABLED)
        self.entrada_apuesta.config(state=tk.NORMAL)
        self.boton_apostar.config(state=tk.NORMAL)


def main():
    Aplicacion()
    return 0


if __name__ == '__main__':
    main()

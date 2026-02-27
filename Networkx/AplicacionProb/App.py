import networkx as nx
import matplotlib.pyplot as plt


def crear_arbol_monedas(num_lanzamientos):
    """
    Crea un árbol de probabilidades para lanzamientos de moneda usando DiGraph de NetworkX.
    Cada nodo almacena su probabilidad y nivel como atributos.
    """
    # Crear grafo dirigido (DiGraph) - representa flujo de probabilidad
    G = nx.DiGraph()

    def generar_nodos(nivel, resultado_actual, probabilidad_actual):
        """Función recursiva que genera todos los caminos posibles"""
        if nivel == num_lanzamientos:
            return

        # Rama: Cara
        nuevo_resultado_cara = resultado_actual + "C"
        nueva_prob_cara = probabilidad_actual * 0.5
        # add_node: agregar nodo con atributos personalizados
        G.add_node(nuevo_resultado_cara, prob=nueva_prob_cara, nivel=nivel + 1)
        # add_edge: crear arista dirigida con etiqueta
        G.add_edge(resultado_actual, nuevo_resultado_cara, label="C (0.5)")
        generar_nodos(nivel + 1, nuevo_resultado_cara, nueva_prob_cara)

        # Rama: Sello
        nuevo_resultado_sello = resultado_actual + "S"
        nueva_prob_sello = probabilidad_actual * 0.5
        G.add_node(nuevo_resultado_sello, prob=nueva_prob_sello, nivel=nivel + 1)
        G.add_edge(resultado_actual, nuevo_resultado_sello, label="S (0.5)")
        generar_nodos(nivel + 1, nuevo_resultado_sello, nueva_prob_sello)

    # Nodo raíz inicial
    G.add_node("Inicio", prob=1.0, nivel=0)
    generar_nodos(0, "Inicio", 1.0)

    return G


def crear_arbol_dado():
    """
    Crea árbol completo para dos lanzamientos de dado.
    Demuestra grafo con más ramificaciones (6 opciones por nivel).
    """
    G = nx.DiGraph()
    G.add_node("Inicio", prob=1.0, nivel=0)

    # Primer lanzamiento: 6 ramas
    for i in range(1, 7):
        nodo1 = f"{i}"
        G.add_node(nodo1, prob=1 / 6, nivel=1)
        G.add_edge("Inicio", nodo1, label=f"{i} (1/6)")

        # Segundo lanzamiento: 6 ramas más por cada resultado del primero
        for j in range(1, 7):
            nodo2 = f"{i},{j}"
            prob_final = (1 / 6) * (1 / 6)  # Probabilidad compuesta
            G.add_node(nodo2, prob=prob_final, nivel=2, suma=i + j)  # Atributo extra: suma
            G.add_edge(nodo1, nodo2, label=f"{j} (1/6)")

    return G


def visualizar_arbol(G, titulo, nombre_archivo):
    """
    Visualiza el árbol usando múltiples funciones de NetworkX:
    - Posicionamiento manual por niveles
    - Coloreo condicional de nodos
    - Dibujo de nodos, aristas y etiquetas por separado
    """
    plt.figure(figsize=(16, 10))

    # Crear layout manual jerárquico (organizar por niveles)
    pos = {}
    niveles = {}

    # Agrupar nodos por nivel usando el atributo 'nivel'
    for node in G.nodes():
        nivel = G.nodes[node]['nivel']
        if nivel not in niveles:
            niveles[nivel] = []
        niveles[nivel].append(node)

    # Posicionar nodos espaciados horizontalmente por nivel
    for nivel, nodos in niveles.items():
        num_nodos = len(nodos)
        for i, nodo in enumerate(nodos):
            x = (i - num_nodos / 2) * 1.5  # Espaciado horizontal
            y = -nivel * 2.5  # Espaciado vertical (niveles hacia abajo)
            pos[nodo] = (x, y)

    # Colorear nodos según su posición en el árbol
    node_colors = []
    for node in G.nodes():
        if node == "Inicio":
            node_colors.append('lightgreen')  # Raíz: verde
        elif G.out_degree(node) == 0:  # out_degree: nodos sin hijos (hojas)
            node_colors.append('lightcoral')  # Hojas: rojo
        else:
            node_colors.append('lightblue')  # Intermedios: azul

    # Tamaños de nodos basados en probabilidad (atributo personalizado)
    node_sizes = [G.nodes[node]['prob'] * 2000 + 500 for node in G.nodes()]

    # draw_networkx_nodes: dibujar solo los nodos
    nx.draw_networkx_nodes(G, pos, node_color=node_colors,
                           node_size=node_sizes, alpha=0.9, edgecolors='black', linewidths=1.5)

    # draw_networkx_edges: dibujar solo las aristas con flechas
    nx.draw_networkx_edges(G, pos, edge_color='gray',
                           arrows=True, arrowsize=20,
                           width=2, alpha=0.7, arrowstyle='->')

    # Crear etiquetas que muestren resultado y probabilidad
    labels = {}
    for node in G.nodes():
        if node == "Inicio":
            labels[node] = "Inicio\nP=1.0"
        else:
            prob = G.nodes[node]['prob']
            resultado = node.replace("Inicio", "")
            labels[node] = f"{resultado}\nP={prob:.4f}"

    # draw_networkx_labels: agregar etiquetas de texto a los nodos
    nx.draw_networkx_labels(G, pos, labels, font_size=7, font_weight='bold')

    # get_edge_attributes: extraer atributos de aristas para etiquetarlas
    edge_labels = nx.get_edge_attributes(G, 'label')
    # draw_networkx_edge_labels: mostrar etiquetas en las aristas
    nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=6, font_color='darkblue')

    plt.title(titulo, fontsize=18, fontweight='bold', pad=25)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(nombre_archivo, dpi=200, bbox_inches='tight', facecolor='white')
    print(f"✓ Gráfico guardado: {nombre_archivo}")
    plt.show()


def analizar_grafo(G, tipo):
    """
    Usa funciones de análisis de NetworkX para obtener información del grafo.
    """
    print("\n🔍 ANÁLISIS DEL GRAFO:")

    # number_of_nodes: contar nodos totales
    print(f"  • Nodos totales: {G.number_of_nodes()}")

    # number_of_edges: contar aristas totales
    print(f"  • Aristas totales: {G.number_of_edges()}")

    # Nodos hoja (sin descendientes): out_degree == 0
    hojas = [n for n in G.nodes() if G.out_degree(n) == 0]
    print(f"  • Nodos hoja (resultados finales): {len(hojas)}")


    # Altura del árbol (camino más largo desde raíz)
    if nx.is_directed_acyclic_graph(G):
        # dag_longest_path_length: longitud del camino más largo en DAG
        altura = nx.dag_longest_path_length(G)
        print(f"  • Altura del árbol: {altura}")

    if tipo == "dado":
        # Análisis específico para dados: contar por suma
        print("\n DISTRIBUCIÓN DE SUMAS:")
        sumas = {}
        for node in hojas:
            suma = G.nodes[node].get('suma', 0)
            if suma not in sumas:
                sumas[suma] = 0
            sumas[suma] += 1

        for suma in sorted(sumas.keys()):
            prob = sumas[suma] / len(hojas)
            print(f"  • Suma = {suma}: {sumas[suma]} formas, P = {prob:.4f}")


# --------------
# MENÚ PRINCIPAL
# --------------
print("=" * 70)
print("  ÁRBOLES DE PROBABILIDAD - NetworkX Demo")
print("=" * 70)
print("\n1. Lanzamiento de 2 monedas")
print("2. Lanzamiento de 3 monedas")
print("3. Lanzamiento de 2 dados")
print("\n0. Salir")
print("=" * 70)

opcion = input("\nElige una opción (0-3): ")
2
if opcion == "1":
    print("\n Generando árbol de 2 monedas...")
    G = crear_arbol_monedas(2)
    visualizar_arbol(G, "Árbol de Probabilidad - 2 Lanzamientos de Moneda",
                     "arbol_2_monedas.png")
    analizar_grafo(G, "moneda")

    print("\n ESPACIO MUESTRAL:")
    hojas = [n for n in G.nodes() if G.out_degree(n) == 0]
    print(f"  Ω = {{{', '.join([h.replace('Inicio', '') for h in hojas])}}}")
    print(f"  |Ω| = {len(hojas)} resultados ")

elif opcion == "2":
    print("\n Generando árbol de 3 monedas...")
    G = crear_arbol_monedas(3)
    visualizar_arbol(G, "Árbol de Probabilidad - 3 Lanzamientos de Moneda",
                     "arbol_3_monedas.png")
    analizar_grafo(G, "moneda")

    print("\n DISTRIBUCIÓN DE CARAS:")
    hojas = [n for n in G.nodes() if G.out_degree(n) == 0]
    for num_caras in range(4):
        resultados = [h for h in hojas if h.count('C') == num_caras]
        prob = len(resultados) / len(hojas)
        print(f"  • {num_caras} cara(s): {len(resultados)}/8 = {prob:.3f}")

elif opcion == "3":
    print("\n Generando árbol de 2 dados ")
    G = crear_arbol_dado()
    visualizar_arbol(G, "Árbol de Probabilidad - 2 Lanzamientos de Dado ",
                     "arbol_dados_completo.png")
    analizar_grafo(G, "dado")

    print("\n🎲 PROBABILIDADES NOTABLES:")
    print(f"  • P(suma = 7): 6/36 = 0.1667 (máximo)")
    print(f"  • P(suma = 2 o 12): 1/36 cada uno = 0.0278 (mínimo)")
    print(f"  • P(suma par): 18/36 = 0.5000")

elif opcion == "0":
    print("\n¡Hasta luego!")

else:
    print("\n Opción no válida")

print("\n" + "=" * 70)


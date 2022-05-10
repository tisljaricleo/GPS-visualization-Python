from traceback import print_tb
import matplotlib.pyplot as plt
from grafo import Graph
from haversine import haversine
import re


g = Graph()
control_click = []

def get_cost(x1, x2):
  x1 = g.get_vertex(x1)
  x2 = g.get_vertex(x2)
  return haversine([x1.latitude, x1.longitude], [x2.latitude, x2.longitude])

with open("map.osm.txt") as fp: #le o arquivo e adiciona ao grafo
    for line in fp:
      points = re.findall(r'[-+]?\d+.\d+', line)
      g.add_vertex(points[0], float(points[1]), float(points[2]))
    
with open("uesb.adjlist") as file: #adiciona as ligações ao grafo
  for line in file:
    points = re.findall(r'[-+]?\d+', line)
    for index in range(len(points) - 1):
      g.add_edge(points[0], points[index+1], get_cost(points[0], points[index+1]))


def connectpoints(x1, x2):
  v1 = g.get_vertex(x1)
  v2 = g.get_vertex(x2)

  plt.plot([v1.latitude, v2.latitude], [v1.longitude, v2.longitude], 'k-')

def get_caminho(x1, x2):
  dist, caminho = g.min_path(x1, x2)

  if caminho == None:
    print("Não existe um caminho.")
    return False

  for index, vertex in enumerate(caminho):
    if len(caminho) > index+1:
      connectpoints(vertex, caminho[index+1])


def mouse_event(event):

  print('x: {} and y: {}'.format(event.xdata, event.ydata))

  if event.xdata == None or event.ydata == None:
    print("Pontos clicados são invalidos")
    return None


  vertex_com_ligacoes = g.get_edges()
  vert = g.get_vertex(vertex_com_ligacoes[0][0])
  menor_distancia = [haversine([event.xdata, event.ydata], [vert.latitude, vert.longitude]), vert]

  for item in vertex_com_ligacoes[1:]:
    vert = g.get_vertex(item[0])

    distancia = haversine([event.xdata, event.ydata], [vert.latitude, vert.longitude])

    if distancia < menor_distancia[0]:
      menor_distancia = [distancia, vert]

  control_click.append(menor_distancia[1].id)

  if len(control_click) == 2:
    plt.clf()
    plot()
    get_caminho(control_click[0], control_click[1])
    plt.draw()
    del control_click[:]


fig = plt.figure()
cid = fig.canvas.mpl_connect('button_press_event', mouse_event)


def plot():
  x = list()
  y = list()
  for elemento in g.get_edges():
    elemento = g.get_vertex(elemento[0])
    x.append(elemento.latitude)
    y.append(elemento.longitude)

  plt.plot(x, y, 'ro')


plot()
plt.show()

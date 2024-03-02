def createExCurve(xMin, xMax, yMin, yMax, base):
  a = (yMax - yMin) / (base ** xMax - base ** xMin)
  c = yMax - a * base ** xMax
  return lambda x: a * base ** x + c

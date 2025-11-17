import numpy as np

def interpolate_points(points, Metodo="Polinomio"):
    if len(points) < 2:
        return points
    
    interpolated = []
    
    if Metodo == "Polinomio":
        # Extraer coordenadas
        x_points = [p[0] for p in points]
        y_points = [p[1] for p in points]
        
        # Construir matriz de Vandermonde
        V = np.vander(x_points, increasing=True)
        
        # Resolver sistema lineal para coeficientes del polinomio
        coeffs = np.linalg.solve(V, y_points)
        
        # Generar valores interpolados
        x_new = np.linspace(min(x_points), max(x_points), num=200)
        y_new = np.polyval(coeffs[::-1], x_new)  # invertir porque usamos increasing=True
        interpolated = list(zip(x_new, y_new))
    
    elif Metodo == "Bezier":
        # Interpolación cuadrática Bézier entre segmentos
        for i in range(len(points) - 1):
            x1, y1 = points[i]
            x2, y2 = points[i + 1]
            
            # Punto de control
            cx = (x1 + x2) / 2
            cy = (y1 + y2) / 2
            
            if i < len(points) - 2:
                x3, y3 = points[i + 2]
                cx += (y2 - y3) * 0.2
                cy += (x3 - x2) * 0.2
            
            # Generar puntos intermedios
            for t in np.linspace(0, 1, num=20):
                xt = (1-t)**2 * x1 + 2*(1-t)*t*cx + t**2*x2
                yt = (1-t)**2 * y1 + 2*(1-t)*t*cy + t**2*y2
                interpolated.append((xt, yt))
    
    return interpolated
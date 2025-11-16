import numpy as np

def interpolate_points(points):
    if len(points) < 2:
        return points
    
    # Crear una lista para los puntos interpolados
    interpolated = []
    
    # Interpolación cuadrática entre puntos
    for i in range(len(points) - 1):
        x1, y1 = points[i]
        x2, y2 = points[i + 1]
        
        # Punto de control en el medio con un poco de curvatura
        cx = (x1 + x2) / 2 
        cy = (y1 + y2) / 2
        
        # Ajustar la curvatura basada en la posición relativa
        if i < len(points) - 2:
            x3, y3 = points[i + 2]
            cx += (y2 - y3) * 0.2
            cy += (x3 - x2) * 0.2
        
        # Generar puntos intermedios usando curva cuadrática de Bézier
        for t in np.linspace(0, 1, num=20):
            xt = (1-t)**2 * x1 + 2*(1-t)*t*cx + t**2*x2
            yt = (1-t)**2 * y1 + 2*(1-t)*t*cy + t**2*y2
            interpolated.append((xt, yt))
    
    return interpolated

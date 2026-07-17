import pygame
import math
import sys
import os
import time
import threading
import winsound
import webbrowser
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# =====================================================================
# CONFIGURACIÓN ÓPTICA DEL SATÉLITE DE ALTA PRECISIÓN (AETHERON EYE-2)
# =====================================================================
SISTEMA_OPTICO = {
    "modo_enfoque": False,
    "coordenadas_objetivo": (-5.1944, -80.6328),  
    "desviacion_mira_metros": 850.0,             
    "resolucion_pixel_cm": 50.0,                 
    "distancia_focal_mm": 1200,                  
    "mapa_automatico": False
}

def consola_operaciones_mira():
    print("\n" + "="*65)
    print(" AETHERON STARK INDUSTRIES - OPTICAL PRECISION CORE V2")
    print("="*65)
    print("SISTEMA: Control de Lentes de Silicio y Actuadores de Torque")
    print("-"*65)
    print("\n[JARVIS] Óptica estabilizada en órbita LEO. Esperando comando...")
    
    while True:
        entrada = input("AETHERON_OPTICS_CMD> ").strip().lower()
        if entrada == "rastrearlo":
            if not SISTEMA_OPTICO["modo_enfoque"]:
                print("\n🧠 [JARVIS] Comando recibido. Activando motores de enfoque óptico...")
                winsound.Beep(2100, 150)
                SISTEMA_OPTICO["modo_enfoque"] = True
                break
            else:
                print("[SISTEMA] El zoom de alta precisión ya está activo.")
        else:
            print("[ERROR] Comando denegado. Digita 'rastrearlo' para enfocar la mira telescópica.")

def dibujar_red_tierra(radio, lineas):
    glLineWidth(1); glColor3f(0.1, 0.6, 0.9)  
    for i in range(lineas):
        lat = math.pi * (-0.5 + float(i) / lineas)
        sin_lat, cos_lat = math.sin(lat), math.cos(lat)
        glBegin(GL_LINE_LOOP)
        for j in range(lineas):
            lon = 2 * math.pi * float(j) / lineas
            glVertex3f(math.cos(lon)*cos_lat*radio, math.sin(lon)*cos_lat*radio, sin_lat*radio)
        glEnd()

def dibujar_reticula_mira_militar():
    glMatrixMode(GL_PROJECTION); glPushMatrix(); glLoadIdentity(); gluOrtho2D(-10, 10, -10, 10)
    glMatrixMode(GL_MODELVIEW); glPushMatrix(); glLoadIdentity()
    glLineWidth(2); glColor3f(1.0, 0.1, 0.1) 
    
    # Retícula en cruz
    glBegin(GL_LINES)
    glVertex2f(-2.0, 0); glVertex2f(-0.4, 0); glVertex2f(0.4, 0); glVertex2f(2.0, 0)
    glVertex2f(0, -2.0); glVertex2f(0, -0.4); glVertex2f(0, 0.4); glVertex2f(0, 2.0)
    glEnd()
    
    # Cuadrante interno de precisión submétrica
    glBegin(GL_LINE_LOOP); glVertex2f(-0.6, -0.6); glVertex2f(0.6, -0.6); glVertex2f(0.6, 0.6); glVertex2f(-0.6, 0.6); glEnd()
    glMatrixMode(GL_PROJECTION); glPopMatrix(); glMatrixMode(GL_MODELVIEW); glPopMatrix()

def arrancar_visualizador_3d():
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()
    W, H = 800, 600
    pantalla = pygame.display.set_mode((W, H), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("AETHERON EYE-2 - HIGH PRECISION OPTICAL MONITOR")
    
    glMatrixMode(GL_PROJECTION); gluPerspective(45, (W/H), 0.1, 200.0)
    glMatrixMode(GL_MODELVIEW); glEnable(GL_DEPTH_TEST)
    
    distancia_camara = 60.0
    angulo_rotacion = 0.0
    reloj = pygame.time.Clock()
    
    threading.Thread(target=consola_operaciones_mira, daemon=True).start()
    
    while True:
        dt = reloj.tick(60) / 1000.0 
        for event in pygame.event.get():
            if event.type == QUIT: pygame.quit(); sys.exit()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT); glLoadIdentity()
        
        # --- MOTOR ÓPTICO DE ALTA VELOCIDAD  ---
        if SISTEMA_OPTICO["modo_enfoque"]:
            if distancia_camara > 14.5: 
                distancia_camara -= 4.5 * dt
            
            # La aberración atmosférica se corrige reduciendo la desviación a 0 metros
            if SISTEMA_OPTICO["desviacion_mira_metros"] > 0.00:
                SISTEMA_OPTICO["desviacion_mira_metros"] -= 85.0 * dt
            else:
                SISTEMA_OPTICO["desviacion_mira_metros"] = 0.00
                
            # Los lentes se ajustan hasta lograr una resolución de 1 cm por píxel (Mil veces superior)
            if SISTEMA_OPTICO["resolucion_pixel_cm"] > 1.0:
                SISTEMA_OPTICO["resolucion_pixel_cm"] -= 4.9 * dt
            else:
                SISTEMA_OPTICO["resolucion_pixel_cm"] = 1.0
                
            # Extensión de la distancia focal por servomotores
            if SISTEMA_OPTICO["distancia_focal_mm"] < 8000:
                SISTEMA_OPTICO["distancia_focal_mm"] += 680 * int(dt * 10)
        else:
            angulo_rotacion += 20.0 * dt 
            
        gluLookAt(0, 0, distancia_camara, 0, 0, 0, 0, 1, 0)
        
        glPushMatrix(); glRotatef(23.5, 1, 0, 0); glRotatef(angulo_rotacion, 0, 1, 0)
        dibujar_red_tierra(12.0, 24); glPopMatrix()
        
        dibujar_reticula_mira_militar()
        
        # Telemetría Óptica limpia en la Terminal
        os.system('cls' if os.name == 'nt' else 'clear')
        print("==============================================================")
        print("    AETHERON EYE-2 : MONITOR DE MIRA SATELITAL DE ALTA PRECISIÓN")
        print("==============================================================")
        print(f" Estatus Óptico       : {'🔒 TARGET LOCK (ENFOQUE CUÁNTICO)' if SISTEMA_OPTICO['modo_enfoque'] else '📡 BUSCANDO COORDENADAS TERRESTRES'}")
        print(f" Distancia Focal      : {SISTEMA_OPTICO['distancia_focal_mm']} mm")
        print(f" Altitud del Sensor   : {max(145.0, distancia_camara * 10):.1f} km")
        print("--------------------------------------------------------------")
        print(f" 🎯 COORDENADAS DEL OBJETIVO FIJADO:")
        print(f"   Desviación de Mira : {max(0.00, SISTEMA_OPTICO['desviacion_mira_metros']):.2f} metros")
        print(f"   Resolución Óptica  : {SISTEMA_OPTICO['resolucion_pixel_cm']:.1f} cm por píxel")
        print("==============================================================")
        
        # INTERCEPCIÓN EN EL SEGUNDO 10 (ERROR = 0)
        if SISTEMA_OPTICO["desviacion_mira_metros"] <= 0.00 and SISTEMA_OPTICO["resolucion_pixel_cm"] <= 1.0:
            lat, lon = SISTEMA_OPTICO["coordenadas_objetivo"]
            print("🎯 [MIRA FIJADA EN CERO METROS] Resolución centimétrica activa.")
            print(f"   Ubicación exacta consolidada: Lat: {lat}, Lon: {lon}")
            
            if not SISTEMA_OPTICO["mapa_automatico"]:
                SISTEMA_OPTICO["mapa_automatico"] = True
                url_final = f"https://google.com{lat},{lon}"
                winsound.Beep(2000, 80); winsound.Beep(2500, 300)
                webbrowser.open(url_final)
                
        elif SISTEMA_OPTICO["modo_enfoque"]:
            print("⚡ [ÓPTICA ADAPTATIVA] Corrigiendo refracción del aire en milisegundos...")
            
        pygame.display.flip()

if __name__ == "__main__":
    arrancar_visualizador_3d()

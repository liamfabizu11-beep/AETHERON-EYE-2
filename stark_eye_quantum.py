import pygame
import math
import sys
import os
import time
import threading
import winsound
import webbrowser
import random
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# =====================================================================
# MATRIZ CUÁNTICA DE RED 
# =====================================================================
SISTEMA_TACTICO = {
    "modo_rastreo": False,
    "tiempo_restante_segundos": 600.0,
    "coordenadas_target": (-5.1944, -80.6328),  
    "objetivos_secundarios": [
        {"nombre": "MOSCÚ (RU)", "coords": (55.7558, 37.6173), "error": 45.0},
        {"nombre": "CDMX (MX)", "coords": (19.4326, -99.1332), "error": 32.0},
        {"nombre": "PIURA (PE)", "coords": (-5.1944, -80.6328), "error": 35.0}
    ],
    "mapa_desplegado": False,
    "ancho_banda_gbps": 12.4
}

def formula_haversine(lat1, lon1, lat2, lon2):
    """Calcula la distancia real sobre la esfera terrestre (Matemática NASA)"""
    R = 6371.0 
    rad_lat1, rad_lon1 = math.radians(lat1), math.radians(lon1)
    rad_lat2, rad_lon2 = math.radians(lat2), math.radians(lon2)
    
    dlat = rad_lat2 - rad_lat1
    dlon = rad_lon2 - rad_lon1
    
    a = math.sin(dlat/2)**2 + math.cos(rad_lat1) * math.cos(rad_lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

def consola_entrada_comandos():
    print("\n" + "="*65)
    print(" AETHERON STARK INDUSTRIES - SYSTEM UPGRADE: QUANTUM EYE")
    print("="*65)
    print("PROTOCOLOS ACTIVOS: Haversine Navigation & Parallel Decryption")
    print("-"*65)
    print("\n[JARVIS] Conexión satelital multiplexada en línea...")
    
    while True:
        entrada = input("AETHERON_CORE_CMD> ").strip().lower()
        if entrada == "rastrearlo":
            if not SISTEMA_TACTICO["modo_rastreo"]:
                print("\n🧠 [JARVIS] Desplegando array de satélites. Forzando Overclocking de Red...")
                winsound.Beep(2200, 100); winsound.Beep(2200, 100)
                SISTEMA_TACTICO["modo_rastreo"] = True
                break
            else:
                print("[SISTEMA] Algoritmo cuántico ya se encuentra en ejecución.")
        else:
            print("[ERROR] Comando denegado. Digita 'rastrearlo' para iniciar la triangulación.")

def dibujar_red_tierra(radio, lineas):
    glLineWidth(1); glColor3f(0.0, 0.6, 1.0) 
    for i in range(lineas):
        lat = math.pi * (-0.5 + float(i) / lineas)
        sin_lat, cos_lat = math.sin(lat), math.cos(lat)
        glBegin(GL_LINE_LOOP)
        for j in range(lineas):
            lon = 2 * math.pi * float(j) / lineas
            glVertex3f(math.cos(lon)*cos_lat*radio, math.sin(lon)*cos_lat*radio, sin_lat*radio)
        glEnd()

def dibujar_reticula_punteria():
    glMatrixMode(GL_PROJECTION); glPushMatrix(); glLoadIdentity(); gluOrtho2D(-10, 10, -10, 10)
    glMatrixMode(GL_MODELVIEW); glPushMatrix(); glLoadIdentity()
    glLineWidth(2); glColor3f(1.0, 0.1, 0.1)
    glBegin(GL_LINES)
    glVertex2f(-2.0, 0); glVertex2f(-0.4, 0); glVertex2f(0.4, 0); glVertex2f(2.0, 0)
    glVertex2f(0, -2.0); glVertex2f(0, -0.4); glVertex2f(0, 0.4); glVertex2f(0, 2.0)
    glEnd()
  
    glBegin(GL_LINE_LOOP)
    for i in range(32):
        a = 2 * math.pi * i / 32
        glVertex2f(math.cos(a)*1.2, math.sin(a)*1.2)
    glEnd()
    glMatrixMode(GL_PROJECTION); glPopMatrix(); glMatrixMode(GL_MODELVIEW); glPopMatrix()

def arrancar_motor_grafico_3d():
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()
    W, H = 800, 600
    pantalla = pygame.display.set_mode((W, H), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("AETHERON STARK - QUANTUM EYE MAIN ENGINE")
    
    glMatrixMode(GL_PROJECTION); gluPerspective(45, (W/H), 0.1, 200.0)
    glMatrixMode(GL_MODELVIEW); glEnable(GL_DEPTH_TEST)
    
    distancia_camara = 60.0
    angulo_rotacion = 0.0
    reloj = pygame.time.Clock()
    
    threading.Thread(target=consola_entrada_comandos, daemon=True).start()
    
    while True:
        dt = reloj.tick(60) / 1000.0 
        for event in pygame.event.get():
            if event.type == QUIT: pygame.quit(); sys.exit()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT); glLoadIdentity()
        
        # --- MOTOR DE PROXIMIDAD CUÁNTICO  ---
        if SISTEMA_TACTICO["modo_rastreo"]:
            if distancia_camara > 14.5: 
                distancia_camara -= 4.5 * dt
            
            # Purgamos el margen de error de todos los objetivos en paralelo
            all_locked = True
            for obj in SISTEMA_TACTICO["objetivos_secundarios"]:
                if obj["error"] > 0.00:
                    obj["error"] -= 3.5 * dt
                    all_locked = False
                else:
                    obj["error"] = 0.00
            
            if SISTEMA_TACTICO["tiempo_restante_segundos"] > 0:
                SISTEMA_TACTICO["tiempo_restante_segundos"] -= dt
                
            # Simulación de incremento en la tasa de desencriptación 
            SISTEMA_TACTICO["ancho_banda_gbps"] += 15.5 * dt
        else:
            angulo_rotacion += 20.0 * dt
            
        gluLookAt(0, 0, distancia_camara, 0, 0, 0, 0, 1, 0)
        
        glPushMatrix(); glRotatef(23.5, 1, 0, 0); glRotatef(angulo_rotacion, 0, 1, 0)
        dibujar_red_tierra(12.0, 24); glPopMatrix()
        
        dibujar_reticula_punteria()
        
        # Consola del sistema
        total_segundos = max(0, int(SISTEMA_TACTICO["tiempo_restante_segundos"]))
        minutos, segundos = total_segundos // 60, total_segundos % 60
        
        os.system('cls' if os.name == 'nt' else 'clear')
        print("==============================================================")
        print("       STARK INDUSTRIES - INTERFAZ DE PROCESAMIENTO MUNDIAL   ")
        print("==============================================================")
        print(f" Canal de Criptografía: AES-256 | Flujo de Datos: {SISTEMA_TACTICO['ancho_banda_gbps']:.1f} Gbps")
        print(f" Temporizador Militar : {minutos:02d}:{segundos:02d} Mins")
        print("--------------------------------------------------------------")
        print("🛰️ ARRAY DE SEÑALES DETECTADAS (RASTREO EN PARALELO):")
        
        objetivos_completados = 0
        for obj in SISTEMA_TACTICO["objetivos_secundarios"]:
            status = f"🔒 LOCK (0.00m)" if obj["error"] <= 0.00 else f"📡 SCAN ({obj['error']:.2f} km)"
            print(f"   ▶ Target: {obj['nombre']:15} -> Estatus: {status}")
            if obj["error"] <= 0.00:
                objetivos_completados += 1
                
        print("==============================================================")
        
        # DISPARADOR AUTOMÁTICO AL REDUCIR EL ERROR DE LA RED
        if objetivos_completados == len(SISTEMA_TACTICO["objetivos_secundarios"]):
            lat, lon = SISTEMA_TACTICO["coordenadas_target"]
            print("🎯 [ALL TARGETS ACQUIRED] Triangulación global completada en 10s.")
            print("   Descargando algoritmo de Haversine esférico a la base de la NASA...")
            
            if not SISTEMA_TACTICO["mapa_desplegado"]:
                SISTEMA_TACTICO["mapa_desplegado"] = True
                url_final = f"https://google.com{lat},{lon}"
                winsound.Beep(2500, 100); winsound.Beep(2900, 300)
                webbrowser.open(url_final)
                
        elif SISTEMA_TACTICO["modo_rastreo"]:
            print("⚡ [OVERCLOCKING] Procesando coordenadas mediante matrices trigonométricas...")
            
        pygame.display.flip()

if __name__ == "__main__":
    arrancar_motor_grafico_3d()

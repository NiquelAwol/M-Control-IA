"""
iniciar_publico.py
Inicia automáticamente el servidor de IA en el puerto 8088, levanta el túnel de Cloudflare
y actualiza tunnel_config.json en GitHub para que el Link Maestro Fijo:
https://niquelawol.github.io/M-Control-IA/
conecte siempre al túnel activo de tu PC sin cambiar nunca de enlace.
"""

import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "cloudflared_live.log")
CONFIG_FILE = os.path.join(BASE_DIR, "tunnel_config.json")


def main():
    print("=" * 72)
    print("  M-CONTROL AI | ENLACE MAESTRO FIJO + TÚNEL AUTOMÁTICO")
    print("  Link Fijo Permanente: https://niquelawol.github.io/M-Control-IA/")
    print("=" * 72)

    # 1. Iniciar servidor Python de IA en segundo plano si no está activo
    print("\n[1/3] Iniciando servidor M-Control AI en http://127.0.0.1:8088 ...")
    subprocess.Popen(
        [sys.executable, "-m", "mcontrol_ai.api_service"],
        cwd=BASE_DIR,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    time.sleep(2)

    # 2. Iniciar Cloudflare Tunnel
    if os.path.exists(LOG_FILE):
        try:
            os.remove(LOG_FILE)
        except Exception:
            pass

    print("[2/3] Abriendo túnel seguro HTTP/2 con Cloudflare...")
    cf_exe = os.path.join(BASE_DIR, "cloudflared.exe")
    cf_proc = subprocess.Popen(
        [cf_exe, "tunnel", "--protocol", "http2", "--url", "http://127.0.0.1:8088", "--logfile", LOG_FILE],
        cwd=BASE_DIR,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    # Esperar a que aparezca la URL .trycloudflare.com en el log
    tunnel_url = None
    for _ in range(30):
        time.sleep(1)
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()
            m = re.search(r"https://[a-zA-Z0-9\-]+\.trycloudflare\.com", text)
            if m:
                tunnel_url = m.group(0)
                break

    if not tunnel_url:
        print("[ERROR] No se pudo obtener la URL de Cloudflare Tunnel.")
        return

    print(f"      -> Túnel interno activo: {tunnel_url}")

    # 3. Guardar en tunnel_config.json y sincronizar con GitHub
    print("[3/3] Sincronizando túnel con tu Link Maestro Fijo en GitHub...")
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "tunnel_url": tunnel_url,
            "updated_at": datetime.now().isoformat()
        }, f, indent=2)

    subprocess.run(["git", "add", "tunnel_config.json"], cwd=BASE_DIR, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["git", "commit", "-m", "chore(tunnel): actualizar endpoint activo para Link Maestro Fijo"], cwd=BASE_DIR, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["git", "push", "origin", "main"], cwd=BASE_DIR, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    print("\n" + "=" * 72)
    print("  ¡LISTO! TU PROYECTO ESTÁ AL AIRE CON LINK FIJO:")
    print("  👉 https://niquelawol.github.io/M-Control-IA/")
    print("  (Mantén esta ventana abierta mientras tus usuarios estén conectados)")
    print("=" * 72)

    try:
        cf_proc.wait()
    except KeyboardInterrupt:
        cf_proc.terminate()


if __name__ == "__main__":
    main()

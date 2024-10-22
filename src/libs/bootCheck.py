import os
import json
import subprocess

def exec_plugins(file_path):
    # Esegui script Python
    if file_path.endswith(".py"):
        subprocess.run(["python", file_path], check=True)
    # Esegui script shell
    elif file_path.endswith(".sh"):
        subprocess.run(["bash", file_path], check=True)
    # Esegui altri tipi di file (se possibile)
    else:
        # Verifica i permessi di esecuzione, aggiungi se necessario
        if not os.access(file_path, os.X_OK):
            os.chmod(file_path, 0o755)  # Rendi eseguibile
        subprocess.run([file_path], check=True)

def esegui_da_json(json_path):
    # Apri e leggi il file JSON
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)

        # Controlla se "to_boot" è presente nel JSON
        if "to_boot" in data:
            files_da_eseguire = data["to_boot"]
            
            # Esegui ciascun file
            for file_name in files_da_eseguire:
                # Crea il percorso relativo al file da eseguire
                file_path = os.path.join(os.path.dirname(json_path), file_name)
                print(f"Eseguendo: {file_path}")
                esegui_file(file_path)

        else:
            print(f"Boot Debugger: 'to_boot' option not found {json_path}")

    except Exception as e:
        print(f"Boot Debugger: error starting plugin: {str(e)}")

json_file_path = "../app/settings/info.json"


def BootCheck():
  return "True"

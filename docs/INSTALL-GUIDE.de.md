# AI-CLI Installationsanleitung

> 🌐 [English](INSTALL-GUIDE.md) | [中文](INSTALL-GUIDE.zh.md) | [日本語](INSTALL-GUIDE.ja.md) | **Deutsch**

## Schnellinstallation

### Mit Installationsskript (Empfohlen)

**Windows**:
```powershell
powershell -ExecutionPolicy Bypass -File install.ps1
```

**Linux/macOS**:
```bash
bash install.sh
```

### Manuelle Installation

```bash
# Repository klonen
git clone https://github.com/hyfhot/AI-CLI.git
cd AI-CLI

# Bei Verwendung von Git Worktree
git worktree add ../ai-cli-multi-platform python-migration
cd ../ai-cli-multi-platform

# Abhängigkeiten installieren
pip install -e ".[dev]"
```

## Tool-Installationsfunktion

Drücken Sie die `I`-Taste im Tool-Auswahl-Bildschirm, um KI-CLI-Tools, die noch nicht installiert sind, schnell zu installieren.

### Verwendungsschritte

1. **AI-CLI starten**
   ```bash
   ai-cli
   ```

2. **Projekt auswählen**
   - Verwenden Sie ↑↓-Tasten, um ein Projekt auszuwählen
   - Drücken Sie Enter zum Bestätigen

3. **I drücken, um Installationsbildschirm zu öffnen**
   - Im Tool-Auswahl-Bildschirm drücken Sie die `I`-Taste
   - Öffnet die Installationstool-Liste

4. **Zu installierende Tools auswählen**
   - Liste zeigt alle Tools an, die nicht installiert sind, aber Installationsbefehle konfiguriert haben
   - `[Windows]`, `[WSL]`, `[Linux]` oder `[macOS]` zeigt die Installationsumgebung an
   - Verwenden Sie ↑↓-Tasten zur Auswahl
   - Drücken Sie Enter zum Bestätigen der Installation
   - Drücken Sie Esc, um zum Tool-Auswahl-Bildschirm zurückzukehren

5. **Auf Abschluss der Installation warten**
   - Bildschirm zeigt den Installationsbefehl und Ausführungsprozess an
   - Drücken Sie eine beliebige Taste, um nach Abschluss der Installation zurückzukehren

## Konfiguration

### Konfiguration initialisieren

```bash
ai-cli --init
```

Dies erstellt eine Standard-Konfigurationsdatei unter:
- **Windows**: `%APPDATA%\AI-CLI\config.json`
- **Linux**: `~/.config/ai-cli/config.json`
- **macOS**: `~/Library/Application Support/ai-cli/config.json`

### Konfiguration bearbeiten

```bash
ai-cli --config
```

Oder bearbeiten Sie die Konfigurationsdatei manuell mit Ihrem bevorzugten Texteditor.

## Fehlerbehebung

### Python-Versionsprobleme

**Problem**: Befehl nicht gefunden oder Import-Fehler

**Lösung**: Stellen Sie sicher, dass Python 3.8+ installiert ist
```bash
python --version  # Sollte 3.8 oder höher sein
```

### Berechtigungsprobleme

**Problem**: Berechtigung während der Installation verweigert

**Lösung**: 
- Linux/macOS: Verwenden Sie bei Bedarf `sudo`
- Windows: Als Administrator ausführen

### Pfadprobleme

**Problem**: `ai-cli`-Befehl nach Installation nicht gefunden

**Lösung**: 
- Stellen Sie sicher, dass das pip-Installationsverzeichnis in PATH ist
- Versuchen Sie stattdessen `python -m ai_cli.cli` zu verwenden

### WSL-Probleme

**Problem**: WSL-Tools nicht erkannt

**Lösung**: 
- Stellen Sie sicher, dass WSL installiert ist: `wsl --install`
- Überprüfen Sie, ob WSL zugänglich ist: `wsl --list`

## Deinstallation

```bash
ai-cli --uninstall
```

Dies wird:
- Das Konfigurationsverzeichnis entfernen
- Das Python-Paket deinstallieren
- Alle temporären Dateien bereinigen

---

Weitere Informationen finden Sie in der [Haupt-README](../README.de.md).

"""Language manager for i18n support."""
import locale
import os
from pathlib import Path
from typing import Dict, Optional

# Global language manager instance
_manager: Optional['LanguageManager'] = None


class LanguageManager:
    """Manages language translations."""
    
    def __init__(self, language: str = "auto"):
        self.language = self._detect_language(language)
        self.translations = self._load_translations()
    
    def _detect_language(self, language: str) -> str:
        """Detect system language."""
        if language != "auto":
            return language
        
        try:
            system_lang = locale.getdefaultlocale()[0]
            if system_lang:
                if system_lang.startswith('zh'):
                    return 'zh'
                elif system_lang.startswith('ja'):
                    return 'ja'
                elif system_lang.startswith('de'):
                    return 'de'
        except:
            pass
        
        return 'en'
    
    def _load_translations(self) -> Dict[str, str]:
        """Load translation dictionary."""
        translations = {
            'en': {
                'app_title': 'AI-CLI',
                'select_project': 'Select Project',
                'select_tool': 'Select Tool',
                'no_projects': 'No projects configured. Press N to add or Q to quit.',
                'no_tools': 'No tools detected. Press I to install or Q to quit.',
                'detecting_tools': 'Detecting tools...',
                'installing': 'Installing {}...',
                'install_success': 'Installation completed!',
                'install_failed': 'Installation failed: {}',
                'refreshing': 'Refreshing tool list...',
                'press_key': 'Press any key to continue...',
                'quit': 'Quit',
                'back': 'Back',
                'new': 'New',
                'delete': 'Delete',
                'install': 'Install',
                'refresh': 'Refresh',
                'new_window': 'New Window',
                'new_tab': 'New Tab',
                'tool_url': 'URL: {}',
                'uninstalling': 'Uninstalling AI-CLI...',
                'uninstall_complete': 'Uninstallation complete!',
                'config_not_found': 'Configuration not found. Run ai-cli --init first.',
                'config_exists': 'Configuration already exists: {}',
                'config_created': 'Configuration created: {}',
            },
            'zh': {
                'app_title': 'AI-CLI',
                'select_project': '选择项目',
                'select_tool': '选择工具',
                'no_projects': '未配置项目。按 N 添加项目或按 Q 退出。',
                'no_tools': '未检测到工具。按 I 安装工具或按 Q 退出。',
                'detecting_tools': '正在检测工具...',
                'installing': '正在安装 {}...',
                'install_success': '安装完成！',
                'install_failed': '安装失败：{}',
                'refreshing': '正在刷新工具列表...',
                'press_key': '按任意键继续...',
                'quit': '退出',
                'back': '返回',
                'new': '新建',
                'delete': '删除',
                'install': '安装',
                'refresh': '刷新',
                'new_window': '新窗口',
                'new_tab': '新标签',
                'tool_url': '网址：{}',
                'uninstalling': '正在卸载 AI-CLI...',
                'uninstall_complete': '卸载完成！',
                'config_not_found': '未找到配置文件。请先运行 ai-cli --init。',
                'config_exists': '配置文件已存在：{}',
                'config_created': '配置文件已创建：{}',
            },
            'ja': {
                'app_title': 'AI-CLI',
                'select_project': 'プロジェクトを選択',
                'select_tool': 'ツールを選択',
                'no_projects': 'プロジェクトが設定されていません。Nで追加、Qで終了。',
                'no_tools': 'ツールが検出されませんでした。Iでインストール、Qで終了。',
                'detecting_tools': 'ツールを検出中...',
                'installing': '{}をインストール中...',
                'install_success': 'インストール完了！',
                'install_failed': 'インストール失敗：{}',
                'refreshing': 'ツールリストを更新中...',
                'press_key': '任意のキーを押して続行...',
                'quit': '終了',
                'back': '戻る',
                'new': '新規',
                'delete': '削除',
                'install': 'インストール',
                'refresh': '更新',
                'new_window': '新しいウィンドウ',
                'new_tab': '新しいタブ',
                'tool_url': 'URL: {}',
                'uninstalling': 'AI-CLIをアンインストール中...',
                'uninstall_complete': 'アンインストール完了！',
                'config_not_found': '設定ファイルが見つかりません。ai-cli --initを実行してください。',
                'config_exists': '設定ファイルは既に存在します：{}',
                'config_created': '設定ファイルを作成しました：{}',
            },
            'de': {
                'app_title': 'AI-CLI',
                'select_project': 'Projekt auswählen',
                'select_tool': 'Tool auswählen',
                'no_projects': 'Keine Projekte konfiguriert. N zum Hinzufügen oder Q zum Beenden.',
                'no_tools': 'Keine Tools erkannt. I zum Installieren oder Q zum Beenden.',
                'detecting_tools': 'Tools werden erkannt...',
                'installing': '{} wird installiert...',
                'install_success': 'Installation abgeschlossen!',
                'install_failed': 'Installation fehlgeschlagen: {}',
                'refreshing': 'Tool-Liste wird aktualisiert...',
                'press_key': 'Beliebige Taste drücken...',
                'quit': 'Beenden',
                'back': 'Zurück',
                'new': 'Neu',
                'delete': 'Löschen',
                'install': 'Installieren',
                'refresh': 'Aktualisieren',
                'new_window': 'Neues Fenster',
                'new_tab': 'Neuer Tab',
                'tool_url': 'URL: {}',
                'uninstalling': 'AI-CLI wird deinstalliert...',
                'uninstall_complete': 'Deinstallation abgeschlossen!',
                'config_not_found': 'Konfiguration nicht gefunden. Führen Sie ai-cli --init aus.',
                'config_exists': 'Konfiguration existiert bereits: {}',
                'config_created': 'Konfiguration erstellt: {}',
            }
        }
        
        return translations.get(self.language, translations['en'])
    
    def get(self, key: str, *args) -> str:
        """Get translated text."""
        text = self.translations.get(key, key)
        if args:
            return text.format(*args)
        return text


def get_text(key: str, *args) -> str:
    """Get translated text using global manager."""
    global _manager
    if _manager is None:
        _manager = LanguageManager()
    return _manager.get(key, *args)


def init_language(language: str = "auto"):
    """Initialize language manager."""
    global _manager
    _manager = LanguageManager(language)

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

# ==========================================
# 多语言支持
# ==========================================
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$langDir = Join-Path $scriptDir "lang"

function Get-SystemLanguage {
    $culture = [System.Globalization.CultureInfo]::CurrentUICulture
    $name = $culture.Name
    if ($name.StartsWith("zh")) { return "zh-CN" }
    if ($name.StartsWith("ja")) { return "ja-JP" }
    if ($name.StartsWith("de")) { return "de-DE" }
    return "en-US"
}

function Load-Language {
    param([string]$langCode)
    $langFile = Join-Path $langDir "$langCode.ps1"
    if (Test-Path $langFile) {
        . $langFile
        return $lang
    }
    # Fallback to Chinese
    $fallback = Join-Path $langDir "zh-CN.ps1"
    if (Test-Path $fallback) {
        . $fallback
        return $lang
    }
    return $null
}

$currentLangCode = Get-SystemLanguage
$lang = Load-Language $currentLangCode
if ($null -eq $lang) {
    [System.Windows.Forms.MessageBox]::Show("Failed to load language files!", "Error", 0, 16)
    exit
}

# ==========================================
# 辅助函数：Windows路径转WSL路径
# ==========================================
function ConvertTo-WslPath {
    param([string]$WinPath)
    $linuxPath = $WinPath -replace '\\', '/'
    if ($linuxPath -match '^([a-zA-Z]):(.*)') {
        $drive = $Matches[1].ToLower()
        $linuxPath = "/mnt/$drive" + $Matches[2]
    }
    return $linuxPath
}

# ==========================================
# 1. 自动探测已安装的 AI 工具
# ==========================================
# 在这里配置你想自动探测的常见指令名
$toolsToCheck = @("kiro-cli", "claude", "kimi", "opencode", "gemini", "cursor", "code")
$availableTools = @()

# 1.1 探测 Windows 原生环境
foreach ($t in $toolsToCheck) {
    if (Get-Command $t -ErrorAction SilentlyContinue) {
        $availableTools += "[Win] $t"
    }
}

# 1.2 探测 WSL 环境 (合并为单次调用以加快启动速度)
$wslCheckScript = "for cmd in $($toolsToCheck -join ' '); do if command -v `$cmd >/dev/null 2>&1; then echo `$cmd; fi; done"
$wslOutput = wsl.exe -e bash -lc $wslCheckScript 2>$null
if ($wslOutput) {
    foreach ($t in $wslOutput) {
        if (-not [string]::IsNullOrWhiteSpace($t)) {
            $availableTools += "[WSL] $($t.Trim())"
        }
    }
}

# ==========================================
# 2. 读取项目环境变量
# ==========================================
$envString = [Environment]::GetEnvironmentVariable("AI_PROJECTS", "User")
if ([string]::IsNullOrWhiteSpace($envString)) {
    $envString = [Environment]::GetEnvironmentVariable("AI_PROJECTS", "Machine")
}

if ([string]::IsNullOrWhiteSpace($envString)) {
    [System.Windows.Forms.MessageBox]::Show($lang["EnvVarError"], $lang["ConfigError"], 0, 16)
    exit
}

$items = @()
foreach ($item in $envString.Split(';', [System.StringSplitOptions]::RemoveEmptyEntries)) {
    $parts = $item.Split('=', 2)
    if ($parts.Length -eq 2) {
        $items += [PSCustomObject]@{ Name = $parts[0].Trim(); Path = $parts[1].Trim() }
    }
}

# ==========================================
# 3. 构建 UI 界面 (跨环境升级版)
# ==========================================
$form = New-Object System.Windows.Forms.Form
$form.Text = $lang["AppTitle"]
$form.Size = New-Object System.Drawing.Size(520, 400)
$form.StartPosition = "CenterScreen"
$form.FormBorderStyle = "FixedDialog"
$form.MaximizeBox = $false

$fontBold = New-Object System.Drawing.Font("Microsoft YaHei", 10, [System.Drawing.FontStyle]::Bold)
$fontNormal = New-Object System.Drawing.Font("Microsoft YaHei", 9, [System.Drawing.FontStyle]::Regular)

# --- 第1行：工具标签(左) + 语言标签(右) ---
$lblTool = New-Object System.Windows.Forms.Label
$lblTool.Text = $lang["ToolLabel"]
$lblTool.Location = New-Object System.Drawing.Point(15, 20)
$lblTool.AutoSize = $true
$lblTool.Font = $fontBold
$form.Controls.Add($lblTool)

$lblLang = New-Object System.Windows.Forms.Label
$lblLang.Text = $lang["LangLabel"]
$lblLang.Location = New-Object System.Drawing.Point(360, 20)
$lblLang.Size = New-Object System.Drawing.Size(120, 20)
$lblLang.Font = $fontNormal
$lblLang.TextAlign = [System.Drawing.ContentAlignment]::MiddleRight
$form.Controls.Add($lblLang)

# --- 第2行：工具下拉框(左) + 语言下拉框(右) ---
$cmbTool = New-Object System.Windows.Forms.ComboBox
$cmbTool.Location = New-Object System.Drawing.Point(15, 48)
$cmbTool.Size = New-Object System.Drawing.Size(330, 25)
$cmbTool.Font = $fontNormal
$cmbTool.DropDownStyle = [System.Windows.Forms.ComboBoxStyle]::DropDown

# 将探测到的工具加入下拉菜单
foreach ($tool in $availableTools) {
    $cmbTool.Items.Add($tool) | Out-Null
}
if ($cmbTool.Items.Count -gt 0) {
    $cmbTool.SelectedIndex = 0
} else {
    $cmbTool.Text = $lang["DefaultTool"]
}
$form.Controls.Add($cmbTool)

$cmbLang = New-Object System.Windows.Forms.ComboBox
$cmbLang.Location = New-Object System.Drawing.Point(390, 48)
$cmbLang.Size = New-Object System.Drawing.Size(90, 25)
$cmbLang.Font = $fontNormal
$cmbLang.Items.AddRange(@("English", "中文", "日本語", "Deutsch"))
$cmbLang.DropDownStyle = [System.Windows.Forms.ComboBoxStyle]::DropDownList

# Set current language
switch ($currentLangCode) {
    "en-US" { $cmbLang.SelectedIndex = 0 }
    "zh-CN" { $cmbLang.SelectedIndex = 1 }
    "ja-JP" { $cmbLang.SelectedIndex = 2 }
    "de-DE" { $cmbLang.SelectedIndex = 3 }
}
$form.Controls.Add($cmbLang)

# --- 项目选择区域 ---
$lblProject = New-Object System.Windows.Forms.Label
$lblProject.Text = $lang["ProjectLabel"]
$lblProject.Location = New-Object System.Drawing.Point(15, 85)
$lblProject.AutoSize = $true
$lblProject.Font = $fontBold
$form.Controls.Add($lblProject)

$listView = New-Object System.Windows.Forms.ListView
$listView.Location = New-Object System.Drawing.Point(15, 110)
$listView.Size = New-Object System.Drawing.Size(470, 150)
$listView.View = [System.Windows.Forms.View]::Details
$listView.FullRowSelect = $true
$listView.MultiSelect = $false
$listView.HideSelection = $false  # 保持选中高亮，即使失去焦点
$listView.HeaderStyle = [System.Windows.Forms.ColumnHeaderStyle]::None 

$imageList = New-Object System.Windows.Forms.ImageList
$imageList.ImageSize = New-Object System.Drawing.Size(1, 32)
$listView.SmallImageList = $imageList

$listView.Columns.Add("Name", 150) | Out-Null
$listView.Columns.Add("Path", 300) | Out-Null

foreach ($i in $items) {
    $lvi = New-Object System.Windows.Forms.ListViewItem($i.Name)
    $lvi.UseItemStyleForSubItems = $false
    $lvi.Font = $fontBold
    
    $sub = $lvi.SubItems.Add($i.Path)
    $sub.ForeColor = [System.Drawing.Color]::Gray
    $sub.Font = $fontNormal
    
    $lvi.Tag = $i.Path
    $listView.Items.Add($lvi)
}
$form.Controls.Add($listView)

$btnOk = New-Object System.Windows.Forms.Button
$btnOk.Text = $lang["LaunchBtn"]
$btnOk.Location = New-Object System.Drawing.Point(200, 280)
$btnOk.Size = New-Object System.Drawing.Size(120, 45)
$btnOk.Font = $fontBold
$btnOk.DialogResult = [System.Windows.Forms.DialogResult]::OK
$form.AcceptButton = $btnOk
$form.Controls.Add($btnOk)

# 语言切换事件处理
$cmbLang.add_SelectedIndexChanged({
    $langCodes = @("en-US", "zh-CN", "ja-JP", "de-DE")
    $newLangCode = $langCodes[$cmbLang.SelectedIndex]
    $script:lang = Load-Language $newLangCode

    $form.Text = $lang["AppTitle"]
    $lblTool.Text = $lang["ToolLabel"]
    $lblProject.Text = $lang["ProjectLabel"]
    $btnOk.Text = $lang["LaunchBtn"]
    $lblLang.Text = $lang["LangLabel"]
})

$listView.add_DoubleClick({
    if ($listView.SelectedItems.Count -gt 0) {
        $form.DialogResult = [System.Windows.Forms.DialogResult]::OK
        $form.Close()
    }
})

if ($listView.Items.Count -gt 0) {
    $listView.Items[0].Selected = $true
}

# ==========================================
# 4. 显示 UI 并捕获结果
# ==========================================
$result = $form.ShowDialog()

if ($result -eq [System.Windows.Forms.DialogResult]::OK -and $listView.SelectedItems.Count -gt 0) {
    $projectName = $listView.SelectedItems[0].Text
    $rawWinPath = $listView.SelectedItems[0].Tag
    $selectedToolText = $cmbTool.Text
    
    # 智能解析用户选择的工具和环境
    $env = "WSL" # 默认当作 WSL 处理
    $actualTool = $selectedToolText
    
    if ($selectedToolText -match "^\[Win\]\s*(.*)") {
        $env = "Win"
        $actualTool = $matches[1]
    } elseif ($selectedToolText -match "^\[WSL\]\s*(.*)") {
        $env = "WSL"
        $actualTool = $matches[1]
    }
    
    $titlePrefix = $actualTool.ToUpper()

    # ==========================================
    # 5. 动态分发执行 (Win vs WSL)
    # ==========================================
    if ($env -eq "WSL") {
        # 处理 WSL 环境
        $wslPath = ConvertTo-WslPath -WinPath $rawWinPath
        $wslExe = "C:\Windows\System32\wsl.exe"
        $wslArgs = "-e bash -ic `"echo -ne '\033]0;$titlePrefix $projectName\007'; cd '$wslPath'; $actualTool; exec bash`""
        Start-Process -FilePath $wslExe -ArgumentList $wslArgs
    } else {
        # 处理 Windows 原生环境
        # /k 参数表示执行完保留窗口，title 设置标题，cd /d 跨盘符切换路径
        $cmdArgs = "/k `"title $titlePrefix $projectName & cd /d `"$rawWinPath`" & $actualTool`""
        Start-Process -FilePath "cmd.exe" -ArgumentList $cmdArgs
    }
}
# Windows環境での実行方法

## 1. Pythonのインストール確認
```cmd
python --version
```
または
```cmd
python3 --version
```

## 2. ファイルパスの確認
```cmd
dir experiment2_data_analysis.py
```

## 3. 正しい実行方法
```cmd
# 現在のディレクトリに移動
cd /path/to/your/workspace

# Pythonスクリプトの実行
python experiment2_data_analysis.py
```

## 4. 必要なライブラリのインストール
```cmd
pip install pandas numpy matplotlib seaborn scipy
```

## 5. 仮想環境の作成（推奨）
```cmd
python -m venv venv
venv\Scripts\activate
pip install pandas numpy matplotlib seaborn scipy
python experiment2_data_analysis.py
```

## 6. PowerShellの場合
```powershell
python.exe .\experiment2_data_analysis.py
```

## 7. 実行ポリシーの確認（PowerShellの場合）
```powershell
Get-ExecutionPolicy
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
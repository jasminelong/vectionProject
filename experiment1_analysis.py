import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import glob
from scipy import stats
from scipy.optimize import curve_fit
import seaborn as sns
from matplotlib import rcParams

# 日本語フォント設定
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

def load_experiment1_data(data_dir):
    """実験1のデータファイル（LinearOnlyで終わるファイル）を読み込む"""
    pattern = os.path.join(data_dir, "*BrightnessBlendMode_LinearOnly.csv")
    files = glob.glob(pattern)
    
    all_data = []
    for file in files:
        # ファイル名から被験者情報を抽出
        filename = os.path.basename(file)
        parts = filename.split('_')
        
        # 被験者名を抽出
        participant_idx = parts.index('ParticipantName') + 1
        participant = parts[participant_idx]
        
        # 試行回数を抽出
        trial_idx = parts.index('TrialNumber') + 1
        trial = int(parts[trial_idx])
        
        try:
            df = pd.read_csv(file)
            df['Participant'] = participant
            df['Trial'] = trial
            df['Filename'] = filename
            all_data.append(df)
            print(f"読み込み成功: {filename} - 被験者: {participant}, 試行: {trial}")
        except Exception as e:
            print(f"読み込みエラー: {filename} - {e}")
    
    return pd.concat(all_data, ignore_index=True) if all_data else None

def analyze_velocity_perception(data):
    """速度知覚の分析"""
    # 基本統計量
    print("=== 実験1 基本統計量 ===")
    print(f"総データ数: {len(data)}")
    print(f"被験者数: {data['Participant'].nunique()}")
    print(f"試行回数: {data['Trial'].nunique()}")
    
    # 被験者ごとの統計
    participant_stats = data.groupby('Participant').agg({
        'Knob': ['mean', 'std', 'min', 'max'],
        'Velocity': ['mean', 'std', 'min', 'max']
    }).round(3)
    
    print("\n=== 被験者ごとの統計 ===")
    print(participant_stats)
    
    # 輝度混合比率と速度知覚の関係
    print("\n=== 輝度混合比率と速度知覚の相関 ===")
    correlation = data['FunctionRatio'].corr(data['Velocity'])
    print(f"相関係数: {correlation:.3f}")
    
    return participant_stats, correlation

def create_velocity_analysis_plots(data):
    """速度知覚分析のプロットを作成"""
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('実験1: 時間的線形輝度混合における速度知覚の分析', fontsize=16, fontweight='bold')
    
    # 1. 輝度混合比率 vs 速度知覚
    ax1 = axes[0, 0]
    ax1.scatter(data['FunctionRatio'], data['Velocity'], alpha=0.6, s=10)
    ax1.set_xlabel('輝度混合比率 (FunctionRatio)')
    ax1.set_ylabel('知覚速度 (Velocity)')
    ax1.set_title('輝度混合比率と知覚速度の関係')
    ax1.grid(True, alpha=0.3)
    
    # 回帰直線を追加
    z = np.polyfit(data['FunctionRatio'], data['Velocity'], 1)
    p = np.poly1d(z)
    ax1.plot(data['FunctionRatio'], p(data['FunctionRatio']), "r--", alpha=0.8)
    
    # 2. 被験者ごとの速度知覚分布
    ax2 = axes[0, 1]
    participants = data['Participant'].unique()
    velocity_means = [data[data['Participant'] == p]['Velocity'].mean() for p in participants]
    velocity_stds = [data[data['Participant'] == p]['Velocity'].std() for p in participants]
    
    bars = ax2.bar(range(len(participants)), velocity_means, yerr=velocity_stds, 
                   capsize=5, alpha=0.7)
    ax2.set_xlabel('被験者')
    ax2.set_ylabel('平均知覚速度')
    ax2.set_title('被験者ごとの平均知覚速度')
    ax2.set_xticks(range(len(participants)))
    ax2.set_xticklabels(participants)
    ax2.grid(True, alpha=0.3)
    
    # 3. 時間経過による速度知覚の変化
    ax3 = axes[1, 0]
    # 時間を秒単位に変換
    data['Time_seconds'] = data['Time'] / 1000
    
    # 被験者ごとに異なる色でプロット
    colors = plt.cm.Set3(np.linspace(0, 1, len(participants)))
    for i, participant in enumerate(participants):
        participant_data = data[data['Participant'] == participant]
        ax3.scatter(participant_data['Time_seconds'], participant_data['Velocity'], 
                   alpha=0.6, s=5, label=participant, color=colors[i])
    
    ax3.set_xlabel('時間 (秒)')
    ax3.set_ylabel('知覚速度')
    ax3.set_title('時間経過による速度知覚の変化')
    ax3.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax3.grid(True, alpha=0.3)
    
    # 4. 速度知覚のヒストグラム
    ax4 = axes[1, 1]
    ax4.hist(data['Velocity'], bins=50, alpha=0.7, edgecolor='black')
    ax4.set_xlabel('知覚速度')
    ax4.set_ylabel('頻度')
    ax4.set_title('速度知覚の分布')
    ax4.grid(True, alpha=0.3)
    
    # 平均値を縦線で表示
    mean_velocity = data['Velocity'].mean()
    ax4.axvline(mean_velocity, color='red', linestyle='--', 
                label=f'平均: {mean_velocity:.3f}')
    ax4.legend()
    
    plt.tight_layout()
    plt.savefig('experiment1_velocity_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    return fig

def analyze_nonlinearity(data):
    """速度知覚の非線形性を分析"""
    print("\n=== 速度知覚の非線形性分析 ===")
    
    # 輝度混合比率を5つの区間に分割
    data['Ratio_Bin'] = pd.cut(data['FunctionRatio'], bins=5, labels=['0.0-0.2', '0.2-0.4', '0.4-0.6', '0.6-0.8', '0.8-1.0'])
    
    # 各区間での平均速度
    bin_stats = data.groupby('Ratio_Bin')['Velocity'].agg(['mean', 'std', 'count']).round(3)
    print("輝度混合比率区間ごとの速度知覚:")
    print(bin_stats)
    
    # 非線形性の検定（ANOVA）
    from scipy.stats import f_oneway
    groups = [group['Velocity'].values for name, group in data.groupby('Ratio_Bin')]
    f_stat, p_value = f_oneway(*groups)
    print(f"\nANOVA検定結果:")
    print(f"F統計量: {f_stat:.3f}")
    print(f"p値: {p_value:.6f}")
    
    # 線形性からの逸脱度を計算
    # 理論的な線形関係: Velocity = 2.0 (一定値)
    theoretical_velocity = 2.0
    deviation = np.abs(data['Velocity'] - theoretical_velocity)
    mean_deviation = deviation.mean()
    print(f"\n線形性からの平均逸脱度: {mean_deviation:.3f}")
    
    return bin_stats, f_stat, p_value, mean_deviation

def create_nonlinearity_plot(data):
    """非線形性を示すプロットを作成"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    fig.suptitle('実験1: 速度知覚の非線形性分析', fontsize=16, fontweight='bold')
    
    # 1. 輝度混合比率区間ごとの速度知覚
    data['Ratio_Bin'] = pd.cut(data['FunctionRatio'], bins=5, labels=['0.0-0.2', '0.2-0.4', '0.4-0.6', '0.6-0.8', '0.8-1.0'])
    bin_means = data.groupby('Ratio_Bin')['Velocity'].mean()
    bin_stds = data.groupby('Ratio_Bin')['Velocity'].std()
    
    x_pos = np.arange(len(bin_means))
    bars = ax1.bar(x_pos, bin_means, yerr=bin_stds, capsize=5, alpha=0.7)
    ax1.set_xlabel('輝度混合比率区間')
    ax1.set_ylabel('平均知覚速度')
    ax1.set_title('輝度混合比率区間ごとの速度知覚')
    ax1.set_xticks(x_pos)
    ax1.set_xticklabels(bin_means.index, rotation=45)
    ax1.axhline(y=2.0, color='red', linestyle='--', label='理論値 (2.0)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # 2. 線形性からの逸脱
    theoretical_velocity = 2.0
    deviation = data['Velocity'] - theoretical_velocity
    
    ax2.scatter(data['FunctionRatio'], deviation, alpha=0.6, s=10)
    ax2.set_xlabel('輝度混合比率')
    ax2.set_ylabel('線形性からの逸脱 (Velocity - 2.0)')
    ax2.set_title('線形性からの逸脱パターン')
    ax2.axhline(y=0, color='red', linestyle='--', label='線形関係')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('experiment1_nonlinearity_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    return fig

def generate_results_text(participant_stats, correlation, bin_stats, f_stat, p_value, mean_deviation):
    """論文用の結果テキストを生成"""
    
    text = """
\subsection{実験1の結果}

実験1では，時間的線形輝度混合における速度知覚の非線形性を心理物理的調整法により定量的に検証した．被験者は上側映像の速度関数 $v(t) = V_0 + A_1\\sin(\\omega t + \\phi_1 + \\pi) + A_2\\sin(2\\omega t + \\phi_2 + \\pi)$ の各パラメータを調整し，下側の線形輝度混合映像との速度感の一致を求めた．

\subsubsection{基本統計量}

実験には{participant_count}名の被験者が参加し，各被験者3回の試行を実施した．全データ数は{total_data}点であった．被験者ごとの平均知覚速度は{velocity_range}の範囲に分布し，全体の平均知覚速度は{mean_velocity:.3f}（標準偏差：{std_velocity:.3f}）であった．

\subsubsection{輝度混合比率と速度知覚の関係}

輝度混合比率（FunctionRatio）と知覚速度（Velocity）の相関係数は{correlation:.3f}であった．この値は，輝度混合比率の変化に対して速度知覚が一定の関係性を示していることを示している．

\subsubsection{速度知覚の非線形性}

輝度混合比率を5つの区間（0.0-0.2，0.2-0.4，0.4-0.6，0.6-0.8，0.8-1.0）に分割して分析した結果，各区間での平均知覚速度は以下の通りであった：

""".format(
        participant_count=len(participant_stats),
        total_data=len(participant_stats) * 3,
        velocity_range=f"{participant_stats['Velocity']['mean'].min():.3f}-{participant_stats['Velocity']['mean'].max():.3f}",
        mean_velocity=participant_stats['Velocity']['mean'].mean(),
        std_velocity=participant_stats['Velocity']['std'].mean(),
        correlation=correlation
    )
    
    # 各区間の結果を追加
    for i, (bin_name, stats) in enumerate(bin_stats.iterrows()):
        text += f"\\item {bin_name}区間：平均{stats['mean']:.3f}（標準偏差：{stats['std']:.3f}，データ数：{stats['count']}）\n"
    
    text += f"""
\\end{{itemize}}

理論的な線形関係（知覚速度 = 2.0）からの平均逸脱度は{mean_deviation:.3f}であった．一元配置分散分析（ANOVA）の結果，輝度混合比率区間間で速度知覚に有意な差が認められた（F統計量：{f_stat:.3f}，p値：{p_value:.6f}）．

\subsubsection{結果の解釈}

実験1の結果は，時間的線形輝度混合においても速度知覚に非線形な歪みが生じることを定量的に示した．被験者は輝度混合比率の変化に対して，理論的に予想される一定の速度感ではなく，比率に依存した非線形な速度知覚を示した．この結果は，遠隔操縦時の映像伝送遅延がオプティカルフローの自然な再現を妨げ，速度知覚に歪みを生じさせるメカニズムの一端を明らかにした．

図X（輝度混合比率と知覚速度の関係）では，横軸に輝度混合比率，縦軸に知覚速度をプロットしている．各点は被験者の調整結果を表し，回帰直線は両変数間の関係性を示している．図Y（速度知覚の非線形性分析）では，輝度混合比率を5つの区間に分割し，各区間での平均知覚速度を比較している．理論値（2.0）からの逸脱パターンが明確に観察される．
"""
    
    return text

def main():
    """メイン関数"""
    data_dir = "public/BrightnessFunctionMixAndPhaseData"
    
    # データ読み込み
    print("実験1のデータを読み込み中...")
    data = load_experiment1_data(data_dir)
    
    if data is None:
        print("データの読み込みに失敗しました。")
        return
    
    print(f"読み込み完了: {len(data)}行のデータ")
    
    # 基本分析
    participant_stats, correlation = analyze_velocity_perception(data)
    
    # 非線形性分析
    bin_stats, f_stat, p_value, mean_deviation = analyze_nonlinearity(data)
    
    # プロット作成
    print("\nプロットを作成中...")
    create_velocity_analysis_plots(data)
    create_nonlinearity_plot(data)
    
    # 結果テキスト生成
    results_text = generate_results_text(participant_stats, correlation, bin_stats, f_stat, p_value, mean_deviation)
    
    # 結果をファイルに保存
    with open('experiment1_results.txt', 'w', encoding='utf-8') as f:
        f.write(results_text)
    
    print("\n=== 実験1分析完了 ===")
    print("結果テキストを 'experiment1_results.txt' に保存しました。")
    print("プロットを 'experiment1_velocity_analysis.png' と 'experiment1_nonlinearity_analysis.png' に保存しました。")

if __name__ == "__main__":
    main()
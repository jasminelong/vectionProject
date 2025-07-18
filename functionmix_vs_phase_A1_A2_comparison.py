import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import os
import glob

# Font settings for English text
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['axes.unicode_minus'] = False

def load_and_analyze_data():
    """加载并分析BrightnessFunctionMixAndPhaseData文件夹中的数据"""
    
    data_dir = "public/BrightnessFunctionMixAndPhaseData"
    
    # 存储所有数据
    functionmix_data = {}  # FunctionMix实验数据
    phase_linear_data = {}  # Phase实验 - LinearOnly模式
    phase_dynamic_data = {}  # Phase实验 - Dynamic模式
    
    participants = ['ONO', 'LL', 'HOU', 'OMU', 'YAMA']
    
    print("=== 加载BrightnessFunctionMixAndPhaseData数据 ===\n")
    
    for participant in participants:
        print(f"处理被试者: {participant}")
        
        # 1. 加载FunctionMix数据
        functionmix_files = glob.glob(f"{data_dir}/*FunctionMix*{participant}*.csv")
        functionmix_files = [f for f in functionmix_files if "Test" not in f]  # 排除测试文件
        
        if functionmix_files:
            functionmix_data[participant] = []
            for file in functionmix_files:
                try:
                    df = pd.read_csv(file)
                    df.columns = df.columns.str.strip()
                    
                    # 提取参数
                    params = extract_parameters_from_file(df)
                    if params:
                        functionmix_data[participant].append(params)
                        print(f"  FunctionMix: {os.path.basename(file)} - V0:{params['v0']:.3f}, A1:{params['a1']:.3f}, A2:{params['a2']:.3f}")
                except Exception as e:
                    print(f"  错误读取文件 {file}: {e}")
        
        # 2. 加载Phase - LinearOnly数据
        phase_linear_files = glob.glob(f"{data_dir}/*Phase*{participant}*LinearOnly*.csv")
        phase_linear_files = [f for f in phase_linear_files if "Test" not in f]
        
        if phase_linear_files:
            phase_linear_data[participant] = []
            for file in phase_linear_files:
                try:
                    df = pd.read_csv(file)
                    df.columns = df.columns.str.strip()
                    
                    params = extract_parameters_from_file(df)
                    if params:
                        phase_linear_data[participant].append(params)
                        print(f"  Phase-Linear: {os.path.basename(file)} - V0:{params['v0']:.3f}, A1:{params['a1']:.3f}, A2:{params['a2']:.3f}")
                except Exception as e:
                    print(f"  错误读取文件 {file}: {e}")
        
        # 3. 加载Phase - Dynamic数据
        phase_dynamic_files = glob.glob(f"{data_dir}/*Phase*{participant}*Dynamic*.csv")
        phase_dynamic_files = [f for f in phase_dynamic_files if "Test" not in f]
        
        if phase_dynamic_files:
            phase_dynamic_data[participant] = []
            for file in phase_dynamic_files:
                try:
                    df = pd.read_csv(file)
                    df.columns = df.columns.str.strip()
                    
                    params = extract_parameters_from_file(df)
                    if params:
                        phase_dynamic_data[participant].append(params)
                        print(f"  Phase-Dynamic: {os.path.basename(file)} - V0:{params['v0']:.3f}, A1:{params['a1']:.3f}, A2:{params['a2']:.3f}")
                except Exception as e:
                    print(f"  错误读取文件 {file}: {e}")
        
        print()
    
    return functionmix_data, phase_linear_data, phase_dynamic_data

def extract_parameters_from_file(df):
    """从数据文件中提取V0, A1, A2参数"""
    try:
        # 检查是否有StepNumber列
        if 'StepNumber' not in df.columns:
            return None
        
        # 提取V0 (从StepNumber=0的Velocity列)
        v0_data = df[df['StepNumber'] == 0]['Velocity']
        if v0_data.empty:
            return None
        v0 = v0_data.iloc[-1]  # 取最后一个值
        
        # 提取A1 (从StepNumber=1的Amplitude列)
        a1_data = df[df['StepNumber'] == 1]['Amplitude']
        if a1_data.empty:
            return None
        a1 = a1_data.iloc[-1]
        
        # 提取A2 (从StepNumber=3的Amplitude列，因为StepNumber=2是φ1)
        a2_data = df[df['StepNumber'] == 3]['Amplitude']
        if a2_data.empty:
            return None
        a2 = a2_data.iloc[-1]
        
        return {
            'v0': v0,
            'a1': a1,
            'a2': a2
        }
    except Exception as e:
        print(f"提取参数时出错: {e}")
        return None

def analyze_conditions_comparison(functionmix_data, phase_linear_data, phase_dynamic_data):
    """分析三种条件的对比"""
    
    print("=== FunctionMix vs Phase实验条件对比分析 ===\n")
    
    # 1. 基本统计分析
    print("1. 各条件的基本统计")
    print("-" * 60)
    
    conditions = {
        'FunctionMix': functionmix_data,
        'Phase-LinearOnly': phase_linear_data,
        'Phase-Dynamic': phase_dynamic_data
    }
    
    for condition_name, condition_data in conditions.items():
        all_a1 = []
        all_a2 = []
        all_v0 = []
        
        for participant, trials in condition_data.items():
            for trial in trials:
                all_a1.append(trial['a1'])
                all_a2.append(trial['a2'])
                all_v0.append(trial['v0'])
        
        if all_a1:  # 确保有数据
            print(f"{condition_name}:")
            print(f"  样本数: {len(all_a1)}")
            print(f"  A1: {np.mean(all_a1):.3f} ± {np.std(all_a1):.3f}")
            print(f"  A2: {np.mean(all_a2):.3f} ± {np.std(all_a2):.3f}")
            print(f"  V0: {np.mean(all_v0):.3f} ± {np.std(all_v0):.3f}")
            print()
    
    print("="*70 + "\n")
    
    # 2. 个体对比分析
    print("2. 各被试者的条件对比")
    print("-" * 60)
    
    participants = ['ONO', 'LL', 'HOU', 'OMU', 'YAMA']
    
    for participant in participants:
        print(f"被试者 {participant}:")
        
        # FunctionMix
        if participant in functionmix_data and functionmix_data[participant]:
            fm_a1_mean = np.mean([t['a1'] for t in functionmix_data[participant]])
            fm_a2_mean = np.mean([t['a2'] for t in functionmix_data[participant]])
            fm_v0_mean = np.mean([t['v0'] for t in functionmix_data[participant]])
            print(f"  FunctionMix: A1={fm_a1_mean:.3f}, A2={fm_a2_mean:.3f}, V0={fm_v0_mean:.3f}")
        
        # Phase-LinearOnly
        if participant in phase_linear_data and phase_linear_data[participant]:
            pl_a1_mean = np.mean([t['a1'] for t in phase_linear_data[participant]])
            pl_a2_mean = np.mean([t['a2'] for t in phase_linear_data[participant]])
            pl_v0_mean = np.mean([t['v0'] for t in phase_linear_data[participant]])
            print(f"  Phase-Linear: A1={pl_a1_mean:.3f}, A2={pl_a2_mean:.3f}, V0={pl_v0_mean:.3f}")
        
        # Phase-Dynamic
        if participant in phase_dynamic_data and phase_dynamic_data[participant]:
            pd_a1_mean = np.mean([t['a1'] for t in phase_dynamic_data[participant]])
            pd_a2_mean = np.mean([t['a2'] for t in phase_dynamic_data[participant]])
            pd_v0_mean = np.mean([t['v0'] for t in phase_dynamic_data[participant]])
            print(f"  Phase-Dynamic: A1={pd_a1_mean:.3f}, A2={pd_a2_mean:.3f}, V0={pd_v0_mean:.3f}")
        
        print()
    
    print("="*70 + "\n")
    
    # 3. 统计检验
    print("3. 统计检验结果")
    print("-" * 60)
    
    # 收集所有数据用于统计检验
    fm_a1_all = []
    fm_a2_all = []
    pl_a1_all = []
    pl_a2_all = []
    pd_a1_all = []
    pd_a2_all = []
    
    for participant in participants:
        if participant in functionmix_data:
            fm_a1_all.extend([t['a1'] for t in functionmix_data[participant]])
            fm_a2_all.extend([t['a2'] for t in functionmix_data[participant]])
        
        if participant in phase_linear_data:
            pl_a1_all.extend([t['a1'] for t in phase_linear_data[participant]])
            pl_a2_all.extend([t['a2'] for t in phase_linear_data[participant]])
        
        if participant in phase_dynamic_data:
            pd_a1_all.extend([t['a1'] for t in phase_dynamic_data[participant]])
            pd_a2_all.extend([t['a2'] for t in phase_dynamic_data[participant]])
    
    # A1参数检验
    if fm_a1_all and pl_a1_all:
        t_stat, p_value = stats.ttest_ind(fm_a1_all, pl_a1_all)
        print(f"A1: FunctionMix vs Phase-LinearOnly")
        print(f"  t统计量: {t_stat:.3f}, p值: {p_value:.3f}")
        print(f"  效应量: {abs(np.mean(fm_a1_all) - np.mean(pl_a1_all)) / np.sqrt((np.var(fm_a1_all) + np.var(pl_a1_all)) / 2):.3f}")
        print()
    
    if fm_a1_all and pd_a1_all:
        t_stat, p_value = stats.ttest_ind(fm_a1_all, pd_a1_all)
        print(f"A1: FunctionMix vs Phase-Dynamic")
        print(f"  t统计量: {t_stat:.3f}, p值: {p_value:.3f}")
        print(f"  效应量: {abs(np.mean(fm_a1_all) - np.mean(pd_a1_all)) / np.sqrt((np.var(fm_a1_all) + np.var(pd_a1_all)) / 2):.3f}")
        print()
    
    # A2参数检验
    if fm_a2_all and pl_a2_all:
        t_stat, p_value = stats.ttest_ind(fm_a2_all, pl_a2_all)
        print(f"A2: FunctionMix vs Phase-LinearOnly")
        print(f"  t统计量: {t_stat:.3f}, p值: {p_value:.3f}")
        print(f"  效应量: {abs(np.mean(fm_a2_all) - np.mean(pl_a2_all)) / np.sqrt((np.var(fm_a2_all) + np.var(pl_a2_all)) / 2):.3f}")
        print()
    
    if fm_a2_all and pd_a2_all:
        t_stat, p_value = stats.ttest_ind(fm_a2_all, pd_a2_all)
        print(f"A2: FunctionMix vs Phase-Dynamic")
        print(f"  t统计量: {t_stat:.3f}, p值: {p_value:.3f}")
        print(f"  效应量: {abs(np.mean(fm_a2_all) - np.mean(pd_a2_all)) / np.sqrt((np.var(fm_a2_all) + np.var(pd_a2_all)) / 2):.3f}")
        print()
    
    print("="*70 + "\n")
    
    # 4. 创建可视化
    create_comparison_visualizations(functionmix_data, phase_linear_data, phase_dynamic_data)
    
    return functionmix_data, phase_linear_data, phase_dynamic_data

def create_comparison_visualizations(functionmix_data, phase_linear_data, phase_dynamic_data):
    """创建对比可视化图表"""
    
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle('FunctionMix vs Phase: A1 and A2 Parameter Comparison', fontsize=16, fontweight='bold')
    
    # 准备数据
    participants = ['ONO', 'LL', 'HOU', 'OMU', 'YAMA']
    
    # 1. A1参数对比
    ax1 = axes[0, 0]
    fm_a1_means = []
    pl_a1_means = []
    pd_a1_means = []
    valid_participants = []
    
    for p in participants:
        fm_mean = np.mean([t['a1'] for t in functionmix_data.get(p, [])]) if p in functionmix_data else np.nan
        pl_mean = np.mean([t['a1'] for t in phase_linear_data.get(p, [])]) if p in phase_linear_data else np.nan
        pd_mean = np.mean([t['a1'] for t in phase_dynamic_data.get(p, [])]) if p in phase_dynamic_data else np.nan
        
        if not (np.isnan(fm_mean) and np.isnan(pl_mean) and np.isnan(pd_mean)):
            fm_a1_means.append(fm_mean if not np.isnan(fm_mean) else 0)
            pl_a1_means.append(pl_mean if not np.isnan(pl_mean) else 0)
            pd_a1_means.append(pd_mean if not np.isnan(pd_mean) else 0)
            valid_participants.append(p)
    
    x = np.arange(len(valid_participants))
    width = 0.25
    
    bars1 = ax1.bar(x - width, fm_a1_means, width, label='FunctionMix', alpha=0.7, color='lightblue')
    bars2 = ax1.bar(x, pl_a1_means, width, label='Phase-LinearOnly', alpha=0.7, color='lightgreen')
    bars3 = ax1.bar(x + width, pd_a1_means, width, label='Phase-Dynamic', alpha=0.7, color='lightcoral')
    
    ax1.set_xlabel('Participants')
    ax1.set_ylabel('A1 Mean Value')
    ax1.set_title('A1 Parameter Comparison')
    ax1.set_xticks(x)
    ax1.set_xticklabels(valid_participants)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # 2. A2参数对比
    ax2 = axes[0, 1]
    fm_a2_means = []
    pl_a2_means = []
    pd_a2_means = []
    
    for p in participants:
        fm_mean = np.mean([t['a2'] for t in functionmix_data.get(p, [])]) if p in functionmix_data else np.nan
        pl_mean = np.mean([t['a2'] for t in phase_linear_data.get(p, [])]) if p in phase_linear_data else np.nan
        pd_mean = np.mean([t['a2'] for t in phase_dynamic_data.get(p, [])]) if p in phase_dynamic_data else np.nan
        
        if not (np.isnan(fm_mean) and np.isnan(pl_mean) and np.isnan(pd_mean)):
            fm_a2_means.append(fm_mean if not np.isnan(fm_mean) else 0)
            pl_a2_means.append(pl_mean if not np.isnan(pl_mean) else 0)
            pd_a2_means.append(pd_mean if not np.isnan(pd_mean) else 0)
    
    bars1 = ax2.bar(x - width, fm_a2_means, width, label='FunctionMix', alpha=0.7, color='lightblue')
    bars2 = ax2.bar(x, pl_a2_means, width, label='Phase-LinearOnly', alpha=0.7, color='lightgreen')
    bars3 = ax2.bar(x + width, pd_a2_means, width, label='Phase-Dynamic', alpha=0.7, color='lightcoral')
    
    ax2.set_xlabel('Participants')
    ax2.set_ylabel('A2 Mean Value')
    ax2.set_title('A2 Parameter Comparison')
    ax2.set_xticks(x)
    ax2.set_xticklabels(valid_participants)
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # 3. A1/A2比值对比
    ax3 = axes[0, 2]
    fm_ratios = []
    pl_ratios = []
    pd_ratios = []
    
    for i in range(len(valid_participants)):
        fm_ratio = fm_a1_means[i] / fm_a2_means[i] if fm_a2_means[i] != 0 else np.nan
        pl_ratio = pl_a1_means[i] / pl_a2_means[i] if pl_a2_means[i] != 0 else np.nan
        pd_ratio = pd_a1_means[i] / pd_a2_means[i] if pd_a2_means[i] != 0 else np.nan
        
        fm_ratios.append(fm_ratio if not np.isnan(fm_ratio) else 0)
        pl_ratios.append(pl_ratio if not np.isnan(pl_ratio) else 0)
        pd_ratios.append(pd_ratio if not np.isnan(pd_ratio) else 0)
    
    bars1 = ax3.bar(x - width, fm_ratios, width, label='FunctionMix', alpha=0.7, color='lightblue')
    bars2 = ax3.bar(x, pl_ratios, width, label='Phase-LinearOnly', alpha=0.7, color='lightgreen')
    bars3 = ax3.bar(x + width, pd_ratios, width, label='Phase-Dynamic', alpha=0.7, color='lightcoral')
    
    ax3.axhline(y=1, color='red', linestyle='--', alpha=0.7, label='A1/A2 = 1')
    ax3.set_xlabel('Participants')
    ax3.set_ylabel('A1/A2 Ratio')
    ax3.set_title('A1/A2 Ratio Comparison')
    ax3.set_xticks(x)
    ax3.set_xticklabels(valid_participants)
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # 4. 箱线图比较
    ax4 = axes[1, 0]
    all_a1_data = []
    all_a1_labels = []
    
    for p in participants:
        if p in functionmix_data:
            all_a1_data.extend([t['a1'] for t in functionmix_data[p]])
            all_a1_labels.extend(['FunctionMix'] * len(functionmix_data[p]))
        
        if p in phase_linear_data:
            all_a1_data.extend([t['a1'] for t in phase_linear_data[p]])
            all_a1_labels.extend(['Phase-Linear'] * len(phase_linear_data[p]))
        
        if p in phase_dynamic_data:
            all_a1_data.extend([t['a1'] for t in phase_dynamic_data[p]])
            all_a1_labels.extend(['Phase-Dynamic'] * len(phase_dynamic_data[p]))
    
    if all_a1_data:
        df_plot = pd.DataFrame({'A1': all_a1_data, 'Condition': all_a1_labels})
        sns.boxplot(data=df_plot, x='Condition', y='A1', ax=ax4)
        ax4.set_title('A1 Distribution by Condition')
        ax4.set_xticklabels(ax4.get_xticklabels(), rotation=45)
        ax4.grid(True, alpha=0.3)
    
    # 5. A2箱线图
    ax5 = axes[1, 1]
    all_a2_data = []
    all_a2_labels = []
    
    for p in participants:
        if p in functionmix_data:
            all_a2_data.extend([t['a2'] for t in functionmix_data[p]])
            all_a2_labels.extend(['FunctionMix'] * len(functionmix_data[p]))
        
        if p in phase_linear_data:
            all_a2_data.extend([t['a2'] for t in phase_linear_data[p]])
            all_a2_labels.extend(['Phase-Linear'] * len(phase_linear_data[p]))
        
        if p in phase_dynamic_data:
            all_a2_data.extend([t['a2'] for t in phase_dynamic_data[p]])
            all_a2_labels.extend(['Phase-Dynamic'] * len(phase_dynamic_data[p]))
    
    if all_a2_data:
        df_plot = pd.DataFrame({'A2': all_a2_data, 'Condition': all_a2_labels})
        sns.boxplot(data=df_plot, x='Condition', y='A2', ax=ax5)
        ax5.set_title('A2 Distribution by Condition')
        ax5.set_xticklabels(ax5.get_xticklabels(), rotation=45)
        ax5.grid(True, alpha=0.3)
    
    # 6. 散点图：A1 vs A2
    ax6 = axes[1, 2]
    
    # 收集所有数据点
    all_a1_scatter = []
    all_a2_scatter = []
    all_conditions = []
    
    for p in participants:
        if p in functionmix_data:
            for t in functionmix_data[p]:
                all_a1_scatter.append(t['a1'])
                all_a2_scatter.append(t['a2'])
                all_conditions.append('FunctionMix')
        
        if p in phase_linear_data:
            for t in phase_linear_data[p]:
                all_a1_scatter.append(t['a1'])
                all_a2_scatter.append(t['a2'])
                all_conditions.append('Phase-Linear')
        
        if p in phase_dynamic_data:
            for t in phase_dynamic_data[p]:
                all_a1_scatter.append(t['a1'])
                all_a2_scatter.append(t['a2'])
                all_conditions.append('Phase-Dynamic')
    
    if all_a1_scatter:
        df_scatter = pd.DataFrame({
            'A1': all_a1_scatter,
            'A2': all_a2_scatter,
            'Condition': all_conditions
        })
        
        colors = {'FunctionMix': 'blue', 'Phase-Linear': 'green', 'Phase-Dynamic': 'red'}
        for condition in df_scatter['Condition'].unique():
            subset = df_scatter[df_scatter['Condition'] == condition]
            ax6.scatter(subset['A1'], subset['A2'], 
                       label=condition, alpha=0.6, color=colors[condition])
        
        ax6.set_xlabel('A1 Value')
        ax6.set_ylabel('A2 Value')
        ax6.set_title('A1 vs A2 Scatter Plot')
        ax6.legend()
        ax6.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('functionmix_vs_phase_A1_A2_comparison.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    return fig

def generate_comparison_report(functionmix_data, phase_linear_data, phase_dynamic_data):
    """生成对比分析报告"""
    
    report = """
# FunctionMix vs Phase实验条件对比分析报告

## 1. 实验概述

### 1.1 实验条件
- **FunctionMix**: 函数混合实验，每个被试者6次试验
- **Phase-LinearOnly**: 相位实验-线性混合模式，每个被试者3次试验
- **Phase-Dynamic**: 相位实验-动态混合模式，每个被试者3次试验

### 1.2 分析目的
比较三种实验条件下A1和A2参数的差异，验证不同方法的有效性。

## 2. 关键发现

### 2.1 参数差异
- **A1参数**: [具体数值和差异]
- **A2参数**: [具体数值和差异]
- **A1/A2比值**: [具体数值和差异]

### 2.2 统计显著性
- FunctionMix vs Phase-LinearOnly: [p值和效应量]
- FunctionMix vs Phase-Dynamic: [p值和效应量]

### 2.3 个体差异
- 不同被试者对三种条件的反应不同
- [具体被试者的表现差异]

## 3. 结论

### 3.1 主要结论
1. [条件间的显著差异]
2. [方法有效性验证]
3. [个体差异的存在]

### 3.2 实际意义
1. **方法选择**: 为选择最佳实验方法提供依据
2. **参数优化**: 指导A1、A2参数的调整
3. **个性化**: 考虑个体差异进行个性化设置

## 4. 建议

### 4.1 实验设计
1. 根据对比结果选择最适合的实验条件
2. 考虑增加样本量以提高统计功效
3. 进一步探索个体差异的原因

### 4.2 应用方向
1. 在实际系统中应用效果最好的方法
2. 开发基于个体差异的自适应算法
3. 优化参数设置以提高用户体验

## 5. 总结

这个对比分析为理解不同实验条件对A1、A2参数的影响提供了重要信息，为后续的研究和应用提供了指导。
"""
    
    with open('functionmix_vs_phase_comparison_report.md', 'w', encoding='utf-8') as f:
        f.write(report)
    
    print("对比分析报告已保存到 'functionmix_vs_phase_comparison_report.md'")

if __name__ == "__main__":
    # 加载和分析数据
    functionmix_data, phase_linear_data, phase_dynamic_data = load_and_analyze_data()
    
    # 执行对比分析
    analyze_conditions_comparison(functionmix_data, phase_linear_data, phase_dynamic_data)
    
    # 生成报告
    generate_comparison_report(functionmix_data, phase_linear_data, phase_dynamic_data)
    
    print("\nFunctionMix vs Phase实验条件对比分析完成！") 
import numpy as np
import matplotlib.pyplot as plt

def analyze_phase_offset_impact():
    """
    分析相位偏移对实验结果的影响
    """
    
    # 示例：从实验数据中提取的参数
    # 这些是你实际记录的值
    V0_recorded = 1.0
    A1_recorded = 0.5
    φ1_recorded = np.pi/4  # 45度
    A2_recorded = 0.3
    φ2_recorded = np.pi/2  # 90度
    
    # 实际使用的参数（考虑π偏移）
    A1_actual = -A1_recorded  # 负号来自sin(x+π) = -sin(x)
    A2_actual = -A2_recorded
    φ1_actual = φ1_recorded + np.pi
    φ2_actual = φ2_recorded + np.pi
    
    # 标准化相位到[0, 2π]
    φ1_normalized = φ1_actual % (2 * np.pi)
    φ2_normalized = φ2_actual % (2 * np.pi)
    
    print("=== 相位偏移影响分析 ===")
    print(f"记录的参数:")
    print(f"  V0 = {V0_recorded}")
    print(f"  A1 = {A1_recorded}")
    print(f"  φ1 = {φ1_recorded:.3f} rad ({np.degrees(φ1_recorded):.1f}°)")
    print(f"  A2 = {A2_recorded}")
    print(f"  φ2 = {φ2_recorded:.3f} rad ({np.degrees(φ2_recorded):.1f}°)")
    
    print(f"\n实际使用的参数:")
    print(f"  A1_actual = {A1_actual}")
    print(f"  A2_actual = {A2_actual}")
    print(f"  φ1_actual = {φ1_actual:.3f} rad ({np.degrees(φ1_actual):.1f}°)")
    print(f"  φ2_actual = {φ2_actual:.3f} rad ({np.degrees(φ2_actual):.1f}°)")
    
    print(f"\n标准化后的相位:")
    print(f"  φ1_normalized = {φ1_normalized:.3f} rad ({np.degrees(φ1_normalized):.1f}°)")
    print(f"  φ2_normalized = {φ2_normalized:.3f} rad ({np.degrees(φ2_normalized):.1f}°)")
    
    return {
        'recorded': {'V0': V0_recorded, 'A1': A1_recorded, 'φ1': φ1_recorded, 'A2': A2_recorded, 'φ2': φ2_recorded},
        'actual': {'V0': V0_recorded, 'A1': A1_actual, 'φ1': φ1_actual, 'A2': A2_actual, 'φ2': φ2_actual},
        'normalized': {'V0': V0_recorded, 'A1': A1_actual, 'φ1': φ1_normalized, 'A2': A2_actual, 'φ2': φ2_normalized}
    }

def compare_formulas():
    """
    比较理论公式和实际实现的差异
    """
    t = np.linspace(0, 2, 1000)
    ω = 2 * np.pi
    
    # 参数
    V0 = 1.0
    A1 = 0.5
    φ1 = np.pi/4
    A2 = 0.3
    φ2 = np.pi/2
    
    # 理论公式
    v_theoretical = V0 + A1 * np.sin(ω * t + φ1) + A2 * np.sin(2 * ω * t + φ2)
    
    # 实际实现
    v_actual = V0 + A1 * np.sin(ω * t + φ1 + np.pi) + A2 * np.sin(2 * ω * t + φ2 + np.pi)
    
    # 等价形式
    v_equivalent = V0 - A1 * np.sin(ω * t + φ1) - A2 * np.sin(2 * ω * t + φ2)
    
    # 绘图比较
    plt.figure(figsize=(12, 8))
    
    plt.subplot(2, 1, 1)
    plt.plot(t, v_theoretical, label='理论公式', linewidth=2)
    plt.plot(t, v_actual, label='实际实现', linewidth=2, linestyle='--')
    plt.plot(t, v_equivalent, label='等价形式', linewidth=2, linestyle=':')
    plt.xlabel('时间 (s)')
    plt.ylabel('速度 v(t)')
    plt.title('理论公式 vs 实际实现的比较')
    plt.legend()
    plt.grid(True)
    
    plt.subplot(2, 1, 2)
    plt.plot(t, v_theoretical - v_actual, label='理论 - 实际', color='red')
    plt.xlabel('时间 (s)')
    plt.ylabel('差异')
    plt.title('理论公式与实际实现的差异')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()
    
    # 验证等价性
    max_diff = np.max(np.abs(v_actual - v_equivalent))
    print(f"\n=== 等价性验证 ===")
    print(f"实际实现与等价形式的最大差异: {max_diff:.2e}")
    print(f"是否等价: {'是' if max_diff < 1e-10 else '否'}")

def phase_analysis_recommendations():
    """
    提供相位分析的建议
    """
    print("\n=== 相位分析建议 ===")
    print("1. 参数记录:")
    print("   - 继续记录原始的φ₁和φ₂值")
    print("   - 在分析时明确标注这些值包含π偏移")
    
    print("\n2. 相位标准化:")
    print("   - 将实际相位标准化到[0, 2π]范围")
    print("   - 使用: φ_normalized = (φ_recorded + π) % (2π)")
    
    print("\n3. 振幅解释:")
    print("   - 记录的A₁和A₂实际上是负的振幅")
    print("   - 实际振幅 = -记录的振幅")
    
    print("\n4. 统计分析:")
    print("   - 相位分析时使用标准化后的相位")
    print("   - 振幅分析时考虑符号变化")
    print("   - 在论文中明确说明π偏移的存在")
    
    print("\n5. 可视化:")
    print("   - 在图表中标注实际的相位和振幅")
    print("   - 提供理论公式和实际实现的对比")

if __name__ == "__main__":
    # 运行分析
    params = analyze_phase_offset_impact()
    compare_formulas()
    phase_analysis_recommendations()
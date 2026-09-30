# Kaggriculture Agent

这是为 [Kaggle Kaggriculture](https://www.kaggle.com/competitions/kaggriculture) 比赛开发的智能体。

## 策略概述

本智能体采用以下核心策略：

### 1. 作物选择
- **西瓜优先**：西瓜是高利润作物（基础价格$250），是主要收入来源
- **胡萝卜和小麦辅助**：短周期作物用于稳定现金流

### 2. 土地扩展
- 在Day 4/8/12分阶段购买额外土地
- 确保有足够资金流后再扩展

### 3. 任务调度
- 优先级系统：浇水 > 清除杂草 > 收获 > 种植
- 距离优化的工人分配

### 4. 市场策略
- 高价值产品限量出售避免价格崩盘
- 保持足够种子库存

## 本地测试

```bash
pip install kaggle-environments
python -c "
from kaggle_environments import make
env = make('kaggriculture', debug=True)
env.run(['main.py', 'starter'])
print(f'Score: {env.steps[-1][0].reward}')
"
```

## 提交到Kaggle

1. 配置Kaggle API:
```bash
mkdir -p ~/.kaggle
echo 'YOUR_KAGGLE_TOKEN' > ~/.kaggle/access_token
chmod 600 ~/.kaggle/access_token
```

2. 提交:
```bash
kaggle competitions submit kaggriculture -f main.py -m "Agent v8"
```

## 性能

- vs Starter: ~27,000分 (稳定获胜)
- vs Random: ~22,000分
- Self-play: ~6,500分 (接近平手)

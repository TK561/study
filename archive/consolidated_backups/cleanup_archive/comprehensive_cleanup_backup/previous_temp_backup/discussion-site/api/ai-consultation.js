// Vercel Edge Function for AI Consultation API
// This provides secure API integration for the static site

export default async function handler(req, res) {
  // Enable CORS for the frontend
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  // Handle preflight requests
  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { userInput, analysisType } = req.body;

    if (!userInput || typeof userInput !== 'string') {
      return res.status(400).json({ error: 'Invalid input' });
    }

    // Validate input length
    if (userInput.length > 5000) {
      return res.status(400).json({ error: 'Input too long' });
    }

    // For now, we'll return simulated responses
    // In production, this would integrate with actual Gemini API
    const response = await simulateAIResponse(userInput, analysisType);

    return res.status(200).json({
      success: true,
      response: response,
      timestamp: new Date().toISOString()
    });

  } catch (error) {
    console.error('AI consultation error:', error);
    return res.status(500).json({ 
      error: 'Internal server error',
      message: process.env.NODE_ENV === 'development' ? error.message : 'Something went wrong'
    });
  }
}

async function simulateAIResponse(userInput, analysisType) {
  // Simulate processing delay
  await new Promise(resolve => setTimeout(resolve, 1000));

  const responses = {
    gemini: generateGeminiResponse(userInput),
    claude: generateClaudeResponse(userInput),
    final: generateFinalResponse(userInput)
  };

  return responses[analysisType] || responses.gemini;
}

function generateGeminiResponse(userInput) {
  const keywords = userInput.toLowerCase();
  
  if (keywords.includes('実験') || keywords.includes('検証')) {
    return {
      title: "実験設計の提案",
      content: `📊 **実験設計の提案**

1. **追加データセット検証**
   - COCO以外のデータセット（Open Images、Pascal VOC）での性能評価
   - 特化カテゴリ数の異なるデータセットでの比較実験

2. **統計的検証の強化**
   - より大規模なサンプルサイズでの実験
   - 交差検証による結果の安定性確認
   - 効果サイズの信頼区間の詳細分析

3. **実用性評価**
   - 処理時間とメモリ使用量の詳細測定
   - 異なるハードウェア環境での性能評価`,
      confidence: 0.92
    };
  } else if (keywords.includes('論文') || keywords.includes('投稿')) {
    return {
      title: "論文投稿戦略",
      content: `📝 **論文投稿戦略**

1. **ターゲット学会・ジャーナル**
   - IEEE Transactions on Image Processing (Impact Factor: 11.0)
   - Computer Vision and Image Understanding
   - Pattern Recognition Letters

2. **論文構成の最適化**
   - Abstract: 定量的結果を強調
   - Related Work: WordNet活用の新規性を明確化
   - Methodology: 再現性を重視した詳細記述
   - Results: 統計的有意性の詳細分析

3. **査読対応準備**
   - 比較手法の追加実装
   - アブレーション実験の実施
   - 失敗ケースの分析と改善策`,
      confidence: 0.95
    };
  } else {
    return {
      title: "総合的な研究発展提案",
      content: `🔍 **総合的な研究発展提案**

1. **技術的改善**
   - モデルの軽量化とリアルタイム処理の実現
   - 動的カテゴリ選択アルゴリズムの開発
   - 転移学習による汎用性向上

2. **評価・検証**
   - 実世界データでの性能評価
   - ユーザビリティテストの実施
   - エラー分析と改善点の特定

3. **実用化・展開**
   - Webアプリケーションのプロトタイプ開発
   - API化による外部サービス連携
   - 商用化の可能性調査`,
      confidence: 0.88
    };
  }
}

function generateClaudeResponse(userInput) {
  return {
    title: "Claude's 分析と改善提案",
    content: `🎯 **Claude's 分析と改善提案**

**Gemini提案の評価:**
✅ **強み**: 包括的なアプローチと具体的な実行項目
⚠️ **改善点**: 優先順位付けとリソース配分の最適化

**推奨する改善策:**

1. **短期集中項目（1-2ヶ月）**
   - 統計的検証の強化を最優先
   - 既存実験データの再分析
   - 信頼区間の詳細計算

2. **中期発展項目（3-6ヶ月）**
   - 新規データセットでの検証実験
   - 論文執筆と投稿準備
   - プロトタイプシステムの開発

3. **戦略的考慮事項**
   - 計算資源の効率的活用
   - 既存研究との差別化ポイントの明確化
   - 産業応用の可能性調査

**リスク評価:**
- 📊 統計的有意性: 現状で十分だが、より大規模な検証で確実性向上
- 🔧 技術的実装: 既存アーキテクチャの拡張性を活用可能
- 📝 学術的インパクト: WordNet統合アプローチの新規性は高評価期待`,
    confidence: 0.94
  };
}

function generateFinalResponse(userInput) {
  return {
    title: "統合アクションプラン",
    content: `🚀 **統合アクションプラン**

## 📋 **immediate actions (今すぐ実行)**

### 1. 統計検証強化 (Priority: 🔥 HIGH)
- [ ] 既存データの信頼区間再計算
- [ ] 効果サイズ分析の詳細化
- [ ] 交差検証結果の可視化

### 2. 追加実験設計 (Priority: 🔶 MEDIUM)
- [ ] Pascal VOCデータセットでの検証実験
- [ ] カテゴリ数8, 32での比較実験追加
- [ ] 処理時間・メモリ使用量の詳細測定

## 📈 **Next phase actions (次のフェーズ)**

### 3. 論文執筆準備 (4-6週間)
- [ ] 関連研究の最新動向調査
- [ ] 実験結果の統計的分析レポート作成
- [ ] 図表の高品質化

### 4. 実装・展開 (2-3ヶ月)
- [ ] Webアプリケーションプロトタイプ
- [ ] API設計と実装
- [ ] ユーザーテスト実施

## 🎯 **Success metrics**
- 論文投稿: 2ヶ月以内
- プロトタイプ完成: 3ヶ月以内
- 産業応用検討: 6ヶ月以内

**次回相談推奨時期:** 2週間後（統計検証完了後）`,
    confidence: 0.91
  };
}
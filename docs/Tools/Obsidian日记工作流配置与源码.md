# Obsidian 日记工作流：自动迁移与极简提问

- 目标：让每日笔记形成“连续闭环”，自动迁移昨日「明日预览」到今日 TODO，并用极简提示词生成“一针见血”的提问。
- 特点：并行请求、超时保护、零打扰使用；输出始终简洁，不写长篇解释。

## 配置要点
- 模板位置：[高级模板.md](file:///c:/Users/Frank/Documents/Obsidian%20Vault/Template/%E9%AB%98%E7%BA%A7%E6%A8%A1%E6%9D%BF.md)
- 昨日日记读取路径：Diary/日期.md（例如 [2026-01-03.md](file:///c:/Users/Frank/Documents/Obsidian%20Vault/Diary/2026-01-03.md)）
- 使用 Obsidian 原生 requestUrl 绕过 CORS
- 问题清洗：自动截取首个问句，移除多余格式与解释

## 插件设置
- Templater 配置文件：[data.json](file:///c:/Users/Frank/Documents/Obsidian%20Vault/.obsidian/plugins/templater-obsidian/data.json)
  ```json
  {
    "templates_folder": "Template",
    "trigger_on_file_creation": true,
    "auto_jump_to_cursor": false,
    "enable_folder_templates": true,
    "folder_templates": [
      { "folder": "Diary", "template": "Template/高级模板.md" }
    ]
  }
  ```
- Daily Notes 配置文件：[daily-notes.json](file:///c:/Users/Frank/Documents/Obsidian%20Vault/.obsidian/daily-notes.json)
  ```json
  {
    "folder": "Diary",
    "autorun": true,
    "template": ""
  }
  ```

## 使用流程
- 打开 Obsidian → 新建日记（位于 Diary）→ 自动执行模板
- 弹框询问“你今天最想完成的1件事是什么？”→ 自动生成今日 TODO
- 自动迁移昨日「明日预览」未完成项到今日待办
- 生成一条极简深问，仅保留“一个短问题”

## 模板源码

```javascript
<%*
// ========== 1. 全局配置 (集中管理) ==========
const CONFIG = {
    apiKey: "", // 你的API Key
    apiUrl: "",
    model: "",
    timeout: 10000, // 超时时间(毫秒)
    prompts: {
        encouragement: "请生成一句简短、独特且充满力量的每日鼓励语，对象是一位坚持自我成长的朋友。避免鸡汤，结合新奇的比喻。只输出一句话。",
        questionFallback: "请提出一个能引发自我觉察的深刻问题（关于个人成长、价值观或未来规划）。要求：1. 只输出问题本身，不要任何解释或背景铺垫。2. 问题要简短有力，一针见血。3. 语气像一个老朋友的关切询问。",
        system: "你是一个极简主义的苏格拉底式导师。你的回答必须极其简练，直击灵魂，拒绝任何废话。"
    }
};

// ========== 2. 日期与文件准备 ==========
const today = tp.date.now("YYYY-MM-DD");
const weekday = tp.date.now("dddd");
const yesterday = tp.date.now("YYYY-MM-DD", -1);
const yesterdayFile = `Diary/${yesterday}.md`;
const tomorrow = tp.date.now("YYYY-MM-DD", 1);

// ========== 3. 核心工具函数 ==========
async function callAI(prompt, systemPrompt = CONFIG.prompts.system) {
    if (!CONFIG.apiKey || CONFIG.apiKey.includes("YOUR_API_KEY")) return "请配置API Key";
    
    try {
        // 使用 Obsidian 原生 requestUrl 绕过 CORS
        const requestPromise = requestUrl({
            url: CONFIG.apiUrl,
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${CONFIG.apiKey}`
            },
            body: JSON.stringify({
                model: CONFIG.model,
                messages: [
                    { role: "system", content: systemPrompt },
                    { role: "user", content: prompt }
                ],
                temperature: 0.7,
                max_tokens: 500
            })
        });

        // 手动实现超时控制
        const timeoutPromise = new Promise((_, reject) => 
            setTimeout(() => reject(new Error("Timeout")), CONFIG.timeout)
        );

        const response = await Promise.race([requestPromise, timeoutPromise]);
        
        // requestUrl 若状态码 >= 400 会自动 throw error，这里只需处理成功情况
        const data = response.json; 
        return data.choices[0].message.content.trim();

    } catch (error) {
        console.error("AI Error:", error);
        if (error.message === "Timeout") return "[AI响应超时]";
        // 尝试解析更详细的错误
        if (error.status === 401) return "[API Key无效]";
        if (error.status === 404) return "[接口地址错误]";
        return `[AI连接失败: ${error.message || error.status}]`;
    }
}

function sanitizeQuestion(text) {
    const s = String(text || "").replace(/[*_#>`]/g, "").replace(/（.*?）/g, "").trim();
    const m = s.match(/(.{3,120}?[？?])/);
    if (m) return m[1].trim();
    const lines = s.split("\n").map(l => l.trim()).filter(Boolean);
    if (lines.length) return lines[0].replace(/^.*?：\s*/, "").replace(/^\"|\"$/g, "").trim();
    return "今天，你最需要面对的是什么？";
}
// ========== 4. 并行执行任务 (Promise.all) ==========
// 4.1 任务迁移 (本地)
let migratedTasks = "";
try {
    const prevFile = app.vault.getAbstractFileByPath(yesterdayFile);
    if (prevFile) {
        const content = await app.vault.read(prevFile);
        const match = content.match(/## 📅 明日预览\s*\n([\s\S]*?)(?=\n## |\n---|$)/);
        if (match) {
            const tasks = match[1].split('\n')
                .filter(l => l.trim().startsWith('- [ ]'))
                .map(l => l.replace(/📅 \d{4}-\d{2}-\d{2}/, '').trim());
            if (tasks.length > 0) migratedTasks = `\n` + tasks.join('\n') + `\n`;
        }
    }
} catch (e) { console.error("迁移失败", e); }

// 4.2 AI任务 (网络)
const pEncouragement = callAI(CONFIG.prompts.encouragement, "你是一位语言优美、充满创意的鼓舞者。");

let pQuestionBlock = (async () => {
    try {
        const prevFile = app.vault.getAbstractFileByPath(yesterdayFile);
        if (prevFile) {
            const content = await app.vault.read(prevFile);
            const answerMatch = content.match(/## 🤔 .*AI.*[\s\S]*?我的回答：\s*\n([\s\S]*?)(?=\n## |\n---|$)/);
            if (answerMatch && answerMatch[1].trim().length > 5) {
                const lastAnswer = answerMatch[1].trim();
                const res = await callAI(`昨天问题与回答：\n"${lastAnswer}"\n请基于此追问一个更深层的问题。要求：只输出问题本身，不要任何客套话或分析。`, "你是一个善于追问的导师。");
                const q = sanitizeQuestion(res);
                return `## 🤔 昨日AI问答与思考\n**AI反馈与追问**：${q}\n\n**我的回答**：\n`;
            }
        }
        const newQ = await callAI(CONFIG.prompts.questionFallback);
        const q = sanitizeQuestion(newQ);
        return `## 🤔 AI启发式问题\n**今日提问**：${q}\n\n**我的回答**：\n`;
    } catch (e) { return `## 🤔 AI启发式问题\n**今日提问**：(读取失败)\n\n**我的回答**：\n`; }
})();

// 等待AI结果
const [dailyEncouragement, aiQuestionBlock] = await Promise.all([pEncouragement, pQuestionBlock]);

// ========== 5. 输出内容 (Output) ==========
// 头部
tR += `> **${today}  ${weekday}** | ${dailyEncouragement}\n\n`;

// TODO部分
tR += `## 📋 今日TODO \n`;
if (migratedTasks) tR += migratedTasks;

// 交互式提问 (核心任务)
const topTask = await tp.system.prompt("你今天最想完成的1件事是什么？") || "思考人生";
tR += `- [ ] **${topTask}**（核心任务）\n`;
-%>
- [ ] 背单词 
- [ ] 

## 💡 今日思考
1. 

## 🙏 感激之事
1.  


<%- aiQuestionBlock %>

## 📅 明日预览
- [ ] 

```

## 常见问题
- 创建今天文件但未迁移：确认昨天的笔记存在于 Diary/目录且包含“## 📅 明日预览”小节，且任务以 `- [ ]` 开头。
- AI 输出太长：模板已做“问题清洗”，只保留首个问句；如仍然过长，可进一步收紧 `CONFIG.prompts`。
- 连接失败：该模板使用 `requestUrl`，避免 CORS；仍失败时检查 API Key 与 `apiUrl` 路径是否正确。

## 安全提示
- 不要在模板或文档中存放真实 API Key；建议用环境变量或在模板中以占位符形式填写后再手动替换。

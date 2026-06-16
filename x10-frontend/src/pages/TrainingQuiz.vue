<template>
  <AppLayout current-page="training-quiz" title="刷题中心" subtitle="巩固知识 · 提升能力">
    <template #actions>
      <template v-if="isAdmin && !quizMode && !showResult">
        <button @click="showUploadModal = true" class="px-4 py-2 bg-emerald-600 text-white rounded-xl text-sm hover:bg-emerald-700 transition-colors flex items-center gap-1">
          <svg class="w-4 h-4" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
          批量上传
        </button>
        <button @click="showGenerateModal = true" class="px-4 py-2 bg-purple-600 text-white rounded-xl text-sm hover:bg-purple-700 transition-colors flex items-center gap-1">
          <svg class="w-4 h-4" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v18"/><path d="M3 12h18"/><path d="m19 19-3-3"/><path d="m19 5-3 3"/><path d="M5 19l3-3"/><path d="M5 5l3 3"/></svg>
          智能出题
        </button>
      </template>
    </template>

    <div class="max-w-4xl mx-auto px-4 sm:px-6 py-8">
      <!-- ========== 管理端：单题上传表单 ========== -->
      <div v-if="isAdmin && !quizMode && !showResult && showAdminPanel" class="mb-8">
        <div class="bg-white rounded-2xl shadow-sm border border-slate-100 p-6">
          <div class="flex items-center justify-between mb-4">
            <h3 class="font-bold text-slate-800">上传新题目</h3>
            <button @click="showAdminPanel = false" class="text-sm text-slate-400 hover:text-slate-600">收起</button>
          </div>
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-1">题目内容</label>
              <textarea v-model="newQuestion.question" rows="2" placeholder="请输入题目内容..." class="w-full p-3 rounded-xl border border-slate-200 text-sm outline-none focus:border-blue-500 resize-none"></textarea>
            </div>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <div class="flex items-center justify-between mb-1">
                  <label class="text-sm font-medium text-slate-700">分类</label>
                  <button @click="showCategoryManager = true" class="text-xs text-blue-600 hover:text-blue-700">管理分类</button>
                </div>
                <select v-model="newQuestion.category" class="w-full h-10 px-3 rounded-xl border border-slate-200 text-sm outline-none focus:border-blue-500 bg-white">
                  <option v-for="cat in quizCategories" :key="cat" :value="cat">{{ cat }}</option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-medium text-slate-700 mb-1">难度</label>
                <select v-model="newQuestion.difficulty" class="w-full h-10 px-3 rounded-xl border border-slate-200 text-sm outline-none focus:border-blue-500 bg-white">
                  <option value="easy">简单</option>
                  <option value="medium">中等</option>
                  <option value="hard">困难</option>
                </select>
              </div>
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-2">选项</label>
              <div class="space-y-2">
                <div v-for="(opt, i) in newQuestion.options" :key="i" class="flex items-center gap-2">
                  <button @click="newQuestion.correct = i" :class="['w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold shrink-0 transition-colors', newQuestion.correct === i ? 'bg-emerald-600 text-white' : 'bg-slate-100 text-slate-500 hover:bg-slate-200']">
                    {{ ['A','B','C','D'][i] }}
                  </button>
                  <input v-model="newQuestion.options[i]" :placeholder="`选项 ${['A','B','C','D'][i]}`" class="flex-1 h-10 px-3 rounded-xl border border-slate-200 text-sm outline-none focus:border-blue-500" />
                </div>
              </div>
            </div>
            <div class="flex gap-3">
              <button @click="saveQuestion" :disabled="!canSaveQuestion" class="px-5 py-2.5 bg-blue-600 text-white rounded-xl text-sm hover:bg-blue-700 disabled:opacity-50">保存题目</button>
              <button @click="resetQuestionForm" class="px-4 py-2.5 border border-slate-200 text-slate-600 rounded-xl text-sm hover:bg-slate-50">重置</button>
            </div>
          </div>
        </div>
      </div>

      <!-- 管理员展开按钮 -->
      <div v-if="isAdmin && !quizMode && !showResult && !showAdminPanel" class="mb-6 text-center">
        <button @click="showAdminPanel = true" class="px-4 py-2 bg-white border border-slate-200 text-slate-600 rounded-xl text-sm hover:bg-slate-50 transition-colors">
          ➕ 上传新题目
        </button>
      </div>

      <!-- ========== 首页统计 ========== -->
      <div v-if="!quizMode && !showResult" class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
        <div class="bg-white rounded-2xl p-5 shadow-sm border border-slate-100 text-center">
          <div class="w-12 h-12 bg-blue-50 rounded-full flex items-center justify-center mx-auto mb-3">
            <svg class="w-6 h-6 text-blue-600" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
          </div>
          <p class="text-2xl font-bold text-slate-800">{{ questions.length }}</p>
          <p class="text-sm text-slate-500">题库总数</p>
        </div>
        <div class="bg-white rounded-2xl p-5 shadow-sm border border-slate-100 text-center">
          <div class="w-12 h-12 bg-emerald-50 rounded-full flex items-center justify-center mx-auto mb-3">
            <svg class="w-6 h-6 text-emerald-600" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
          </div>
          <p class="text-2xl font-bold text-slate-800">{{ myRecords.length }}</p>
          <p class="text-sm text-slate-500">累计答题</p>
        </div>
        <div class="bg-white rounded-2xl p-5 shadow-sm border border-slate-100 text-center">
          <div class="w-12 h-12 bg-amber-50 rounded-full flex items-center justify-center mx-auto mb-3">
            <svg class="w-6 h-6 text-amber-600" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"/><path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"/><path d="M4 22h16"/><path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22"/><path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22"/><path d="M18 2H6v7a6 6 0 0 0 12 0V2Z"/></svg>
          </div>
          <p class="text-2xl font-bold text-slate-800">{{ accuracy }}%</p>
          <p class="text-sm text-slate-500">正确率</p>
        </div>
      </div>

      <!-- 题目掌握情况 -->
      <div v-if="!quizMode && !showResult && questions.length > 0" class="mb-8">
        <h3 class="font-bold text-slate-800 mb-3">题目掌握情况</h3>
        <div class="bg-white rounded-2xl shadow-sm border border-slate-100 p-5">
          <div class="flex flex-wrap gap-2">
            <div v-for="(q, i) in questionStats" :key="q.id" :class="['w-8 h-8 rounded-lg flex items-center justify-center text-xs font-medium cursor-pointer transition-colors', q.lastCorrect === true ? 'bg-emerald-100 text-emerald-700' : q.lastCorrect === false ? 'bg-red-100 text-red-700' : 'bg-slate-100 text-slate-500']" :title="q.question">
              {{ i + 1 }}
            </div>
          </div>
          <div class="flex items-center gap-4 mt-3 text-xs text-slate-500">
            <span class="flex items-center gap-1"><span class="w-3 h-3 rounded bg-emerald-100"></span> 已掌握</span>
            <span class="flex items-center gap-1"><span class="w-3 h-3 rounded bg-red-100"></span> 需加强</span>
            <span class="flex items-center gap-1"><span class="w-3 h-3 rounded bg-slate-100"></span> 未答题</span>
          </div>
        </div>
      </div>

      <!-- 开始刷题按钮 -->
      <div v-if="!quizMode && !showResult" class="text-center mb-8">
        <button @click="startQuiz" :disabled="questions.length === 0" class="px-10 py-4 bg-blue-600 text-white rounded-2xl text-lg font-medium hover:bg-blue-700 shadow-lg shadow-blue-600/20 transition-all disabled:opacity-50 disabled:shadow-none">
          开始刷题
        </button>
        <p v-if="questions.length === 0" class="text-sm text-slate-400 mt-3">暂无题目，管理员请先上传题目</p>
      </div>

      <!-- ========== 答题中 ========== -->
      <div v-if="quizMode && !showResult">
        <div class="mb-4 flex items-center justify-between">
          <span class="text-sm text-slate-500">第 {{ current + 1 }} / {{ questions.length }} 题</span>
          <div class="w-32 h-2 bg-slate-100 rounded-full overflow-hidden">
            <div class="h-full bg-blue-500 rounded-full transition-all" :style="{ width: `${((current + 1) / questions.length) * 100}%` }" />
          </div>
        </div>
        <div class="bg-white rounded-2xl shadow-sm border border-slate-100 p-6">
          <div class="flex items-center gap-2 mb-4">
            <span :class="['px-2 py-0.5 rounded text-xs font-medium', questions[current].difficulty === 'easy' ? 'bg-emerald-100 text-emerald-700' : questions[current].difficulty === 'medium' ? 'bg-amber-100 text-amber-700' : 'bg-red-100 text-red-700']">
              {{ questions[current].difficulty === 'easy' ? '简单' : questions[current].difficulty === 'medium' ? '中等' : '困难' }}
            </span>
            <span class="px-2 py-0.5 bg-slate-100 rounded text-xs text-slate-600">{{ questions[current].category }}</span>
          </div>
          <h2 class="text-lg font-bold text-slate-800 mb-6">{{ questions[current].question }}</h2>
          <div class="space-y-3">
            <button v-for="(opt, i) in questions[current].options" :key="i" @click="answer(i)" :disabled="answered !== null" :class="['w-full text-left p-4 rounded-xl border-2 transition-all', answered !== null ? (i === questions[current].correct ? 'border-emerald-300 bg-emerald-50' : i === answered ? 'border-red-300 bg-red-50' : 'border-slate-100') : 'border-slate-100 hover:border-blue-300']">
              <span class="font-bold mr-2" :class="answered !== null && i === questions[current].correct ? 'text-emerald-600' : answered !== null && i === answered ? 'text-red-600' : 'text-slate-500'">{{ ['A','B','C','D'][i] }}.</span>
              {{ opt }}
            </button>
          </div>
          <div v-if="answered !== null" class="mt-6">
            <p :class="['text-sm font-medium', answered === questions[current].correct ? 'text-emerald-600' : 'text-red-600']">
              {{ answered === questions[current].correct ? '✅ 回答正确！' : `✕ 回答错误，正确答案是 ${['A','B','C','D'][questions[current].correct]}` }}
            </p>
            <p v-if="questions[current].explanation" class="text-sm text-slate-500 mt-2">💡 {{ questions[current].explanation }}</p>
            <button @click="next" class="mt-4 px-6 py-2.5 bg-blue-600 text-white rounded-xl text-sm hover:bg-blue-700">{{ current < questions.length - 1 ? '下一题' : '查看结果' }}</button>
          </div>
        </div>
      </div>

      <!-- ========== 结果页 ========== -->
      <div v-if="showResult" class="bg-white rounded-2xl shadow-sm border border-slate-100 p-8 text-center">
        <span class="text-6xl block mb-4">{{ sessionScore >= questions.length * 0.8 ? '🎉' : sessionScore >= questions.length * 0.6 ? '👍' : '💪' }}</span>
        <p class="text-3xl font-bold text-slate-800">{{ sessionScore }} / {{ sessionTotal }}</p>
        <p class="text-slate-500 mt-2">{{ sessionScore >= sessionTotal * 0.8 ? '太棒了！知识掌握很好' : sessionScore >= sessionTotal * 0.6 ? '不错，继续加油' : '继续努力，多复习几遍' }}</p>
        <div class="flex justify-center gap-3 mt-6">
          <button @click="restart" class="px-6 py-2.5 bg-blue-600 text-white rounded-xl text-sm hover:bg-blue-700">再刷一次</button>
          <button @click="showResult = false; quizMode = false" class="px-6 py-2.5 border border-slate-200 text-slate-600 rounded-xl text-sm hover:bg-slate-50">返回题库</button>
        </div>
      </div>
    </div>

    <!-- ========== 批量上传弹窗 ========== -->
    <Teleport to="body">
      <div v-if="showUploadModal" class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4" @click.self="showUploadModal = false">
        <div class="bg-white rounded-2xl shadow-xl w-full max-w-2xl max-h-[90vh] overflow-hidden flex flex-col">
          <div class="p-4 border-b border-slate-100 flex items-center justify-between">
            <h3 class="font-bold text-slate-800">批量上传题目</h3>
            <button @click="showUploadModal = false" class="w-8 h-8 flex items-center justify-center rounded-lg hover:bg-slate-100 text-slate-400">✕</button>
          </div>
          <div class="p-5 overflow-y-auto flex-1">
            <div class="bg-amber-50 border border-amber-200 rounded-xl p-3 mb-4">
              <p class="text-xs text-amber-800 font-bold mb-1">JSON 格式示例：</p>
              <pre class="text-xs text-amber-700 bg-white rounded-lg p-2 overflow-x-auto">[
  {
    "question": "客户投诉产品质量问题，以下哪项是首要处理步骤？",
    "options": ["立即道歉并记录", "转交技术部门", "要求客户提供证据", "上报管理层"],
    "correct": 0,
    "category": "客服规范",
    "difficulty": "easy",
    "explanation": "首要步骤是立即道歉并记录投诉内容"
  }
]</pre>
            </div>
            <textarea v-model="batchQuestions" rows="10" placeholder="在此粘贴 JSON 格式的题目数据..." class="w-full p-3 rounded-xl border border-slate-200 text-sm outline-none focus:border-blue-500 font-mono resize-none"></textarea>
            <div v-if="uploadResult" :class="['mt-4 p-4 rounded-xl', uploadResult.fail === 0 ? 'bg-emerald-50 border border-emerald-200' : 'bg-amber-50 border border-amber-200']">
              <p class="text-sm font-bold">上传结果：共 {{ uploadResult.total }} 题，成功 {{ uploadResult.success }} 题，失败 {{ uploadResult.fail }} 题</p>
              <div v-if="uploadResult.details.length > 0" class="text-xs text-red-600 space-y-1 mt-2 max-h-[100px] overflow-y-auto">
                <p class="font-bold">失败详情：</p>
                <p v-for="(d, i) in uploadResult.details" :key="i">{{ d }}</p>
              </div>
            </div>
          </div>
          <div class="p-4 border-t border-slate-100 flex justify-end gap-2">
            <button @click="showUploadModal = false" class="px-4 py-2 rounded-xl border border-slate-200 text-sm text-slate-600 hover:bg-slate-50">取消</button>
            <button @click="handleBatchUpload" class="px-5 py-2 bg-emerald-600 text-white rounded-xl text-sm hover:bg-emerald-700">开始上传</button>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- ========== 智能出题弹窗 ========== -->
    <Teleport to="body">
      <div v-if="showGenerateModal" class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4" @click.self="showGenerateModal = false">
        <div class="bg-white rounded-2xl shadow-xl w-full max-w-lg p-6">
          <h3 class="font-bold text-slate-800 text-lg mb-2">智能出题</h3>
          <p class="text-sm text-slate-500 mb-4">根据知识库文档内容自动生成选择题</p>
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-1">选择知识库文档</label>
              <select v-model="generateDocId" class="w-full h-10 px-3 rounded-xl border border-slate-200 text-sm outline-none focus:border-blue-500 bg-white">
                <option value="">请选择文档...</option>
                <option v-for="doc in knowledgeDocs" :key="doc.id" :value="doc.id">{{ doc.title }}</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-1">生成题目数量</label>
              <input v-model.number="generateCount" type="number" min="1" max="20" class="w-full h-10 px-3 rounded-xl border border-slate-200 text-sm outline-none focus:border-blue-500" />
            </div>
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-1">分类</label>
              <select v-model="generateCategory" class="w-full h-10 px-3 rounded-xl border border-slate-200 text-sm outline-none focus:border-blue-500 bg-white">
                <option v-for="cat in quizCategories" :key="cat" :value="cat">{{ cat }}</option>
              </select>
            </div>
          </div>
          <div class="flex justify-end gap-3 mt-6">
            <button @click="showGenerateModal = false" class="px-4 py-2 rounded-xl border border-slate-200 text-sm text-slate-600 hover:bg-slate-50">取消</button>
            <button @click="generateQuestions" :disabled="!generateDocId || generating" class="px-5 py-2 bg-purple-600 text-white rounded-xl text-sm hover:bg-purple-700 disabled:opacity-50 flex items-center gap-2">
              <span v-if="generating" class="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
              {{ generating ? '生成中...' : '生成题目' }}
            </button>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- ========== 分类管理弹窗 ========== -->
    <Teleport to="body">
      <div v-if="showCategoryManager" class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4" @click.self="showCategoryManager = false">
        <div class="bg-white rounded-2xl shadow-xl w-full max-w-md p-6">
          <h3 class="font-bold text-slate-800 text-lg mb-4">题库分类管理</h3>
          <div class="flex gap-2 mb-4">
            <input v-model="newCategoryName" placeholder="输入新分类名称" class="flex-1 h-10 px-3 rounded-xl border border-slate-200 text-sm outline-none focus:border-blue-500" />
            <button @click="addCategory" class="px-3 py-2 bg-blue-600 text-white rounded-xl text-sm hover:bg-blue-700">添加</button>
          </div>
          <div class="space-y-2 max-h-[50vh] overflow-y-auto">
            <div v-for="(cat, idx) in quizCategories" :key="idx" class="flex items-center gap-2 bg-slate-50 rounded-xl p-3">
              <template v-if="editingCategory === idx">
                <input v-model="editCategoryValue" class="flex-1 h-8 px-2 rounded-lg border border-slate-200 text-sm outline-none" />
                <button @click="saveCategoryEdit(idx)" class="text-xs text-emerald-600 hover:text-emerald-700">保存</button>
                <button @click="editingCategory = null" class="text-xs text-slate-400 hover:text-slate-600">取消</button>
              </template>
              <template v-else>
                <span class="flex-1 text-sm">{{ cat }}</span>
                <button @click="startEditCategory(idx, cat)" class="w-7 h-7 flex items-center justify-center rounded-lg hover:bg-white text-slate-400 hover:text-blue-500">✎</button>
                <button @click="deleteCategory(idx)" class="w-7 h-7 flex items-center justify-center rounded-lg hover:bg-white text-slate-400 hover:text-red-500">🗑</button>
              </template>
            </div>
          </div>
          <div class="flex justify-end mt-4">
            <button @click="showCategoryManager = false" class="px-4 py-2 rounded-xl border border-slate-200 text-sm text-slate-600 hover:bg-slate-50">关闭</button>
          </div>
        </div>
      </div>
    </Teleport>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import AppLayout from '@/layouts/AppLayout.vue'
import { useAuthStore } from '@/stores/auth'
import api from '@/api'

const authStore = useAuthStore()
const isAdmin = computed(() => authStore.isAdmin)

// ========== 题目数据 ==========
interface Question {
  id: string
  question: string
  options: string[]
  correct: number
  category: string
  difficulty: string
  explanation?: string
  source?: string
}

const questions = ref<Question[]>([])
const quizRecords = ref<any[]>([])

// 默认题目（兜底）
const defaultQuestions: Question[] = [
  { id: 'q1', question: 'BD的全称是什么？', options: ['Business Development', 'Brand Design', 'Big Data', 'Business Data'], correct: 0, category: '销售规范', difficulty: 'easy', explanation: 'BD是Business Development的缩写，即商务拓展' },
  { id: 'q2', question: '以下哪个不是抖音达人筛选的关键指标？', options: ['粉丝数量', '作品质量', '达人籍贯', '粉丝画像'], correct: 2, category: '销售规范', difficulty: 'easy' },
  { id: 'q3', question: 'GMV代表什么含义？', options: ['利润率', '商品交易总额', '投入产出比', '库存量'], correct: 1, category: '销售规范', difficulty: 'easy', explanation: 'GMV = Gross Merchandise Volume，商品交易总额' },
  { id: 'q4', question: '赵宜主每日营养包包含多少种营养素？', options: ['21种', '28种', '37种', '45种'], correct: 2, category: '产品知识', difficulty: 'easy', explanation: '科学配比37种营养素' },
  { id: 'q5', question: '赵宜主每日营养包月费是多少？', options: ['59元', '89元', '129元', '159元'], correct: 1, category: '产品知识', difficulty: 'easy', explanation: '每月只需89元，每天不到3元' },
  { id: 'q6', question: '不开票佣金比例区间是？', options: ['15%-25%', '20%-30%', '25%-35%', '30%-40%'], correct: 2, category: '公司制度', difficulty: 'medium', explanation: '不开票佣金25%-35%' },
  { id: 'q7', question: '达人筛选时粉丝量最低要求？', options: ['3000', '5000', '10000', '20000'], correct: 2, category: '销售规范', difficulty: 'medium', explanation: '粉丝量1万以上，KOC可放宽至5000' },
  { id: 'q8', question: '每日任务配额标准是多少条？', options: ['30条', '40条', '50条', '60条'], correct: 3, category: '公司制度', difficulty: 'hard', explanation: '每日任务配额标准为60条' },
]

// 分类
const quizCategories = ref(['销售规范', '技术文档', '客服规范', '公司制度', '产品知识'])

// ========== 答题状态 ==========
const quizMode = ref(false)
const showResult = ref(false)
const current = ref(0)
const answered = ref<number | null>(null)
const sessionScore = ref(0)
const sessionTotal = ref(0)

const myRecords = computed(() => quizRecords.value.filter(r => r.userId === authStore.user?.id))
const accuracy = computed(() => {
  if (myRecords.value.length === 0) return 0
  const correct = myRecords.value.filter(r => r.isCorrect).length
  return Math.round((correct / myRecords.value.length) * 100)
})
const questionStats = computed(() => questions.value.map(q => {
  const recs = myRecords.value.filter(r => r.questionId === q.id)
  return { ...q, answered: recs.length > 0, lastCorrect: recs.length > 0 ? recs[recs.length - 1].isCorrect : null }
}))

function startQuiz() {
  if (questions.value.length === 0) return
  quizMode.value = true
  showResult.value = false
  current.value = 0
  answered.value = null
  sessionScore.value = 0
  sessionTotal.value = 0
}

function answer(i: number) {
  if (answered.value !== null) return
  answered.value = i
  const q = questions.value[current.value]
  const correct = i === q.correct
  if (correct) sessionScore.value++
  sessionTotal.value++

  // 保存记录
  const record = {
    id: 'r_' + Date.now(),
    questionId: q.id,
    userId: authStore.user?.id || '',
    userName: authStore.user?.name || '',
    selectedOption: i,
    correctAnswer: q.correct,
    isCorrect: correct,
    answeredAt: new Date().toISOString()
  }
  quizRecords.value.push(record)
  saveRecords()

  // 同步到后端
  try {
    api.post('/training/quiz/records', {
      question_id: q.id,
      user_answer: ['A','B','C','D'][i],
      is_correct: correct ? 1 : 0,
      category: q.category,
    }).catch(() => {})
  } catch {}
}

function next() {
  if (current.value < questions.value.length - 1) {
    current.value++
    answered.value = null
  } else {
    showResult.value = true
    quizMode.value = false
  }
}

function restart() {
  current.value = 0
  answered.value = null
  sessionScore.value = 0
  sessionTotal.value = 0
  quizMode.value = true
  showResult.value = false
}

// ========== 管理员：单题上传 ==========
const showAdminPanel = ref(false)
const newQuestion = ref({
  question: '',
  options: ['', '', '', ''],
  correct: 0,
  category: '销售规范',
  difficulty: 'easy',
  explanation: ''
})

const canSaveQuestion = computed(() => {
  return newQuestion.value.question.trim() && newQuestion.value.options.every(o => o.trim())
})

function resetQuestionForm() {
  newQuestion.value = { question: '', options: ['', '', '', ''], correct: 0, category: quizCategories.value[0], difficulty: 'easy', explanation: '' }
}

async function saveQuestion() {
  if (!canSaveQuestion.value) return
  const q: Question = {
    id: 'q_' + Date.now(),
    question: newQuestion.value.question.trim(),
    options: newQuestion.value.options.map(o => o.trim()),
    correct: newQuestion.value.correct,
    category: newQuestion.value.category,
    difficulty: newQuestion.value.difficulty,
    explanation: newQuestion.value.explanation,
    source: '手动上传'
  }
  questions.value.push(q)
  saveQuestions()

  // 同步到后端
  try {
    await api.post('/training/quiz/questions', {
      question: q.question,
      options: q.options,
      answer: ['A','B','C','D'][q.correct],
      explanation: q.explanation,
      category: q.category,
      difficulty: q.difficulty,
    })
  } catch {}

  resetQuestionForm()
  alert('题目已保存！')
}

// ========== 批量上传 ==========
const showUploadModal = ref(false)
const batchQuestions = ref('')
const uploadResult = ref<any>(null)

function handleBatchUpload() {
  if (!batchQuestions.value.trim()) {
    alert('请输入题目数据')
    return
  }
  let parsed: any[]
  try {
    parsed = JSON.parse(batchQuestions.value)
    if (!Array.isArray(parsed)) parsed = [parsed]
  } catch (err: any) {
    alert('JSON 格式错误: ' + err.message)
    return
  }

  const valid: Question[] = []
  const errors: string[] = []
  parsed.forEach((item, idx) => {
    if (!item.question?.trim()) { errors.push(`第 ${idx+1} 题: 题目内容不能为空`); return }
    if (!Array.isArray(item.options) || item.options.length < 2) { errors.push(`第 ${idx+1} 题: 选项必须是至少包含2个元素的数组`); return }
    if (typeof item.correct !== 'number' || item.correct < 0 || item.correct >= item.options.length) { errors.push(`第 ${idx+1} 题: 正确答案索引必须在 0 到 ${item.options.length-1} 之间`); return }
    valid.push({
      id: 'q_' + Date.now() + '_' + idx,
      question: item.question.trim(),
      options: item.options.map((o: string) => String(o).trim()),
      correct: Number(item.correct),
      category: item.category || quizCategories.value[0],
      difficulty: item.difficulty || 'easy',
      explanation: item.explanation || '',
      source: '批量上传'
    })
  })

  if (errors.length > 0) {
    uploadResult.value = { total: parsed.length, success: valid.length, fail: errors.length, details: errors.slice(0, 5) }
    return
  }

  questions.value.push(...valid)
  saveQuestions()
  uploadResult.value = { total: valid.length, success: valid.length, fail: 0, details: [] }
  batchQuestions.value = ''
  alert(`成功上传 ${valid.length} 题！`)
}

// ========== 智能出题 ==========
const showGenerateModal = ref(false)
const generateDocId = ref('')
const generateCount = ref(5)
const generateCategory = ref('产品知识')
const generating = ref(false)
const knowledgeDocs = ref<any[]>([])

function generateQuestions() {
  if (!generateDocId.value) return
  generating.value = true

  // 模拟从知识库生成题目（实际可接入AI接口）
  setTimeout(() => {
    const doc = knowledgeDocs.value.find(d => d.id === generateDocId.value)
    const content = doc?.content || ''
    const sentences = content.split(/[。！？\n]/).filter((s: string) => s.trim().length > 10)

    const generated: Question[] = []
    for (let i = 0; i < Math.min(generateCount.value, sentences.length); i++) {
      const sentence = sentences[i]?.trim() || '根据知识库内容生成的题目'
      generated.push({
        id: 'q_gen_' + Date.now() + '_' + i,
        question: `关于以下内容，请选择正确描述：${sentence.slice(0, 30)}...`,
        options: ['正确', '错误', '部分正确', '无法判断'],
        correct: 0,
        category: generateCategory.value,
        difficulty: 'medium',
        explanation: sentence,
        source: '智能生成'
      })
    }

    questions.value.push(...generated)
    saveQuestions()
    generating.value = false
    showGenerateModal.value = false
    alert(`成功生成 ${generated.length} 道题目！`)
  }, 1500)
}

// ========== 分类管理 ==========
const showCategoryManager = ref(false)
const newCategoryName = ref('')
const editingCategory = ref<number | null>(null)
const editCategoryValue = ref('')

function addCategory() {
  if (!newCategoryName.value.trim()) return
  if (quizCategories.value.includes(newCategoryName.value.trim())) { alert('分类已存在'); return }
  quizCategories.value.push(newCategoryName.value.trim())
  saveCategories()
  newCategoryName.value = ''
}
function startEditCategory(idx: number, val: string) {
  editingCategory.value = idx
  editCategoryValue.value = val
}
function saveCategoryEdit(idx: number) {
  const old = quizCategories.value[idx]
  quizCategories.value[idx] = editCategoryValue.value.trim()
  // 更新所有题目的分类
  questions.value.forEach(q => { if (q.category === old) q.category = editCategoryValue.value.trim() })
  saveCategories()
  saveQuestions()
  editingCategory.value = null
}
function deleteCategory(idx: number) {
  if (!confirm('确定删除该分类？')) return
  quizCategories.value.splice(idx, 1)
  saveCategories()
}

// ========== 持久化 ==========
function saveQuestions() { localStorage.setItem('training_quiz_questions', JSON.stringify(questions.value)) }
function saveRecords() { localStorage.setItem('training_quiz_records', JSON.stringify(quizRecords.value)) }
function saveCategories() { localStorage.setItem('training_quiz_categories', JSON.stringify(quizCategories.value)) }

// ========== 初始化 ==========
onMounted(async () => {
  // 加载本地题目
  const savedQ = localStorage.getItem('training_quiz_questions')
  if (savedQ) { try { questions.value = JSON.parse(savedQ) } catch {} }
  else { questions.value = [...defaultQuestions] }

  // 加载记录
  const savedR = localStorage.getItem('training_quiz_records')
  if (savedR) { try { quizRecords.value = JSON.parse(savedR) } catch {} }

  // 加载分类
  const savedC = localStorage.getItem('training_quiz_categories')
  if (savedC) { try { quizCategories.value = JSON.parse(savedC) } catch {} }

  // 从后端加载题目
  try {
    const res = await api.get('/training/quiz/questions')
    if (res.data?.length) {
      const backend = res.data.map((q: any) => ({
        id: q.id,
        question: q.question,
        options: q.options,
        correct: ['A','B','C','D'].indexOf(q.answer),
        category: q.category,
        difficulty: q.difficulty,
        explanation: q.explanation,
      }))
      // 合并去重
      const existingIds = new Set(questions.value.map(q => q.id))
      backend.forEach((q: Question) => { if (!existingIds.has(q.id)) questions.value.push(q) })
    }
  } catch {}

  // 从后端加载答题记录
  try {
    const res = await api.get('/training/quiz/records')
    if (res.data?.length) {
      quizRecords.value = res.data.map((r: any) => ({
        id: r.id,
        questionId: r.question_id,
        userId: r.user_id,
        userName: r.user_name,
        selectedOption: ['A','B','C','D'].indexOf(r.user_answer),
        correctAnswer: r.is_correct ? 0 : 1,
        isCorrect: r.is_correct === 1,
        answeredAt: r.created_at,
      }))
    }
  } catch {}

  // 加载知识库文档（用于智能出题）
  const savedK = localStorage.getItem('training_knowledge_base')
  if (savedK) { try { knowledgeDocs.value = JSON.parse(savedK) } catch {} }
})
</script>

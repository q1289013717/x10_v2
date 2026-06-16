<template>
  <AppLayout current-page="training" title="X10成长中心" subtitle="知识库与BD自查手册">
    <template #actions>
      <button v-if="isAdmin && activeTab === 'bd-manual' && !isEditing" @click="startEdit" class="px-4 py-2 bg-blue-600 text-white rounded-xl text-sm hover:bg-blue-700 transition-colors">✏️ 编辑</button>
      <button v-if="isAdmin && activeTab === 'bd-manual' && isEditing" @click="saveEdit" class="px-4 py-2 bg-emerald-600 text-white rounded-xl text-sm hover:bg-emerald-700 transition-colors">💾 保存</button>
      <button v-if="isAdmin && activeTab === 'bd-manual' && isEditing" @click="cancelEdit" class="px-4 py-2 border border-slate-200 text-slate-600 rounded-xl text-sm hover:bg-slate-50 transition-colors">取消</button>
      <button v-if="activeTab === 'bd-manual' && !isEditing" @click="showEmployeeModal = true" class="px-4 py-2 bg-white border border-slate-200 text-slate-700 rounded-xl text-sm hover:bg-slate-50 transition-colors flex items-center gap-2">
        <svg class="w-4 h-4" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>
        查看员工手册
      </button>
    </template>

    <div class="max-w-[1600px] mx-auto px-4 sm:px-6 lg:px-8 py-6">
      <!-- Tab 导航 -->
      <div class="flex items-center justify-center mb-6">
        <div class="inline-flex bg-slate-100 rounded-xl p-1">
          <button @click="activeTab = 'knowledge'" :class="['px-6 py-2.5 rounded-lg text-sm font-medium transition-all', activeTab === 'knowledge' ? 'bg-white text-slate-800 shadow-sm' : 'text-slate-500 hover:text-slate-700']">
            <span class="mr-1">📚</span>知识库
          </button>
          <button @click="activeTab = 'bd-manual'" :class="['px-6 py-2.5 rounded-lg text-sm font-medium transition-all', activeTab === 'bd-manual' ? 'bg-[#1e3a5f] text-white shadow-sm' : 'text-slate-500 hover:text-slate-700']">
            <span class="mr-1">📋</span>BD自查手册
          </button>
          <button @click="activeTab = 'problems'" :class="['px-6 py-2.5 rounded-lg text-sm font-medium transition-all', activeTab === 'problems' ? 'bg-white text-slate-800 shadow-sm' : 'text-slate-500 hover:text-slate-700']">
            <span class="mr-1">💡</span>难题库
          </button>
          <button @click="goToQuiz" class="px-6 py-2.5 rounded-lg text-sm font-medium transition-all text-slate-500 hover:text-slate-700">
            <span class="mr-1">📝</span>刷题中心
          </button>
        </div>
      </div>

      <!-- ========== 知识库 Tab ========== -->
      <div v-if="activeTab === 'knowledge'">
        <div class="mb-4 flex items-center justify-between">
          <h2 class="text-lg font-bold text-slate-800">知识库文档</h2>
          <div class="flex items-center gap-2">
            <button v-if="isAdmin" @click="showCategoryManager = true" class="px-3 py-2 bg-white border border-slate-200 text-slate-600 rounded-xl text-sm hover:bg-slate-50">🏷 分类管理</button>
            <button v-if="isAdmin" @click="showAddKnowledge = true" class="px-4 py-2 bg-emerald-600 text-white rounded-xl text-sm hover:bg-emerald-700">➕ 新增文档</button>
          </div>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div v-for="doc in knowledgeList" :key="doc.id" class="bg-white rounded-xl p-5 shadow-sm border border-slate-100 hover:shadow-md hover:border-slate-200 transition-all cursor-pointer relative group">
            <div class="flex items-start gap-3">
              <span class="text-3xl">{{ doc.icon || '📄' }}</span>
              <div class="flex-1 min-w-0">
                <h3 class="font-medium text-slate-800 truncate">{{ doc.title }}</h3>
                <p class="text-sm text-slate-500 mt-1 line-clamp-2">{{ doc.desc || doc.content?.slice(0, 60) }}</p>
                <div class="flex items-center gap-2 mt-2 text-xs text-slate-400">
                  <span class="px-2 py-0.5 bg-slate-100 rounded">{{ doc.category }}</span>
                  <span>👁 {{ doc.views || 0 }}</span>
                </div>
              </div>
              <button v-if="isAdmin" @click.stop="deleteKnowledge(doc.id)" class="opacity-0 group-hover:opacity-100 transition-opacity w-8 h-8 flex items-center justify-center rounded-lg hover:bg-red-50 text-slate-400 hover:text-red-500 flex-shrink-0" title="删除">🗑</button>
            </div>
          </div>
        </div>
        <div v-if="knowledgeList.length === 0" class="text-center py-16 text-slate-400">
          <span class="text-5xl block mb-4">📚</span><p>暂无知识库文档</p>
        </div>
      </div>

      <!-- ========== BD自查手册 Tab ========== -->
      <div v-if="activeTab === 'bd-manual'">
        <!-- 手册标题区 -->
        <div class="flex items-center justify-between mb-4">
          <div>
            <h2 class="text-xl font-bold text-slate-800">BD自查手册</h2>
            <p class="text-sm text-slate-500 mt-1">赵宜主BD全流程SOP模板</p>
          </div>
        </div>

        <!-- 章节列表 -->
        <div class="space-y-3">
          <div v-for="(chapter, cIdx) in bdChapters" :key="chapter.id" class="bg-white rounded-xl border border-slate-200 overflow-hidden">
            <!-- 章节头部 -->
            <div @click="!isEditing && toggleChapter(chapter.id)" :class="['flex items-center gap-3 px-5 py-4 transition-colors', isEditing ? '' : 'cursor-pointer hover:bg-slate-50']">
              <span class="text-sm font-bold text-blue-600 w-8">{{ String(cIdx + 1).padStart(2, '0') }}</span>
              <!-- 编辑模式下章节标题可编辑 -->
              <template v-if="isEditing">
                <input v-model="chapter.title" @click.stop class="flex-1 h-9 px-3 rounded-lg border border-blue-200 text-sm font-semibold text-slate-800 outline-none focus:border-blue-500 bg-blue-50/50" placeholder="章节标题..." />
                <button @click.stop="toggleChapter(chapter.id)" class="text-slate-400 hover:text-slate-600 p-1 rounded" title="展开/折叠">
                  <svg :class="['w-5 h-5 transition-transform', expandedChapters.includes(chapter.id) ? 'rotate-180' : '']" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>
                </button>
              </template>
              <template v-else>
                <h3 class="font-semibold text-slate-800 flex-1">{{ chapter.title }}</h3>
                <svg :class="['w-5 h-5 text-slate-400 transition-transform', expandedChapters.includes(chapter.id) ? 'rotate-180' : '']" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>
              </template>
            </div>

            <!-- 展开内容 -->
            <div v-if="expandedChapters.includes(chapter.id)" class="px-5 pb-5 border-t border-slate-100">
              <!-- 填写提示区（蓝色高亮） -->
              <div class="mt-4 p-4 bg-blue-50 rounded-xl border border-blue-100">
                <div class="flex items-center gap-2 mb-2">
                  <span class="text-sm font-semibold text-blue-700">填写提示</span>
                </div>
                <template v-if="isEditing">
                  <textarea v-model="chapter.hint" rows="4" class="w-full p-3 rounded-xl border border-blue-200 text-sm text-blue-600 outline-none focus:border-blue-500 resize-none bg-white" placeholder="编辑本章节的填写提示..."></textarea>
                </template>
                <template v-else>
                  <pre class="text-sm text-blue-600 whitespace-pre-wrap font-sans leading-relaxed">{{ chapter.hint }}</pre>
                </template>
              </div>

              <!-- 章节内容编辑（整章） -->
              <div v-if="isEditing" class="mt-4">
                <textarea v-model="chapter.content" rows="4" class="w-full p-3 rounded-xl border border-blue-200 text-sm outline-none focus:border-blue-500 resize-none" placeholder="请填写本章整体内容..."></textarea>
              </div>
              <div v-else-if="chapter.content" class="mt-4 p-4 bg-slate-50 rounded-xl">
                <p class="text-sm text-slate-700 whitespace-pre-wrap">{{ chapter.content }}</p>
              </div>

              <!-- 小节列表 -->
              <div class="mt-4 space-y-4">
                <div v-for="(section, sIdx) in chapter.sections" :key="sIdx" class="flex gap-4">
                  <!-- 左侧内容区 -->
                  <div class="flex-1">
                    <div class="flex items-center gap-2 mb-2">
                      <span class="w-6 h-6 bg-blue-100 text-blue-600 rounded-lg flex items-center justify-center text-xs font-bold">{{ sIdx + 1 }}</span>
                      <!-- 编辑模式下标题可编辑 -->
                      <template v-if="isEditing">
                        <input v-model="section.title" class="flex-1 h-8 px-3 rounded-lg border border-blue-200 text-sm font-semibold text-slate-800 outline-none focus:border-blue-500 bg-blue-50/50" placeholder="小节标题..." />
                        <button @click="removeSection(chapter, sIdx)" class="text-red-400 hover:text-red-600 p-1 rounded" title="删除此问题">🗑</button>
                      </template>
                      <template v-else>
                        <h4 class="font-semibold text-slate-800">{{ section.title }}</h4>
                      </template>
                    </div>
                    <!-- hint 在编辑模式下也可编辑 -->
                    <template v-if="isEditing">
                      <input v-model="section.hint" class="w-full h-8 px-3 mb-1 rounded-lg border border-slate-200 text-sm text-slate-500 italic outline-none focus:border-blue-400 bg-slate-50" placeholder="填写提示（副标题）..." />
                      <input v-model="section.placeholder" class="w-full h-8 px-3 mb-2 rounded-lg border border-blue-100 text-sm text-blue-400 outline-none focus:border-blue-400 bg-blue-50/30" placeholder="输入框提示文本（如：请填写品牌核心定位...）" />
                    </template>
                    <template v-else>
                      <p class="text-sm text-slate-500 mb-2 italic">{{ section.hint }}</p>
                      <p v-if="section.placeholder" class="text-xs text-blue-400 mb-2">💬 {{ section.placeholder }}</p>
                    </template>

                    <!-- 编辑模式 -->
                    <div v-if="isEditing">
                      <textarea v-model="section.content" :placeholder="section.placeholder" rows="3" class="w-full p-3 rounded-xl border border-slate-200 text-sm outline-none focus:border-blue-500 resize-none"></textarea>
                    </div>
                    <!-- 只读模式 -->
                    <div v-else class="p-3 bg-slate-50 rounded-xl min-h-[60px]">
                      <p v-if="section.content" class="text-sm text-slate-700 whitespace-pre-wrap">{{ section.content }}</p>
                      <p v-else class="text-sm text-slate-400 italic">（暂无内容）</p>
                    </div>
                  </div>

                  <!-- 右侧用户头像 -->
                  <div class="flex-shrink-0 pt-6">
                    <div class="w-10 h-10 rounded-full bg-gradient-to-br from-blue-400 to-blue-600 flex items-center justify-center text-white text-sm font-medium shadow-sm" :title="currentUser?.name || '我'">
                      {{ (currentUser?.name || '我')[0] }}
                    </div>
                  </div>
                </div>
              </div>

              <!-- 管理员批注区 -->
              <div v-if="chapter.annotations?.length" class="mt-4 p-3 bg-amber-50 rounded-xl border border-amber-100">
                <p class="text-sm font-semibold text-amber-700 mb-2">管理员批注</p>
                <div v-for="(anno, aIdx) in chapter.annotations" :key="aIdx" class="text-sm text-amber-600 mb-1">
                  <span class="font-medium">{{ anno.author }}:</span> {{ anno.content }}
                </div>
              </div>

              <!-- 管理员添加批注按钮 -->
              <div v-if="isAdmin && !isEditing" class="mt-3">
                <button @click="openAnnotation(chapter.id)" class="text-sm text-blue-600 hover:text-blue-700 hover:bg-blue-50 px-3 py-1.5 rounded-lg transition-colors">➕ 添加批注</button>
              </div>

              <!-- 编辑模式下：添加新小节 -->
              <div v-if="isEditing" class="mt-4 border-t border-dashed border-blue-200 pt-4">
                <div class="flex items-center gap-2 mb-2">
                  <span class="text-sm font-semibold text-blue-600">➕ 添加新问题/小节</span>
                  <span class="text-xs text-slate-400">(在此章节下新增填写项)</span>
                </div>
                <div class="flex gap-2 mb-2">
                  <input v-model="newSectionTitle[chapter.id]" placeholder="小节标题..." class="flex-1 h-9 px-3 rounded-lg border border-slate-200 text-sm outline-none focus:border-blue-500" />
                  <input v-model="newSectionHint[chapter.id]" placeholder="提示文本(选填)..." class="w-48 h-9 px-3 rounded-lg border border-slate-200 text-sm outline-none focus:border-blue-500" />
                  <input v-model="newSectionPlaceholder[chapter.id]" placeholder="输入框提示(选填)..." class="w-56 h-9 px-3 rounded-lg border border-slate-200 text-sm outline-none focus:border-blue-500" />
                  <button @click="addSection(chapter)" class="px-4 h-9 bg-emerald-600 text-white rounded-lg text-sm hover:bg-emerald-700 transition-colors">添加</button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- ========== 难题库 Tab ========== -->
      <div v-if="activeTab === 'problems'">
        <div class="mb-4 flex items-center justify-between">
          <h2 class="text-lg font-bold text-slate-800">难题库</h2>
          <button @click="showAddProblem = true" class="px-4 py-2 bg-amber-600 text-white rounded-xl text-sm hover:bg-amber-700">➕ 提交难题</button>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div v-for="p in problemList" :key="p.id" class="bg-white rounded-xl p-5 shadow-sm border border-slate-100 hover:shadow-md transition-all">
            <div class="flex items-start justify-between mb-2">
              <h3 class="font-semibold text-slate-800">{{ p.title }}</h3>
              <span :class="['px-2 py-0.5 rounded-full text-xs font-medium', p.status === 'approved' ? 'bg-emerald-100 text-emerald-700' : p.status === 'rejected' ? 'bg-red-100 text-red-700' : 'bg-amber-100 text-amber-700']">
                {{ p.status === 'approved' ? '已通过' : p.status === 'rejected' ? '已驳回' : '待审核' }}
              </span>
            </div>
            <p class="text-sm text-slate-600 line-clamp-2 mb-2">{{ p.description }}</p>
            <p class="text-xs text-slate-400">👤 {{ p.author }} · {{ formatDate(p.createdAt) }}</p>
            <div v-if="isAdmin && p.status === 'pending'" class="mt-3 flex gap-2">
              <button @click="approveProblem(p.id, true)" class="px-3 py-1 bg-emerald-100 text-emerald-700 rounded-lg text-xs hover:bg-emerald-200">通过</button>
              <button @click="approveProblem(p.id, false)" class="px-3 py-1 bg-red-100 text-red-700 rounded-lg text-xs hover:bg-red-200">驳回</button>
            </div>
          </div>
        </div>
        <div v-if="problemList.length === 0" class="text-center py-16 text-slate-400">
          <span class="text-5xl block mb-4">💡</span><p>暂无难题记录</p>
        </div>
      </div>
    </div>

    <!-- ========== 弹窗 ========== -->

    <!-- 新增知识库文档弹窗 -->
    <Teleport to="body">
      <div v-if="showAddKnowledge" class="fixed inset-0 bg-black/40 z-50 flex items-center justify-center p-4" @click.self="showAddKnowledge = false">
        <div class="bg-white rounded-2xl shadow-xl w-full max-w-lg p-6 max-h-[85vh] overflow-auto">
          <h2 class="text-lg font-bold text-slate-900 mb-4">新增知识库文档</h2>
          <div class="space-y-4">
            <div><label class="block text-sm font-medium text-slate-700 mb-1">文档标题</label><input v-model="newKnowledge.title" placeholder="请输入文档标题" class="w-full h-11 px-4 rounded-xl border border-slate-200 text-sm outline-none focus:border-blue-500" /></div>
            <div><label class="block text-sm font-medium text-slate-700 mb-1">分类</label><select v-model="newKnowledge.category" class="w-full h-11 px-4 rounded-xl border border-slate-200 text-sm outline-none focus:border-blue-500 bg-white">
              <option v-for="cat in knowledgeCategories" :key="cat" :value="cat">{{ cat }}</option>
            </select></div>
            <div><label class="block text-sm font-medium text-slate-700 mb-1">内容</label><textarea v-model="newKnowledge.content" rows="6" placeholder="请输入文档内容..." class="w-full p-3 rounded-xl border border-slate-200 text-sm outline-none focus:border-blue-500 resize-none"></textarea></div>
          </div>
          <div class="flex justify-end gap-3 mt-6">
            <button @click="showAddKnowledge = false" class="px-4 py-2 rounded-xl border border-slate-200 text-sm text-slate-600 hover:bg-slate-50">取消</button>
            <button @click="addKnowledge" :disabled="!newKnowledge.title" class="px-5 py-2 bg-blue-600 text-white rounded-xl text-sm hover:bg-blue-700 disabled:opacity-50">创建</button>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- 分类管理弹窗 -->
    <Teleport to="body">
      <div v-if="showCategoryManager" class="fixed inset-0 bg-black/40 z-50 flex items-center justify-center p-4" @click.self="showCategoryManager = false">
        <div class="bg-white rounded-2xl shadow-xl w-full max-w-md p-6 max-h-[85vh] overflow-auto">
          <h2 class="text-lg font-bold text-slate-900 mb-4">分类管理</h2>
          <div class="space-y-2 mb-4">
            <div v-for="(cat, idx) in knowledgeCategories" :key="cat" class="flex items-center gap-2 p-3 bg-slate-50 rounded-xl">
              <template v-if="categoryEditIndex === idx">
                <input v-model="editingCategory" @keyup.enter="confirmEditCategory" class="flex-1 h-9 px-3 rounded-lg border border-blue-300 text-sm outline-none" />
                <button @click="confirmEditCategory" class="px-2 py-1 bg-blue-600 text-white rounded-lg text-xs">保存</button>
                <button @click="categoryEditIndex = -1; editingCategory = ''" class="px-2 py-1 text-slate-400 hover:text-slate-600 text-xs">取消</button>
              </template>
              <template v-else>
                <span class="flex-1 text-sm text-slate-700">{{ cat }}</span>
                <button @click="startEditCategory(idx)" class="text-slate-400 hover:text-blue-500 text-xs" title="编辑">✎</button>
                <button @click="deleteCategory(idx)" class="text-slate-400 hover:text-red-500 text-xs" title="删除">🗑</button>
              </template>
            </div>
          </div>
          <div class="flex items-center gap-2">
            <input v-model="newCategoryName" @keyup.enter="addCategory" placeholder="输入新分类名称..." class="flex-1 h-10 px-3 rounded-xl border border-slate-200 text-sm outline-none focus:border-blue-500" />
            <button @click="addCategory" :disabled="!newCategoryName.trim()" class="px-4 py-2 bg-blue-600 text-white rounded-xl text-sm hover:bg-blue-700 disabled:opacity-50">添加</button>
          </div>
          <div class="flex justify-end mt-4">
            <button @click="showCategoryManager = false" class="px-4 py-2 rounded-xl border border-slate-200 text-sm text-slate-600 hover:bg-slate-50">关闭</button>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- 提交难题弹窗 -->
    <Teleport to="body">
      <div v-if="showAddProblem" class="fixed inset-0 bg-black/40 z-50 flex items-center justify-center p-4" @click.self="showAddProblem = false">
        <div class="bg-white rounded-2xl shadow-xl w-full max-w-lg p-6">
          <h2 class="text-lg font-bold text-slate-900 mb-4">提交难题</h2>
          <div class="space-y-4">
            <div><label class="block text-sm font-medium text-slate-700 mb-1">难题标题 <span class="text-red-500">*</span></label><input v-model="newProblem.title" placeholder="请简要描述难题" class="w-full h-11 px-4 rounded-xl border border-slate-200 text-sm outline-none focus:border-blue-500" /></div>
            <div><label class="block text-sm font-medium text-slate-700 mb-1">问题描述 <span class="text-red-500">*</span></label><textarea v-model="newProblem.description" rows="3" placeholder="详细描述遇到的问题..." class="w-full p-3 rounded-xl border border-slate-200 text-sm outline-none focus:border-blue-500 resize-none"></textarea></div>
            <div><label class="block text-sm font-medium text-slate-700 mb-1">解决方案 <span class="text-red-500">*</span></label><textarea v-model="newProblem.solution" rows="3" placeholder="你的解决方案或思路..." class="w-full p-3 rounded-xl border border-slate-200 text-sm outline-none focus:border-blue-500 resize-none"></textarea></div>
          </div>
          <div class="flex justify-end gap-3 mt-6">
            <button @click="showAddProblem = false" class="px-4 py-2 rounded-xl border border-slate-200 text-sm text-slate-600 hover:bg-slate-50">取消</button>
            <button @click="submitProblem" :disabled="!newProblem.title || !newProblem.description || !newProblem.solution" class="px-5 py-2 bg-amber-600 text-white rounded-xl text-sm hover:bg-amber-700 disabled:opacity-50">提交</button>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- 添加批注弹窗 -->
    <Teleport to="body">
      <div v-if="showAnnotationModal" class="fixed inset-0 bg-black/40 z-50 flex items-center justify-center p-4" @click.self="showAnnotationModal = false">
        <div class="bg-white rounded-2xl shadow-xl w-full max-w-md p-6">
          <h2 class="text-lg font-bold text-slate-900 mb-4">添加批注</h2>
          <textarea v-model="newAnnotationText" rows="4" placeholder="请输入批注内容..." class="w-full p-3 rounded-xl border border-slate-200 text-sm outline-none focus:border-blue-500 resize-none"></textarea>
          <div class="flex justify-end gap-3 mt-4">
            <button @click="showAnnotationModal = false" class="px-4 py-2 rounded-xl border border-slate-200 text-sm text-slate-600 hover:bg-slate-50">取消</button>
            <button @click="addAnnotation" :disabled="!newAnnotationText.trim()" class="px-5 py-2 bg-blue-600 text-white rounded-xl text-sm hover:bg-blue-700 disabled:opacity-50">添加</button>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- 查看员工手册弹窗 -->
    <Teleport to="body">
      <div v-if="showEmployeeModal" class="fixed inset-0 bg-black/40 z-50 flex items-center justify-center p-4" @click.self="showEmployeeModal = false">
        <div class="bg-white rounded-2xl shadow-xl w-full max-w-lg p-6 max-h-[85vh] overflow-auto">
          <h2 class="text-lg font-bold text-slate-900 mb-4">选择员工查看手册</h2>
          <div v-if="employees.length === 0" class="text-center py-8 text-slate-400">
            <p>暂无员工数据</p>
          </div>
          <div v-else class="space-y-2">
            <button v-for="emp in employees" :key="emp.id" @click="viewEmployeeManual(emp)" class="w-full flex items-center gap-3 p-3 rounded-xl hover:bg-slate-50 transition-colors text-left border border-slate-100">
              <div class="w-10 h-10 rounded-full bg-gradient-to-br from-blue-400 to-blue-600 flex items-center justify-center text-white text-sm font-medium">{{ emp.name[0] }}</div>
              <div>
                <p class="font-medium text-slate-800">{{ emp.name }}</p>
                <p class="text-xs text-slate-500">{{ emp.company || emp.department || '' }}</p>
              </div>
            </button>
          </div>
          <div class="flex justify-end mt-4">
            <button @click="showEmployeeModal = false" class="px-4 py-2 rounded-xl border border-slate-200 text-sm text-slate-600 hover:bg-slate-50">关闭</button>
          </div>
        </div>
      </div>
    </Teleport>
  </AppLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import AppLayout from '@/layouts/AppLayout.vue'
import { useAuthStore } from '@/stores/auth'
import api from '@/api'

const router = useRouter()

const authStore = useAuthStore()
const currentUser = computed(() => authStore.user)
const isAdmin = computed(() => authStore.isAdmin)

const activeTab = ref('bd-manual')
const isEditing = ref(false)

function goToQuiz() {
  router.push({ name: 'training-quiz' })
}

// ========== BD自查手册数据 ==========

interface Section {
  title: string
  content: string
  placeholder: string
  hint: string
}

interface Chapter {
  id: string
  title: string
  content: string
  hint: string
  sections: Section[]
  annotations?: Array<{ id: string; content: string; author: string; createdAt: string }>
}

const bdChapters = ref<Chapter[]>([
  { id: 'c1', title: '赵宜主品牌核心信息', content: '', hint: '填写提示：\n• 品牌定位：【填写赵宜主品牌核心定位，如"专注国人体质的高性价比每日营养包"，主打为国人体质定制，科学均衡营养，分龄分性精准补充，高性价比普惠大众，每日一包省心便捷理念，面向新锐白领、资深中产人群】\n• 品牌实力：【填写赵宜主核心资质、荣誉、行业地位、核心资源等，重点填写达人关心的合作达人量级、供应链实力】\n• 核心优势（达人适配版）：【填写3-5条核心优势，每条搭配简单案例，如"售后响应快：客诉2小时内响应，降低达人沟通成本"】\n• 统一介绍口径：【100字内标准介绍，例："您好，我是赵宜主品牌达人BDXXX，我们专注XX领域，主打XX产品，佣金优厚，提供专属素材和流量扶持，诚邀合作共赢"】\n• 宣传禁用话术：【按品牌类、产品类、推广类分类填写，如极限词、涉医疗表述，例："全网最低价、根治XX问题"】', sections: [
    { title: '品牌定位', content: '', placeholder: '请填写品牌核心定位...', hint: '如：专注国人体质的高性价比每日营养包，为国人体质定制，科学均衡营养' },
    { title: '品牌实力', content: '', placeholder: '请填写品牌核心资质、荣誉、行业地位...', hint: '重点填写达人关心的合作达人量级、供应链实力' },
    { title: '核心优势（达人适配版）', content: '', placeholder: '请填写3-5条核心优势...', hint: '每条搭配简单案例，如"售后响应快：客诉2小时内响应，降低达人沟通成本"' },
    { title: '统一介绍口径', content: '', placeholder: '请填写100字内标准介绍...', hint: '例："您好，我是赵宜主品牌达人BD XXX，我们专注XX领域，主打XX产品，佣金优厚..."' },
    { title: '宣传禁用话术', content: '', placeholder: '请填写禁用话术分类列表...', hint: '按品牌类、产品类、推广类分类填写，如"全网最低价、根治XX问题"' }
  ]},
  { id: 'c2', title: '赵宜主产品体系信息', content: '', hint: '填写提示：\n• 核心合作产品线明细\n• 核心卖点（达人适配版）：【每个产品提炼2-3条适配推广的卖点，如"出片率高、易演示、复购率高"】\n• 适配达人类型：【明确每个产品适配的达人领域、粉丝量级】\n• 差异化亮点：【对比同行的独特优势，如"达人专属定制素材包、灵活佣金调整"】\n• 达人常见误区答疑：【列出3-5个常见问题+标准回答，如"误区1：供货是否稳定？回答：专属供应链，优先保障达人供货，缺货提前3天通知"】', sections: [
    { title: '核心合作产品线明细', content: '', placeholder: '请列出核心合作产品...', hint: '包含产品名称、规格、价格区间等信息' },
    { title: '核心卖点（达人适配版）', content: '', placeholder: '请填写各产品核心卖点...', hint: '每个产品提炼2-3条适配推广的卖点，如"出片率高、易演示、复购率高"' },
    { title: '适配达人类型', content: '', placeholder: '请填写适配的达人类型...', hint: '明确每个产品适配的达人领域、粉丝量级' },
    { title: '差异化亮点', content: '', placeholder: '请填写差异化优势...', hint: '对比同行的独特优势，如"达人专属定制素材包、灵活佣金调整"' },
    { title: '达人常见误区答疑', content: '', placeholder: '请列出常见问题及解答...', hint: '列出3-5个常见问题+标准回答' }
  ]},
  { id: 'c3', title: '赵宜主达人合作政策体系', content: '', hint: '填写提示：\n• 佣金体系：\n开发票：1.自然流线上45%，2.协投5%线上＋40%线下次月结算，3.代投5%线上＋40%线下次月结算\n不开发票：1.平台代开，自然流线上45%；2.不开，自然流/协投/代投公司豁免，减10%，线上5%线下30%次月结算\n• 核心合作模式：纯佣金合作（新达人、试推广）、长期合作（核心达人）\n• 达人扶持福利：基础福利（素材、流量、新品试用）、进阶福利（佣金上浮、投流支持）\n• BD权限边界：【明确可自主决策和需上报的事项】', sections: [
    { title: '开票/不开票佣金规则', content: '', placeholder: '请填写佣金规则...', hint: '开发票：1.自然流线上45%，2.协投5%线上＋40%线下次月结算，3.代投5%线上＋40%线下次月结算；不开发票：1.平台代开，自然流线上45%；2.不开，自然流/协投/代投公司豁免，减10%，线上5%线下30%次月结算' },
    { title: '合作模式', content: '', placeholder: '请填写合作模式...', hint: '纯佣金合作（新达人、试推广）、长期合作（核心达人）' },
    { title: '达人福利', content: '', placeholder: '请填写达人福利政策...', hint: '基础福利（素材、流量、新品试用）、进阶福利（佣金上浮、投流支持）' },
    { title: 'BD权限边界', content: '', placeholder: '请填写BD权限范围...', hint: '明确可自主决策和需上报的事项' }
  ]},
  { id: 'c4', title: '达人BD基础常识', content: '', hint: '填写提示：记录行业术语释义和实操知识点，便于新BD快速上手', sections: [
    { title: '行业术语释义', content: '', placeholder: '请填写行业术语解释...', hint: '如：GMV、ROI、坑位费、佣金比例等术语解释' },
    { title: '账号权重/粉丝画像/平台规则知识点', content: '', placeholder: '请填写实操知识点...', hint: '账号权重判断、粉丝画像分析、平台规则要点' }
  ]},
  { id: 'c5', title: '达人筛选标准SOP', content: '', hint: '填写提示：明确获客渠道、达人判定标准、筛选动作和考核指标', sections: [
    { title: '获客渠道', content: '', placeholder: '请填写获客渠道...', hint: '如：抖音精选联盟、小红书蒲公英、微博微任务、私域转介绍等' },
    { title: '三类达人判定', content: '', placeholder: '请填写达人判定标准...', hint: '头部达人、腰部达人、尾部达人的判定标准' },
    { title: '筛选动作', content: '', placeholder: '请填写筛选步骤...', hint: '查看作品质量、粉丝真实性、过往合作案例等' },
    { title: '日周月考核指标', content: '', placeholder: '请填写考核指标...', hint: '新增达人数量、转化率、GMV目标等' }
  ]},
  { id: 'c6', title: '达人首次触达开发SOP', content: '', hint: '填写提示：规范首次触达前的准备工作、触达渠道选择、沟通要点和跟进时效', sections: [
    { title: '事前准备', content: '', placeholder: '请填写准备工作...', hint: '研究达人账号、准备资料包、设计个性化开场白' },
    { title: '触达渠道', content: '', placeholder: '请填写触达方式...', hint: '私信、微信、邮件、电话等渠道选择' },
    { title: '沟通要点', content: '', placeholder: '请填写沟通重点...', hint: '自我介绍、品牌亮点、合作价值、下一步动作' },
    { title: '分层跟进时效', content: '', placeholder: '请填写跟进节奏...', hint: 'A/B/C类达人的不同跟进频率' }
  ]},
  { id: 'c7', title: '达人需求挖掘&意向判断SOP', content: '', hint: '填写提示：掌握挖掘达人真实需求的话术、信息登记模板和意向判定标准', sections: [
    { title: '挖需求话术', content: '', placeholder: '请填写挖需求话术...', hint: '了解达人当前困境、期望收益、合作顾虑' },
    { title: '信息登记模板', content: '', placeholder: '请填写信息登记项...', hint: '达人基本信息、粉丝画像、合作意向、特殊需求' },
    { title: '意向判定标准', content: '', placeholder: '请填写判定标准...', hint: '高意向、中意向、低意向的判断依据' }
  ]},
  { id: 'c8', title: '达人合作方案报价流程SOP', content: '', hint: '填写提示：规范方案制作、审核、发送流程和时效要求', sections: [
    { title: '方案制作', content: '', placeholder: '请填写方案内容...', hint: '合作形式、权益说明、佣金方案、预期效果' },
    { title: '审核要求', content: '', placeholder: '请填写审核流程...', hint: '内部审核节点、审批权限、修改反馈' },
    { title: '发送方式', content: '', placeholder: '请填写发送渠道...', hint: '邮件、微信、PDF附件等' },
    { title: '时效约束', content: '', placeholder: '请填写时间要求...', hint: '方案制作时效、审核时效、达人反馈时效' }
  ]},
  { id: 'c9', title: '达人谈判逼单跟进SOP', content: '', hint: '填写提示：梳理常见异议、谈判技巧、逼单节点和跟进频次', sections: [
    { title: '异议梳理', content: '', placeholder: '请填写常见异议...', hint: '佣金太低、没时间、不匹配、观望等' },
    { title: '谈判动作', content: '', placeholder: '请填写谈判策略...', hint: '价值塑造、案例举证、灵活调整' },
    { title: '逼单节点', content: '', placeholder: '请填写逼单时机...', hint: '合适的签约推进节点' },
    { title: '跟进频次', content: '', placeholder: '请填写跟进频率...', hint: '不同阶段的跟进间隔' }
  ]},
  { id: 'c10', title: '达人推广落地对接SOP', content: '', hint: '填写提示：规范素材寄送、排期核对和上线跟进流程', sections: [
    { title: '素材寄送', content: '', placeholder: '请填写寄送流程...', hint: '样品准备、物流跟踪、签收确认' },
    { title: '排期核对', content: '', placeholder: '请填写排期确认...', hint: '直播时间、短视频发布时间、预热安排' },
    { title: '上线前后跟进节点', content: '', placeholder: '请填写跟进事项...', hint: '上线前确认、直播中支持、上线后复盘' }
  ]},
  { id: 'c11', title: '达人售后维护&复购转介绍SOP', content: '', hint: '填写提示：制定回访周期、复购激励政策和转介绍话术', sections: [
    { title: '回访周期', content: '', placeholder: '请填写回访计划...', hint: '合作后3天、7天、30天回访' },
    { title: '复购激励', content: '', placeholder: '请填写激励政策...', hint: '复购佣金上浮、专属福利' },
    { title: '转介绍话术', content: '', placeholder: '请填写转介绍话术...', hint: '引导达人推荐其他达人的话术' }
  ]},
  { id: 'c12', title: 'ABC达人分层日常跟进SOP', content: '', hint: '填写提示：针对A/B/C类达人制定不同的日常跟进策略', sections: [
    { title: 'A类达人跟进策略', content: '', placeholder: '请填写A类策略...', hint: '高频互动、专属服务、优先资源' },
    { title: 'B类达人跟进策略', content: '', placeholder: '请填写B类策略...', hint: '定期维护、潜力挖掘、成长支持' },
    { title: 'C类达人跟进策略', content: '', placeholder: '请填写C类策略...', hint: '标准化触达、批量转化、基础服务' }
  ]},
  { id: 'c13', title: '四类场景破冰开场白', content: '', hint: '填写提示：针对不同场景设计有效的开场白话术', sections: [
    { title: '私信开场白', content: '', placeholder: '请填写私信话术...', hint: '简洁明了、突出价值、引发兴趣' },
    { title: '微信新增开场白', content: '', placeholder: '请填写微信话术...', hint: '友好亲切、自我介绍、说明来意' },
    { title: '转介绍开场白', content: '', placeholder: '请填写转介绍话术...', hint: '提及介绍人、建立信任、快速切入' },
    { title: '达人主动咨询开场白', content: '', placeholder: '请填写应答话术...', hint: '热情响应、了解需求、专业解答' }
  ]},
  { id: 'c14', title: '100字以内BD自我介绍标准话术', content: '', hint: '填写提示：准备标准版和精简版两套自我介绍话术', sections: [
    { title: '标准版话术', content: '', placeholder: '请填写标准版...', hint: '完整介绍品牌、职位、合作价值' },
    { title: '精简版话术', content: '', placeholder: '请填写精简版...', hint: '快速抓住重点、适合快速触达' }
  ]},
  { id: 'c15', title: '品牌简洁+详细两套讲解话术', content: '', hint: '填写提示：准备简洁版和详细版两套品牌讲解话术', sections: [
    { title: '简洁版讲解', content: '', placeholder: '请填写简洁版...', hint: '30秒内讲完核心卖点' },
    { title: '详细版讲解', content: '', placeholder: '请填写详细版...', hint: '深入介绍品牌故事、产品优势、合作政策' }
  ]},
  { id: 'c16', title: '探需求/期望/合作意向专用话术', content: '', hint: '填写提示：设计专门用于挖掘需求、了解期望、探询合作意向的话术', sections: [
    { title: '探需求话术', content: '', placeholder: '请填写探需求话术...', hint: '了解达人当前痛点、合作诉求' },
    { title: '探定期望话术', content: '', placeholder: '请填写探期望话术...', hint: '了解达人对合作的期望和目标' },
    { title: '探合作意向话术', content: '', placeholder: '请填写探意向话术...', hint: '判断达人合作意愿和时机' }
  ]},
  { id: 'c17', title: '报价、佣金解释、价值塑造话术', content: '', hint: '填写提示：准备报价、解释佣金结构和塑造合作价值的话术', sections: [
    { title: '报价话术', content: '', placeholder: '请填写报价话术...', hint: '清晰传达价格和权益' },
    { title: '佣金解释话术', content: '', placeholder: '请填写佣金解释...', hint: '详细解释佣金计算方式、结算周期' },
    { title: '价值塑造话术', content: '', placeholder: '请填写价值话术...', hint: '突出品牌优势、合作价值、成功案例' }
  ]},
  { id: 'c18', title: '邀约深聊、签约后标准话术', content: '', hint: '填写提示：设计邀约达人深入沟通和签约后的标准话术', sections: [
    { title: '邀约深聊话术', content: '', placeholder: '请填写邀约话术...', hint: '邀请达人进行正式沟通的话术' },
    { title: '签约后话术', content: '', placeholder: '请填写签约后话术...', hint: '表达感谢、确认下一步计划' }
  ]},
  { id: 'c19', title: '日常/节日/转介绍维护话术', content: '', hint: '填写提示：准备日常维护、节日祝福和转介绍的话术', sections: [
    { title: '日常维护话术', content: '', placeholder: '请填写日常维护...', hint: '保持联系、了解动态、提供支持' },
    { title: '节日维护话术', content: '', placeholder: '请填写节日祝福...', hint: '节日问候、专属福利告知' },
    { title: '转介绍维护话术', content: '', placeholder: '请填写转介绍话术...', hint: '引导达人推荐其他达人' }
  ]},
  { id: 'c20', title: '佣金偏低异议标准回复', content: '', hint: '填写提示：针对达人提出佣金偏低的异议准备标准回复', sections: [
    { title: '标准回复话术', content: '', placeholder: '请填写回复话术...', hint: '解释佣金结构、提供增值服务' },
    { title: '应对策略', content: '', placeholder: '请填写应对策略...', hint: '差异化方案、长期合作激励' }
  ]},
  { id: 'c21', title: '没时间/不匹配/观望/怕质量四类拒绝应答', content: '', hint: '填写提示：针对四种常见拒绝理由准备标准应答', sections: [
    { title: '没时间应答', content: '', placeholder: '请填写应答话术...', hint: '提供便捷方案、灵活时间安排' },
    { title: '不匹配应答', content: '', placeholder: '请填写应答话术...', hint: '寻找共同点、挖掘潜在需求' },
    { title: '观望应答', content: '', placeholder: '请填写应答话术...', hint: '提供案例、降低合作门槛' },
    { title: '怕质量应答', content: '', placeholder: '请填写应答话术...', hint: '提供产品保障、售后承诺' }
  ]},
  { id: 'c22', title: '达人投诉处理话术+流程', content: '', hint: '填写提示：制定达人投诉处理流程和标准话术', sections: [
    { title: '处理流程', content: '', placeholder: '请填写处理流程...', hint: '投诉接收、问题核实、解决方案、反馈跟进' },
    { title: '标准话术', content: '', placeholder: '请填写处理话术...', hint: '道歉话术、问题确认、解决方案告知' }
  ]},
  { id: 'c23', title: '临时毁约挽回话术+处理步骤', content: '', hint: '填写提示：制定达人临时毁约的挽回话术和处理步骤', sections: [
    { title: '挽回话术', content: '', placeholder: '请填写挽回话术...', hint: '了解原因、提供解决方案、争取保留' },
    { title: '处理步骤', content: '', placeholder: '请填写处理步骤...', hint: '紧急沟通、备选方案、后续跟进' }
  ]},
  { id: 'c24', title: '直播封号、素材审核失败应急话术', content: '', hint: '填写提示：准备直播封号和素材审核失败的应急处理话术', sections: [
    { title: '直播封号应急话术', content: '', placeholder: '请填写应急话术...', hint: '安抚达人、了解原因、协助解决' },
    { title: '素材审核失败应急话术', content: '', placeholder: '请填写应急话术...', hint: '告知原因、提供修改建议、协助重新提交' }
  ]},
  { id: 'c25', title: '产品缺货致歉补偿话术', content: '', hint: '填写提示：准备产品缺货时的致歉和补偿话术', sections: [
    { title: '致歉话术', content: '', placeholder: '请填写致歉话术...', hint: '诚恳道歉、说明原因、表达歉意' },
    { title: '补偿方案', content: '', placeholder: '请填写补偿措施...', hint: '延期补偿、赠品、佣金补偿等' }
  ]},
  { id: 'c26', title: '特殊情况处理', content: '', hint: '填写提示：记录超模碗、不开票方案、美妆达人合作等特殊情况的处理方式', sections: [
    { title: '超模碗处理', content: '', placeholder: '请填写处理方式...', hint: '超模碗活动的特殊合作政策' },
    { title: '不开票方案', content: '', placeholder: '请填写方案内容...', hint: '不开票情况下的合作方案' },
    { title: '美妆达人合作', content: '', placeholder: '请填写合作要点...', hint: '美妆类达人的特殊合作注意事项' }
  ]}
])

const expandedChapters = ref<string[]>(['c1'])
function toggleChapter(id: string) {
  if (expandedChapters.value.includes(id)) {
    expandedChapters.value = expandedChapters.value.filter(x => x !== id)
  } else {
    expandedChapters.value.push(id)
  }
}

// 加载已保存的BD手册数据
function loadBdManual() {
  const userId = currentUser.value?.id || 'default'
  const saved = localStorage.getItem(`bd_manual_${userId}`)
  if (saved) {
    try {
      const parsed = JSON.parse(saved)
      if (Array.isArray(parsed)) {
        // 合并保存的数据与模板
        bdChapters.value = bdChapters.value.map(ch => {
          const savedCh = parsed.find((c: any) => c.id === ch.id)
          if (savedCh) {
            return {
              ...ch,
              content: savedCh.content || '',
              annotations: savedCh.annotations || [],
              sections: ch.sections.map((sec, idx) => ({
                ...sec,
                content: savedCh.sections?.[idx]?.content || ''
              }))
            }
          }
          return ch
        })
      }
    } catch {}
  }
}

// ========== 添加新小节（问题） ==========
const newSectionTitle = ref<Record<string, string>>({})
const newSectionHint = ref<Record<string, string>>({})
const newSectionPlaceholder = ref<Record<string, string>>({})

function addSection(chapter: Chapter) {
  const title = newSectionTitle.value[chapter.id]?.trim()
  if (!title) { alert('请输入问题标题'); return }
  chapter.sections.push({
    title,
    content: '',
    placeholder: newSectionPlaceholder.value[chapter.id]?.trim() || '请填写...',
    hint: newSectionHint.value[chapter.id]?.trim() || ''
  })
  // 清空输入
  newSectionTitle.value[chapter.id] = ''
  newSectionHint.value[chapter.id] = ''
  newSectionPlaceholder.value[chapter.id] = ''
}

// 删除小节
function removeSection(chapter: Chapter, sIdx: number) {
  if (!confirm('确定删除此问题？')) return
  chapter.sections.splice(sIdx, 1)
}

const editSnapshot = ref<Chapter[] | null>(null)
function startEdit() {
  editSnapshot.value = JSON.parse(JSON.stringify(bdChapters.value))
  isEditing.value = true
}
function cancelEdit() {
  if (editSnapshot.value) {
    bdChapters.value = editSnapshot.value
  }
  isEditing.value = false
  editSnapshot.value = null
}
function saveEdit() {
  const userId = currentUser.value?.id || 'default'
  localStorage.setItem(`bd_manual_${userId}`, JSON.stringify(bdChapters.value))
  isEditing.value = false
  editSnapshot.value = null
  alert('保存成功！')
}

// 批注
const showAnnotationModal = ref(false)
const annotationChapterId = ref('')
const newAnnotationText = ref('')
function openAnnotation(chapterId: string) {
  annotationChapterId.value = chapterId
  newAnnotationText.value = ''
  showAnnotationModal.value = true
}
function addAnnotation() {
  const chapter = bdChapters.value.find(c => c.id === annotationChapterId.value)
  if (!chapter || !newAnnotationText.value.trim()) return
  if (!chapter.annotations) chapter.annotations = []
  chapter.annotations.push({
    id: Date.now().toString(),
    content: newAnnotationText.value.trim(),
    author: currentUser.value?.name || '管理员',
    createdAt: new Date().toISOString()
  })
  // 保存
  const userId = currentUser.value?.id || 'default'
  localStorage.setItem(`bd_manual_${userId}`, JSON.stringify(bdChapters.value))
  showAnnotationModal.value = false
}

// ========== 知识库 ==========
const knowledgeList = ref<any[]>([])
const DEFAULT_CATEGORIES = ['销售规范', '技术文档', '客服规范', '公司制度', '产品知识']
const knowledgeCategories = ref([...DEFAULT_CATEGORIES])
const showAddKnowledge = ref(false)
const newKnowledge = ref({ title: '', category: '销售规范', content: '' })

// 分类管理
const showCategoryManager = ref(false)
const editingCategory = ref('')
const newCategoryName = ref('')
const categoryEditIndex = ref(-1)

async function loadCategories() {
  try {
    const res = await api.get('/training/docs/categories', { params: { source_type: 'knowledge' } })
    if (res.data?.length) {
      knowledgeCategories.value = res.data.map((c: any) => c.name || c)
    }
  } catch {
    // 降级到 localStorage
    const saved = localStorage.getItem('training_knowledge_categories')
    if (saved) { try { knowledgeCategories.value = JSON.parse(saved) } catch {} }
  }
}
function saveCategories() {
  localStorage.setItem('training_knowledge_categories', JSON.stringify(knowledgeCategories.value))
}
function addCategory() {
  const name = newCategoryName.value.trim()
  if (!name) return
  if (knowledgeCategories.value.includes(name)) { alert('分类已存在'); return }
  knowledgeCategories.value.push(name)
  saveCategories()
  newCategoryName.value = ''
}
function startEditCategory(idx: number) {
  categoryEditIndex.value = idx
  editingCategory.value = knowledgeCategories.value[idx]
}
function confirmEditCategory() {
  const name = editingCategory.value.trim()
  if (!name) return
  if (knowledgeCategories.value.includes(name) && knowledgeCategories.value.indexOf(name) !== categoryEditIndex.value) { alert('分类已存在'); return }
  knowledgeCategories.value[categoryEditIndex.value] = name
  saveCategories()
  categoryEditIndex.value = -1
  editingCategory.value = ''
}
function deleteCategory(idx: number) {
  if (!confirm('确定删除该分类？相关文档将保留但分类变为空。')) return
  const deleted = knowledgeCategories.value[idx]
  knowledgeCategories.value.splice(idx, 1)
  // 更新已有文档的分类
  knowledgeList.value.forEach(doc => { if (doc.category === deleted) doc.category = knowledgeCategories.value[0] || '未分类' })
  saveCategories()
}

async function addKnowledge() {
  if (!newKnowledge.value.title) return
  try {
    await api.post('/training/docs', {
      title: newKnowledge.value.title,
      category: newKnowledge.value.category,
      content: newKnowledge.value.content,
      source_type: 'knowledge',
    })
    await fetchKnowledgeList()
  } catch (e: any) {
    // 降级到本地
    const doc = {
      id: 'k_' + Date.now(),
      title: newKnowledge.value.title,
      category: newKnowledge.value.category,
      content: newKnowledge.value.content,
      desc: newKnowledge.value.content?.slice(0, 60),
      icon: '📄',
      views: 0,
      author: currentUser.value?.name || '管理员',
      createdAt: new Date().toISOString()
    }
    knowledgeList.value.unshift(doc)
    localStorage.setItem('training_knowledge_base', JSON.stringify(knowledgeList.value))
    alert('后端暂不可用，已保存到本地')
  }
  showAddKnowledge.value = false
  newKnowledge.value = { title: '', category: '销售规范', content: '' }
}

async function deleteKnowledge(id: string) {
  if (!confirm('确定删除该文档？')) return
  try {
    await api.delete(`/training/docs/${id}`)
    await fetchKnowledgeList()
  } catch {
    knowledgeList.value = knowledgeList.value.filter(k => k.id !== id)
    localStorage.setItem('training_knowledge_base', JSON.stringify(knowledgeList.value))
  }
}

async function fetchKnowledgeList() {
  try {
    const res = await api.get('/training/docs', { params: { source_type: 'knowledge', limit: 200 } })
    knowledgeList.value = (res.data || []).map((d: any) => ({
      id: d.id,
      title: d.title,
      category: d.category || '未分类',
      content: d.content || '',
      desc: d.content?.slice(0, 60) || '',
      icon: '📄',
      views: d.views || 0,
      author: d.author || '',
      createdAt: d.created_at || '',
    }))
  } catch {
    const saved = localStorage.getItem('training_knowledge_base')
    if (saved) { try { knowledgeList.value = JSON.parse(saved) } catch {} }
  }
}

// ========== 难题库 ==========
const problemList = ref<any[]>([])
const showAddProblem = ref(false)
const newProblem = ref({ title: '', description: '', solution: '' })

async function submitProblem() {
  if (!newProblem.value.title || !newProblem.value.description || !newProblem.value.solution) return
  try {
    await api.post('/training/problems', {
      title: newProblem.value.title,
      description: newProblem.value.description,
      solution: newProblem.value.solution,
    })
    await fetchProblems()
  } catch {
    // 降级到本地
    const p = {
      id: 'p_' + Date.now(),
      title: newProblem.value.title,
      description: newProblem.value.description,
      solution: newProblem.value.solution,
      author: currentUser.value?.name || '未知用户',
      authorId: currentUser.value?.id,
      status: 'pending',
      createdAt: new Date().toISOString()
    }
    problemList.value.unshift(p)
    localStorage.setItem('training_problems', JSON.stringify(problemList.value))
    alert('后端暂不可用，已保存到本地')
  }
  showAddProblem.value = false
  newProblem.value = { title: '', description: '', solution: '' }
}

async function approveProblem(id: string, approve: boolean) {
  try {
    await api.put(`/training/problems/${id}/approve`, { status: approve ? 'approved' : 'rejected' })
    await fetchProblems()
  } catch {
    const p = problemList.value.find(x => x.id === id)
    if (!p) return
    p.status = approve ? 'approved' : 'rejected'
    localStorage.setItem('training_problems', JSON.stringify(problemList.value))
  }
}

async function fetchProblems() {
  try {
    const res = await api.get('/training/problems', { params: { limit: 200 } })
    problemList.value = (res.data || []).map((p: any) => ({
      id: p.id,
      title: p.title,
      description: p.description || '',
      solution: p.solution || '',
      author: p.author || p.created_by || '未知用户',
      authorId: p.created_by || '',
      status: p.status || 'pending',
      createdAt: p.created_at || '',
    }))
  } catch {
    const saved = localStorage.getItem('training_problems')
    if (saved) { try { problemList.value = JSON.parse(saved) } catch {} }
  }
}

// ========== 员工列表 ==========
const employees = ref<any[]>([])
const showEmployeeModal = ref(false)
function viewEmployeeManual(emp: any) {
  const saved = localStorage.getItem(`bd_manual_${emp.id}`)
  if (saved) {
    try {
      const parsed = JSON.parse(saved)
      if (Array.isArray(parsed)) {
        bdChapters.value = bdChapters.value.map(ch => {
          const savedCh = parsed.find((c: any) => c.id === ch.id)
          if (savedCh) {
            return {
              ...ch,
              content: savedCh.content || '',
              annotations: savedCh.annotations || [],
              sections: ch.sections.map((sec, idx) => ({
                ...sec,
                content: savedCh.sections?.[idx]?.content || ''
              }))
            }
          }
          return ch
        })
      }
    } catch {}
  } else {
    // 无保存数据，显示空模板
    bdChapters.value = bdChapters.value.map(ch => ({
      ...ch,
      content: '',
      annotations: [],
      sections: ch.sections.map(s => ({ ...s, content: '' }))
    }))
  }
  showEmployeeModal.value = false
  activeTab.value = 'bd-manual'
  alert(`已切换到「${emp.name}」的BD自查手册（只读模式）`)
}

async function fetchEmployees() {
  try {
    const res = await api.get('/auth/users')
    const users = res.data || []
    employees.value = users.filter((u: any) => u.id !== currentUser.value?.id)
  } catch {
    const savedUsers = localStorage.getItem('users')
    if (savedUsers) {
      try {
        const users = JSON.parse(savedUsers)
        employees.value = users.filter((u: any) => u.id !== currentUser.value?.id)
      } catch {}
    }
  }
}

function formatDate(d: string) {
  if (!d) return ''
  const date = new Date(d)
  return `${date.getMonth() + 1}月${date.getDate()}日`
}

// ========== 初始化 ==========
onMounted(async () => {
  loadBdManual()

  // 加载分类
  await loadCategories()

  // 加载知识库
  await fetchKnowledgeList()

  // 加载难题库
  await fetchProblems()

  // 加载员工列表
  await fetchEmployees()
})
</script>

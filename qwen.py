<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>School Register & Fee Management System</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        @import url('https://cdn.jsdelivr.net/npm/@fontsource/inter@5.0.0/index.css');
        body { font-family: 'Inter', sans-serif; }
        .fade-in { animation: fadeIn 0.3s ease-in-out; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        .slide-in { animation: slideIn 0.3s ease-out; }
        @keyframes slideIn { from { transform: translateX(-100%); } to { transform: translateX(0); } }
        .pulse-dot { animation: pulse 2s infinite; }
        @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }
        .sidebar-link.active { background: linear-gradient(135deg, #3b82f6, #2563eb); color: white; box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4); }
        .glass { background: rgba(255,255,255,0.7); backdrop-filter: blur(10px); }
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: #f1f5f9; }
        ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 3px; }
        .modal-overlay { background: rgba(0,0,0,0.5); backdrop-filter: blur(4px); }
    </style>
</head>
<body class="bg-slate-50 text-slate-800 min-h-screen flex">

    <!-- Sidebar -->
    <aside id="sidebar" class="fixed lg:static inset-y-0 left-0 z-40 w-72 bg-white border-r border-slate-200 flex flex-col transform -translate-x-full lg:translate-x-0 transition-transform duration-300">
        <div class="p-6 border-b border-slate-100">
            <div class="flex items-center gap-3">
                <img src="https://image.qwenlm.ai/public_source/04995bf8-25f8-4aed-be97-8ffc1e9a48fd/175c8cfef-ef3b-4215-9322-faef8e47d61b.png" class="w-10 h-10 rounded-lg object-cover" alt="Logo">
                <div>
                    <h1 class="font-bold text-slate-900 text-lg leading-tight">EduFinance</h1>
                    <p class="text-xs text-slate-500">School Management</p>
                </div>
            </div>
        </div>
        <nav class="flex-1 p-4 space-y-1 overflow-y-auto">
            <button onclick="switchView('dashboard')" class="sidebar-link active w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all hover:bg-slate-100" data-view="dashboard">
                <i data-lucide="layout-dashboard" class="w-5 h-5"></i> Dashboard
            </button>
            <button onclick="switchView('students')" class="sidebar-link w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium text-slate-600 transition-all hover:bg-slate-100" data-view="students">
                <i data-lucide="users" class="w-5 h-5"></i> Student Register
            </button>
            <button onclick="switchView('fees')" class="sidebar-link w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium text-slate-600 transition-all hover:bg-slate-100" data-view="fees">
                <i data-lucide="receipt" class="w-5 h-5"></i> Fee Management
            </button>
            <button onclick="switchView('payments')" class="sidebar-link w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium text-slate-600 transition-all hover:bg-slate-100" data-view="payments">
                <i data-lucide="credit-card" class="w-5 h-5"></i> Payments (Payten)
            </button>
            <button onclick="switchView('database')" class="sidebar-link w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium text-slate-600 transition-all hover:bg-slate-100" data-view="database">
                <i data-lucide="database" class="w-5 h-5"></i> PostgreSQL Sync
            </button>
        </nav>
        <div class="p-4 border-t border-slate-100">
            <div class="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl p-4">
                <div class="flex items-center gap-2 mb-2">
                    <div class="w-2 h-2 rounded-full bg-green-500 pulse-dot"></div>
                    <span class="text-xs font-semibold text-slate-700">System Status</span>
                </div>
                <p class="text-xs text-slate-600 mb-1">PostgreSQL: <span class="text-green-600 font-medium">Connected</span></p>
                <p class="text-xs text-slate-600">Payten Gateway: <span class="text-green-600 font-medium">Active</span></p>
            </div>
        </div>
    </aside>

    <!-- Main Content -->
    <div class="flex-1 flex flex-col min-h-screen lg:ml-0">
        <!-- Top Bar -->
        <header class="bg-white border-b border-slate-200 px-6 py-4 flex items-center justify-between sticky top-0 z-30">
            <div class="flex items-center gap-4">
                <button onclick="toggleSidebar()" class="lg:hidden p-2 rounded-lg hover:bg-slate-100">
                    <i data-lucide="menu" class="w-5 h-5"></i>
                </button>
                <div>
                    <h2 id="page-title" class="text-xl font-bold text-slate-900">Dashboard</h2>
                    <p class="text-sm text-slate-500">Welcome back, Administrator</p>
                </div>
            </div>
            <div class="flex items-center gap-3">
                <button class="p-2 rounded-lg hover:bg-slate-100 relative">
                    <i data-lucide="bell" class="w-5 h-5 text-slate-600"></i>
                    <span class="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
                </button>
                <div class="flex items-center gap-2 pl-3 border-l border-slate-200">
                    <div class="w-8 h-8 rounded-full bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center text-white text-sm font-bold">A</div>
                    <span class="text-sm font-medium text-slate-700 hidden sm:block">Admin</span>
                </div>
            </div>
        </header>

        <!-- Views Container -->
        <main class="flex-1 p-6 overflow-y-auto">

            <!-- Dashboard View -->
            <div id="view-dashboard" class="view fade-in space-y-6">
                <!-- Stats Cards -->
                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                    <div class="bg-white rounded-2xl p-5 border border-slate-200 hover:shadow-lg transition-shadow">
                        <div class="flex items-center justify-between mb-3">
                            <div class="w-10 h-10 rounded-xl bg-blue-100 flex items-center justify-center">
                                <i data-lucide="users" class="w-5 h-5 text-blue-600"></i>
                            </div>
                            <span class="text-xs font-medium text-green-600 bg-green-50 px-2 py-1 rounded-full">+12%</span>
                        </div>
                        <p class="text-2xl font-bold text-slate-900" id="stat-students">0</p>
                        <p class="text-sm text-slate-500">Total Students</p>
                    </div>
                    <div class="bg-white rounded-2xl p-5 border border-slate-200 hover:shadow-lg transition-shadow">
                        <div class="flex items-center justify-between mb-3">
                            <div class="w-10 h-10 rounded-xl bg-green-100 flex items-center justify-center">
                                <i data-lucide="dollar-sign" class="w-5 h-5 text-green-600"></i>
                            </div>
                            <span class="text-xs font-medium text-green-600 bg-green-50 px-2 py-1 rounded-full">+8%</span>
                        </div>
                        <p class="text-2xl font-bold text-slate-900" id="stat-collected">$0</p>
                        <p class="text-sm text-slate-500">Fees Collected</p>
                    </div>
                    <div class="bg-white rounded-2xl p-5 border border-slate-200 hover:shadow-lg transition-shadow">
                        <div class="flex items-center justify-between mb-3">
                            <div class="w-10 h-10 rounded-xl bg-amber-100 flex items-center justify-center">
                                <i data-lucide="clock" class="w-5 h-5 text-amber-600"></i>
                            </div>
                            <span class="text-xs font-medium text-red-600 bg-red-50 px-2 py-1 rounded-full">Urgent</span>
                        </div>
                        <p class="text-2xl font-bold text-slate-900" id="stat-pending">$0</p>
                        <p class="text-sm text-slate-500">Pending Fees</p>
                    </div>
                    <div class="bg-white rounded-2xl p-5 border border-slate-200 hover:shadow-lg transition-shadow">
                        <div class="flex items-center justify-between mb-3">
                            <div class="w-10 h-10 rounded-xl bg-purple-100 flex items-center justify-center">
                                <i data-lucide="database" class="w-5 h-5 text-purple-600"></i>
                            </div>
                            <span class="text-xs font-medium text-green-600 bg-green-50 px-2 py-1 rounded-full">Live</span>
                        </div>
                        <p class="text-2xl font-bold text-slate-900">14</p>
                        <p class="text-sm text-slate-500">DB Tables Synced</p>
                    </div>
                </div>

                <!-- Charts & Activity -->
                <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    <div class="lg:col-span-2 bg-white rounded-2xl p-6 border border-slate-200">
                        <div class="flex items-center justify-between mb-6">
                            <h3 class="font-bold text-slate-900">Fee Collection Overview</h3>
                            <select class="text-sm border border-slate-200 rounded-lg px-3 py-1.5 focus:outline-none focus:ring-2 focus:ring-blue-500">
                                <option>This Year</option>
                                <option>Last Year</option>
                            </select>
                        </div>
                        <div class="flex items-end justify-between h-48 gap-2" id="chart-bars">
                            <!-- Generated by JS -->
                        </div>
                        <div class="flex justify-between mt-2 text-xs text-slate-500">
                            <span>Jan</span><span>Feb</span><span>Mar</span><span>Apr</span><span>May</span><span>Jun</span><span>Jul</span><span>Aug</span><span>Sep</span><span>Oct</span><span>Nov</span><span>Dec</span>
                        </div>
                    </div>
                    <div class="bg-white rounded-2xl p-6 border border-slate-200">
                        <h3 class="font-bold text-slate-900 mb-4">Recent Activity</h3>
                        <div class="space-y-4" id="activity-list">
                            <!-- Generated by JS -->
                        </div>
                    </div>
                </div>

                <!-- Quick Actions -->
                <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
                    <button onclick="switchView('students'); showStudentForm()" class="bg-gradient-to-br from-blue-500 to-blue-600 text-white rounded-2xl p-5 text-left hover:shadow-xl transition-all hover:-translate-y-1">
                        <i data-lucide="user-plus" class="w-8 h-8 mb-3"></i>
                        <p class="font-bold text-lg">Register Student</p>
                        <p class="text-sm text-blue-100">Add new student to database</p>
                    </button>
                    <button onclick="switchView('fees'); showFeeForm()" class="bg-gradient-to-br from-emerald-500 to-emerald-600 text-white rounded-2xl p-5 text-left hover:shadow-xl transition-all hover:-translate-y-1">
                        <i data-lucide="plus-circle" class="w-8 h-8 mb-3"></i>
                        <p class="font-bold text-lg">Create Fee Type</p>
                        <p class="text-sm text-emerald-100">Define new fee structure</p>
                    </button>
                    <button onclick="switchView('payments')" class="bg-gradient-to-br from-purple-500 to-purple-600 text-white rounded-2xl p-5 text-left hover:shadow-xl transition-all hover:-translate-y-1">
                        <i data-lucide="credit-card" class="w-8 h-8 mb-3"></i>
                        <p class="font-bold text-lg">Process Payment</p>
                        <p class="text-sm text-purple-100">Via Payten Gateway</p>
                    </button>
                </div>
            </div>

            <!-- Students View -->
            <div id="view-students" class="view hidden fade-in space-y-6">
                <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                    <div class="relative flex-1 max-w-md">
                        <i data-lucide="search" class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400"></i>
                        <input type="text" id="student-search" placeholder="Search students..." class="w-full pl-10 pr-4 py-2.5 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm" oninput="renderStudents()">
                    </div>
                    <button onclick="showStudentForm()" class="bg-blue-600 text-white px-5 py-2.5 rounded-xl text-sm font-medium hover:bg-blue-700 transition-colors flex items-center gap-2">
                        <i data-lucide="plus" class="w-4 h-4"></i> Register Student
                    </button>
                </div>

                <div class="bg-white rounded-2xl border border-slate-200 overflow-hidden">
                    <div class="overflow-x-auto">
                        <table class="w-full">
                            <thead class="bg-slate-50 border-b border-slate-200">
                                <tr>
                                    <th class="text-left px-6 py-3 text-xs font-semibold text-slate-600 uppercase tracking-wider">Student</th>
                                    <th class="text-left px-6 py-3 text-xs font-semibold text-slate-600 uppercase tracking-wider">Grade</th>
                                    <th class="text-left px-6 py-3 text-xs font-semibold text-slate-600 uppercase tracking-wider">Parent Contact</th>
                                    <th class="text-left px-6 py-3 text-xs font-semibold text-slate-600 uppercase tracking-wider">Status</th>
                                    <th class="text-left px-6 py-3 text-xs font-semibold text-slate-600 uppercase tracking-wider">Actions</th>
                                </tr>
                            </thead>
                            <tbody id="students-table" class="divide-y divide-slate-100">
                                <!-- Generated by JS -->
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- Fees View -->
            <div id="view-fees" class="view hidden fade-in space-y-6">
                <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                    <h3 class="font-bold text-slate-900">Fee Structures</h3>
                    <button onclick="showFeeForm()" class="bg-emerald-600 text-white px-5 py-2.5 rounded-xl text-sm font-medium hover:bg-emerald-700 transition-colors flex items-center gap-2">
                        <i data-lucide="plus" class="w-4 h-4"></i> Create Fee Type
                    </button>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4" id="fees-grid">
                    <!-- Generated by JS -->
                </div>

                <div class="bg-white rounded-2xl border border-slate-200 p-6">
                    <h3 class="font-bold text-slate-900 mb-4">Assign Fees to Students</h3>
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <select id="assign-student" class="border border-slate-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
                            <option value="">Select Student</option>
                        </select>
                        <select id="assign-fee" class="border border-slate-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
                            <option value="">Select Fee Type</option>
                        </select>
                        <button onclick="assignFee()" class="bg-blue-600 text-white px-5 py-2.5 rounded-xl text-sm font-medium hover:bg-blue-700 transition-colors">Assign Fee</button>
                    </div>
                </div>

                <div class="bg-white rounded-2xl border border-slate-200 overflow-hidden">
                    <div class="overflow-x-auto">
                        <table class="w-full">
                            <thead class="bg-slate-50 border-b border-slate-200">
                                <tr>
                                    <th class="text-left px-6 py-3 text-xs font-semibold text-slate-600 uppercase tracking-wider">Student</th>
                                    <th class="text-left px-6 py-3 text-xs font-semibold text-slate-600 uppercase tracking-wider">Fee Type</th>
                                    <th class="text-left px-6 py-3 text-xs font-semibold text-slate-600 uppercase tracking-wider">Amount</th>
                                    <th class="text-left px-6 py-3 text-xs font-semibold text-slate-600 uppercase tracking-wider">Status</th>
                                </tr>
                            </thead>
                            <tbody id="assignments-table" class="divide-y divide-slate-100">
                                <!-- Generated by JS -->
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- Payments View -->
            <div id="view-payments" class="view hidden fade-in space-y-6">
                <div class="bg-gradient-to-r from-purple-600 to-indigo-600 rounded-2xl p-6 text-white">
                    <div class="flex items-center gap-3 mb-2">
                        <div class="w-12 h-12 bg-white/20 rounded-xl flex items-center justify-center">
                            <i data-lucide="credit-card" class="w-6 h-6"></i>
                        </div>
                        <div>
                            <h3 class="font-bold text-xl">Payten Payment Gateway</h3>
                            <p class="text-purple-100 text-sm">Secure payment processing integration</p>
                        </div>
                    </div>
                    <div class="grid grid-cols-3 gap-4 mt-6">
                        <div class="bg-white/10 rounded-xl p-3">
                            <p class="text-purple-200 text-xs">Gateway Status</p>
                            <p class="font-bold flex items-center gap-2"><span class="w-2 h-2 rounded-full bg-green-400 pulse-dot"></span> Active</p>
                        </div>
                        <div class="bg-white/10 rounded-xl p-3">
                            <p class="text-purple-200 text-xs">Today's Transactions</p>
                            <p class="font-bold" id="payten-today">0</p>
                        </div>
                        <div class="bg-white/10 rounded-xl p-3">
                            <p class="text-purple-200 text-xs">Success Rate</p>
                            <p class="font-bold">99.8%</p>
                        </div>
                    </div>
                </div>

                <div class="bg-white rounded-2xl border border-slate-200 p-6">
                    <h3 class="font-bold text-slate-900 mb-4">Process New Payment</h3>
                    <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                        <select id="pay-student" class="border border-slate-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-purple-500" onchange="updatePayFeeOptions()">
                            <option value="">Select Student</option>
                        </select>
                        <select id="pay-fee" class="border border-slate-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-purple-500">
                            <option value="">Select Pending Fee</option>
                        </select>
                        <select id="pay-method" class="border border-slate-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-purple-500">
                            <option value="card">Credit/Debit Card</option>
                            <option value="bank">Bank Transfer</option>
                            <option value="mobile">Mobile Money</option>
                        </select>
                        <button onclick="processPayment()" class="bg-purple-600 text-white px-5 py-2.5 rounded-xl text-sm font-medium hover:bg-purple-700 transition-colors flex items-center justify-center gap-2">
                            <i data-lucide="zap" class="w-4 h-4"></i> Pay via Payten
                        </button>
                    </div>
                </div>

                <div class="bg-white rounded-2xl border border-slate-200 overflow-hidden">
                    <div class="px-6 py-4 border-b border-slate-200 flex items-center justify-between">
                        <h3 class="font-bold text-slate-900">Payment History</h3>
                        <button class="text-sm text-blue-600 hover:underline flex items-center gap-1">
                            <i data-lucide="download" class="w-4 h-4"></i> Export CSV
                        </button>
                    </div>
                    <div class="overflow-x-auto">
                        <table class="w-full">
                            <thead class="bg-slate-50 border-b border-slate-200">
                                <tr>
                                    <th class="text-left px-6 py-3 text-xs font-semibold text-slate-600 uppercase tracking-wider">Ref ID</th>
                                    <th class="text-left px-6 py-3 text-xs font-semibold text-slate-600 uppercase tracking-wider">Student</th>
                                    <th class="text-left px-6 py-3 text-xs font-semibold text-slate-600 uppercase tracking-wider">Fee</th>
                                    <th class="text-left px-6 py-3 text-xs font-semibold text-slate-600 uppercase tracking-wider">Amount</th>
                                    <th class="text-left px-6 py-3 text-xs font-semibold text-slate-600 uppercase tracking-wider">Method</th>
                                    <th class="text-left px-6 py-3 text-xs font-semibold text-slate-600 uppercase tracking-wider">Date</th>
                                    <th class="text-left px-6 py-3 text-xs font-semibold text-slate-600 uppercase tracking-wider">Status</th>
                                </tr>
                            </thead>
                            <tbody id="payments-table" class="divide-y divide-slate-100">
                                <!-- Generated by JS -->
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- Database View -->
            <div id="view-database" class="view hidden fade-in space-y-6">
                <div class="bg-gradient-to-r from-slate-800 to-slate-900 rounded-2xl p-6 text-white">
                    <div class="flex items-center gap-3 mb-4">
                        <div class="w-12 h-12 bg-blue-500/20 rounded-xl flex items-center justify-center">
                            <i data-lucide="database" class="w-6 h-6 text-blue-400"></i>
                        </div>
                        <div>
                            <h3 class="font-bold text-xl">PostgreSQL Database</h3>
                            <p class="text-slate-400 text-sm">Primary data storage & synchronization</p>
                        </div>
                    </div>
                    <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                        <div class="bg-white/5 rounded-xl p-3 border border-white/10">
                            <p class="text-slate-400 text-xs">Host</p>
                            <p class="font-mono text-sm">db.edufinance.local</p>
                        </div>
                        <div class="bg-white/5 rounded-xl p-3 border border-white/10">
                            <p class="text-slate-400 text-xs">Port</p>
                            <p class="font-mono text-sm">5432</p>
                        </div>
                        <div class="bg-white/5 rounded-xl p-3 border border-white/10">
                            <p class="text-slate-400 text-xs">Database</p>
                            <p class="font-mono text-sm">school_register</p>
                        </div>
                        <div class="bg-white/5 rounded-xl p-3 border border-white/10">
                            <p class="text-slate-400 text-xs">Status</p>
                            <p class="font-bold text-green-400 flex items-center gap-2"><span class="w-2 h-2 rounded-full bg-green-400 pulse-dot"></span> Connected</p>
                        </div>
                    </div>
                </div>

                <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    <div class="bg-white rounded-2xl border border-slate-200 p-6">
                        <h3 class="font-bold text-slate-900 mb-4">Database Tables</h3>
                        <div class="space-y-2">
                            <div class="flex items-center justify-between p-3 bg-slate-50 rounded-xl">
                                <div class="flex items-center gap-3">
                                    <i data-lucide="table" class="w-4 h-4 text-blue-600"></i>
                                    <span class="text-sm font-medium">students</span>
                                </div>
                                <span class="text-xs text-slate-500" id="tbl-students">0 rows</span>
                            </div>
                            <div class="flex items-center justify-between p-3 bg-slate-50 rounded-xl">
                                <div class="flex items-center gap-3">
                                    <i data-lucide="table" class="w-4 h-4 text-emerald-600"></i>
                                    <span class="text-sm font-medium">fee_types</span>
                                </div>
                                <span class="text-xs text-slate-500" id="tbl-fees">0 rows</span>
                            </div>
                            <div class="flex items-center justify-between p-3 bg-slate-50 rounded-xl">
                                <div class="flex items-center gap-3">
                                    <i data-lucide="table" class="w-4 h-4 text-purple-600"></i>
                                    <span class="text-sm font-medium">fee_assignments</span>
                                </div>
                                <span class="text-xs text-slate-500" id="tbl-assignments">0 rows</span>
                            </div>
                            <div class="flex items-center justify-between p-3 bg-slate-50 rounded-xl">
                                <div class="flex items-center gap-3">
                                    <i data-lucide="table" class="w-4 h-4 text-amber-600"></i>
                                    <span class="text-sm font-medium">payments</span>
                                </div>
                                <span class="text-xs text-slate-500" id="tbl-payments">0 rows</span>
                            </div>
                        </div>
                    </div>
                    <div class="bg-white rounded-2xl border border-slate-200 p-6">
                        <h3 class="font-bold text-slate-900 mb-4">Sync Operations</h3>
                        <div class="space-y-3">
                            <button onclick="syncDatabase()" class="w-full flex items-center justify-between p-4 bg-blue-50 border border-blue-200 rounded-xl hover:bg-blue-100 transition-colors">
                                <div class="flex items-center gap-3">
                                    <i data-lucide="refresh-cw" class="w-5 h-5 text-blue-600"></i>
                                    <div class="text-left">
                                        <p class="text-sm font-medium text-slate-900">Full Database Sync</p>
                                        <p class="text-xs text-slate-500">Sync all tables to PostgreSQL</p>
                                    </div>
                                </div>
                                <i data-lucide="chevron-right" class="w-4 h-4 text-slate-400"></i>
                            </button>
                            <button onclick="backupDatabase()" class="w-full flex items-center justify-between p-4 bg-emerald-50 border border-emerald-200 rounded-xl hover:bg-emerald-100 transition-colors">
                                <div class="flex items-center gap-3">
                                    <i data-lucide="download-cloud" class="w-5 h-5 text-emerald-600"></i>
                                    <div class="text-left">
                                        <p class="text-sm font-medium text-slate-900">Backup Database</p>
                                        <p class="text-xs text-slate-500">Create PostgreSQL dump</p>
                                    </div>
                                </div>
                                <i data-lucide="chevron-right" class="w-4 h-4 text-slate-400"></i>
                            </button>
                            <button onclick="runQuery()" class="w-full flex items-center justify-between p-4 bg-purple-50 border border-purple-200 rounded-xl hover:bg-purple-100 transition-colors">
                                <div class="flex items-center gap-3">
                                    <i data-lucide="terminal" class="w-5 h-5 text-purple-600"></i>
                                    <div class="text-left">
                                        <p class="text-sm font-medium text-slate-900">Run SQL Query</p>
                                        <p class="text-xs text-slate-500">Execute custom PostgreSQL query</p>
                                    </div>
                                </div>
                                <i data-lucide="chevron-right" class="w-4 h-4 text-slate-400"></i>
                            </button>
                        </div>
                        <div id="sync-log" class="mt-4 bg-slate-900 rounded-xl p-4 font-mono text-xs text-green-400 h-32 overflow-y-auto">
                            <p>> System initialized...</p>
                            <p>> Connected to PostgreSQL 15.2</p>
                            <p>> Schema validated successfully</p>
                        </div>
                    </div>
                </div>
            </div>

        </main>
    </div>

    <!-- Student Form Modal -->
    <div id="student-modal" class="fixed inset-0 z-50 hidden">
        <div class="modal-overlay absolute inset-0" onclick="closeStudentForm()"></div>
        <div class="absolute right-0 top-0 h-full w-full max-w-lg bg-white shadow-2xl slide-in overflow-y-auto">
            <div class="p-6 border-b border-slate-200 flex items-center justify-between">
                <h3 class="font-bold text-lg text-slate-900">Register New Student</h3>
                <button onclick="closeStudentForm()" class="p-2 rounded-lg hover:bg-slate-100">
                    <i data-lucide="x" class="w-5 h-5"></i>
                </button>
            </div>
            <form onsubmit="saveStudent(event)" class="p-6 space-y-4">
                <div>
                    <label class="block text-sm font-medium text-slate-700 mb-1">Full Name *</label>
                    <input type="text" id="s-name" required class="w-full border border-slate-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
                </div>
                <div>
                    <label class="block text-sm font-medium text-slate-700 mb-1">Email *</label>
                    <input type="email" id="s-email" required class="w-full border border-slate-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
                </div>
                <div class="grid grid-cols-2 gap-4">
                    <div>
                        <label class="block text-sm font-medium text-slate-700 mb-1">Grade *</label>
                        <select id="s-grade" required class="w-full border border-slate-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
                            <option value="">Select</option>
                            <option>Grade 1</option><option>Grade 2</option><option>Grade 3</option>
                            <option>Grade 4</option><option>Grade 5</option><option>Grade 6</option>
                            <option>Grade 7</option><option>Grade 8</option><option>Grade 9</option>
                            <option>Grade 10</option><option>Grade 11</option><option>Grade 12</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-slate-700 mb-1">Status</label>
                        <select id="s-status" class="w-full border border-slate-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
                            <option>Active</option><option>Pending</option><option>Inactive</option>
                        </select>
                    </div>
                </div>
                <div>
                    <label class="block text-sm font-medium text-slate-700 mb-1">Parent/Guardian Name *</label>
                    <input type="text" id="s-parent" required class="w-full border border-slate-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
                </div>
                <div>
                    <label class="block text-sm font-medium text-slate-700 mb-1">Parent Phone *</label>
                    <input type="tel" id="s-phone" required class="w-full border border-slate-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
                </div>
                <div class="flex gap-3 pt-4">
                    <button type="button" onclick="closeStudentForm()" class="flex-1 border border-slate-200 text-slate-700 py-2.5 rounded-xl text-sm font-medium hover:bg-slate-50">Cancel</button>
                    <button type="submit" class="flex-1 bg-blue-600 text-white py-2.5 rounded-xl text-sm font-medium hover:bg-blue-700">Save to PostgreSQL</button>
                </div>
            </form>
        </div>
    </div>

    <!-- Fee Form Modal -->
    <div id="fee-modal" class="fixed inset-0 z-50 hidden">
        <div class="modal-overlay absolute inset-0" onclick="closeFeeForm()"></div>
        <div class="absolute right-0 top-0 h-full w-full max-w-lg bg-white shadow-2xl slide-in overflow-y-auto">
            <div class="p-6 border-b border-slate-200 flex items-center justify-between">
                <h3 class="font-bold text-lg text-slate-900">Create Fee Type</h3>
                <button onclick="closeFeeForm()" class="p-2 rounded-lg hover:bg-slate-100">
                    <i data-lucide="x" class="w-5 h-5"></i>
                </button>
            </div>
            <form onsubmit="saveFee(event)" class="p-6 space-y-4">
                <div>
                    <label class="block text-sm font-medium text-slate-700 mb-1">Fee Name *</label>
                    <input type="text" id="f-name" required class="w-full border border-slate-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500" placeholder="e.g., Tuition Fee 2024">
                </div>
                <div>
                    <label class="block text-sm font-medium text-slate-700 mb-1">Amount ($) *</label>
                    <input type="number" id="f-amount" required min="0" step="0.01" class="w-full border border-slate-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500">
                </div>
                <div>
                    <label class="block text-sm font-medium text-slate-700 mb-1">Description</label>
                    <textarea id="f-desc" rows="3" class="w-full border border-slate-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500" placeholder="Fee description..."></textarea>
                </div>
                <div>
                    <label class="block text-sm font-medium text-slate-700 mb-1">Category</label>
                    <select id="f-category" class="w-full border border-slate-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500">
                        <option>Tuition</option><option>Library</option><option>Lab</option><option>Sports</option><option>Transport</option><option>Other</option>
                    </select>
                </div>
                <div class="flex gap-3 pt-4">
                    <button type="button" onclick="closeFeeForm()" class="flex-1 border border-slate-200 text-slate-700 py-2.5 rounded-xl text-sm font-medium hover:bg-slate-50">Cancel</button>
                    <button type="submit" class="flex-1 bg-emerald-600 text-white py-2.5 rounded-xl text-sm font-medium hover:bg-emerald-700">Create Fee</button>
                </div>
            </form>
        </div>
    </div>

    <!-- Toast Notification -->
    <div id="toast" class="fixed bottom-6 right-6 z-50 hidden">
        <div class="bg-slate-900 text-white px-5 py-3 rounded-xl shadow-2xl flex items-center gap-3 fade-in">
            <i data-lucide="check-circle" class="w-5 h-5 text-green-400"></i>
            <span id="toast-msg" class="text-sm font-medium">Success</span>
        </div>
    </div>

    <script>
        // Data Store (simulating PostgreSQL)
        let data = {
            students: [
                { id: 1, name: 'Emma Johnson', email: 'emma.j@school.edu', grade: 'Grade 10', parentName: 'Robert Johnson', phone: '+1 555-0101', status: 'Active' },
                { id: 2, name: 'Liam Smith', email: 'liam.s@school.edu', grade: 'Grade 8', parentName: 'Sarah Smith', phone: '+1 555-0102', status: 'Active' },
                { id: 3, name: 'Olivia Brown', email: 'olivia.b@school.edu', grade: 'Grade 11', parentName: 'Michael Brown', phone: '+1 555-0103', status: 'Active' },
                { id: 4, name: 'Noah Davis', email: 'noah.d@school.edu', grade: 'Grade 9', parentName: 'Jennifer Davis', phone: '+1 555-0104', status: 'Pending' },
                { id: 5, name: 'Ava Wilson', email: 'ava.w@school.edu', grade: 'Grade 12', parentName: 'David Wilson', phone: '+1 555-0105', status: 'Active' }
            ],
            fees: [
                { id: 1, name: 'Tuition Fee 2024', amount: 5000, description: 'Annual tuition fee', category: 'Tuition' },
                { id: 2, name: 'Library Fee', amount: 150, description: 'Library access and resources', category: 'Library' },
                { id: 3, name: 'Lab Fee', amount: 300, description: 'Science laboratory usage', category: 'Lab' },
                { id: 4, name: 'Sports Fee', amount: 200, description: 'Sports facilities and equipment', category: 'Sports' }
            ],
            assignments: [
                { id: 1, studentId: 1, feeId: 1, status: 'Paid' },
                { id: 2, studentId: 1, feeId: 2, status: 'Pending' },
                { id: 3, studentId: 2, feeId: 1, status: 'Pending' },
                { id: 4, studentId: 3, feeId: 1, status: 'Paid' },
                { id: 5, studentId: 3, feeId: 3, status: 'Pending' },
                { id: 6, studentId: 4, feeId: 1, status: 'Pending' },
                { id: 7, studentId: 5, feeId: 1, status: 'Paid' }
            ],
            payments: [
                { id: 1, studentId: 1, feeId: 1, amount: 5000, method: 'card', date: '2024-01-15', status: 'Success', paytenRef: 'PAY-2024-001' },
                { id: 2, studentId: 3, feeId: 1, amount: 5000, method: 'bank', date: '2024-02-20', status: 'Success', paytenRef: 'PAY-2024-002' },
                { id: 3, studentId: 5, feeId: 1, amount: 5000, method: 'card', date: '2024-03-10', status: 'Success', paytenRef: 'PAY-2024-003' }
            ]
        };

        let nextIds = { students: 6, fees: 5, assignments: 8, payments: 4 };

        // View Switching
        function switchView(viewName) {
            document.querySelectorAll('.view').forEach(v => v.classList.add('hidden'));
            document.getElementById(`view-${viewName}`).classList.remove('hidden');
            document.querySelectorAll('.sidebar-link').forEach(l => {
                l.classList.remove('active');
                l.classList.add('text-slate-600');
            });
            const activeLink = document.querySelector(`[data-view="${viewName}"]`);
            if (activeLink) {
                activeLink.classList.add('active');
                activeLink.classList.remove('text-slate-600');
            }
            const titles = { dashboard: 'Dashboard', students: 'Student Register', fees: 'Fee Management', payments: 'Payments (Payten)', database: 'PostgreSQL Sync' };
            document.getElementById('page-title').textContent = titles[viewName];
            lucide.createIcons();
            renderAll();
        }

        function toggleSidebar() {
            const sb = document.getElementById('sidebar');
            sb.classList.toggle('-translate-x-full');
        }

        // Rendering
        function renderAll() {
            renderDashboard();
            renderStudents();
            renderFees();
            renderAssignments();
            renderPayments();
            updateSelects();
            updateDbStats();
        }

        function renderDashboard() {
            document.getElementById('stat-students').textContent = data.students.length;
            const collected = data.payments.filter(p => p.status === 'Success').reduce((s, p) => s + p.amount, 0);
            const totalAssigned = data.assignments.reduce((s, a) => {
                const fee = data.fees.find(f => f.id === a.feeId);
                return s + (fee ? fee.amount : 0);
            }, 0);
            const pending = totalAssigned - collected;
            document.getElementById('stat-collected').textContent = '$' + collected.toLocaleString();
            document.getElementById('stat-pending').textContent = '$' + Math.max(0, pending).toLocaleString();
            document.getElementById('payten-today').textContent = data.payments.length;

            // Chart
            const chartData = [65, 45, 78, 52, 88, 70, 42, 95, 60, 82, 55, 90];
            const maxVal = Math.max(...chartData);
            const chartContainer = document.getElementById('chart-bars');
            chartContainer.innerHTML = chartData.map((val, i) => `
                <div class="flex-1 flex flex-col items-center gap-1">
                    <div class="w-full bg-gradient-to-t from-blue-500 to-blue-400 rounded-t-lg transition-all hover:from-blue-600 hover:to-blue-500 cursor-pointer relative group" style="height: ${(val/maxVal)*100}%">
                        <div class="absolute -top-8 left-1/2 -translate-x-1/2 bg-slate-900 text-white text-xs px-2 py-1 rounded opacity-0 group-hover:opacity-100 transition-opacity">$${val}k</div>
                    </div>
                </div>
            `).join('');

            // Activity
            const activities = [
                { icon: 'user-plus', color: 'blue', text: 'New student registered', time: '2 min ago' },
                { icon: 'credit-card', color: 'purple', text: 'Payment received via Payten', time: '15 min ago' },
                { icon: 'database', color: 'emerald', text: 'Database sync completed', time: '1 hour ago' },
                { icon: 'receipt', color: 'amber', text: 'Fee structure updated', time: '3 hours ago' }
            ];
            document.getElementById('activity-list').innerHTML = activities.map(a => `
                <div class="flex items-center gap-3">
                    <div class="w-8 h-8 rounded-lg bg-${a.color}-100 flex items-center justify-center flex-shrink-0">
                        <i data-lucide="${a.icon}" class="w-4 h-4 text-${a.color}-600"></i>
                    </div>
                    <div class="flex-1 min-w-0">
                        <p class="text-sm font-medium text-slate-900 truncate">${a.text}</p>
                        <p class="text-xs text-slate-500">${a.time}</p>
                    </div>
                </div>
            `).join('');
        }

        function renderStudents() {
            const search = (document.getElementById('student-search')?.value || '').toLowerCase();
            const filtered = data.students.filter(s => s.name.toLowerCase().includes(search) || s.grade.toLowerCase().includes(search));
            document.getElementById('students-table').innerHTML = filtered.map(s => `
                <tr class="hover:bg-slate-50 transition-colors">
                    <td class="px-6 py-4">
                        <div class="flex items-center gap-3">
                            <div class="w-9 h-9 rounded-full bg-gradient-to-br from-blue-400 to-indigo-500 flex items-center justify-center text-white text-sm font-bold">${s.name.charAt(0)}</div>
                            <div>
                                <p class="font-medium text-slate-900 text-sm">${s.name}</p>
                                <p class="text-xs text-slate-500">${s.email}</p>
                            </div>
                        </div>
                    </td>
                    <td class="px-6 py-4 text-sm text-slate-600">${s.grade}</td>
                    <td class="px-6 py-4">
                        <p class="text-sm text-slate-900">${s.parentName}</p>
                        <p class="text-xs text-slate-500">${s.phone}</p>
                    </td>
                    <td class="px-6 py-4">
                        <span class="px-2.5 py-1 rounded-full text-xs font-medium ${s.status === 'Active' ? 'bg-green-100 text-green-700' : s.status === 'Pending' ? 'bg-amber-100 text-amber-700' : 'bg-slate-100 text-slate-700'}">${s.status}</span>
                    </td>
                    <td class="px-6 py-4">
                        <button onclick="deleteStudent(${s.id})" class="p-1.5 rounded-lg hover:bg-red-50 text-red-500 transition-colors">
                            <i data-lucide="trash-2" class="w-4 h-4"></i>
                        </button>
                    </td>
                </tr>
            `).join('');
        }

        function renderFees() {
            const colors = { Tuition: 'blue', Library: 'emerald', Lab: 'purple', Sports: 'amber', Transport: 'pink', Other: 'slate' };
            document.getElementById('fees-grid').innerHTML = data.fees.map(f => `
                <div class="bg-white rounded-2xl border border-slate-200 p-5 hover:shadow-lg transition-all hover:-translate-y-1">
                    <div class="flex items-center justify-between mb-3">
                        <div class="w-10 h-10 rounded-xl bg-${colors[f.category] || 'blue'}-100 flex items-center justify-center">
                            <i data-lucide="receipt" class="w-5 h-5 text-${colors[f.category] || 'blue'}-600"></i>
                        </div>
                        <span class="text-xs font-medium text-slate-500 bg-slate-100 px-2 py-1 rounded-full">${f.category}</span>
                    </div>
                    <h4 class="font-bold text-slate-900 mb-1">${f.name}</h4>
                    <p class="text-xs text-slate-500 mb-3 line-clamp-2">${f.description}</p>
                    <div class="flex items-center justify-between pt-3 border-t border-slate-100">
                        <span class="text-xl font-bold text-slate-900">$${f.amount.toLocaleString()}</span>
                        <button onclick="deleteFee(${f.id})" class="p-1.5 rounded-lg hover:bg-red-50 text-red-500">
                            <i data-lucide="trash-2" class="w-4 h-4"></i>
                        </button>
                    </div>
                </div>
            `).join('');
        }

        function renderAssignments() {
            document.getElementById('assignments-table').innerHTML = data.assignments.map(a => {
                const s = data.students.find(st => st.id === a.studentId);
                const f = data.fees.find(fe => fe.id === a.feeId);
                if (!s || !f) return '';
                return `
                    <tr class="hover:bg-slate-50">
                        <td class="px-6 py-4 text-sm font-medium text-slate-900">${s.name}</td>
                        <td class="px-6 py-4 text-sm text-slate-600">${f.name}</td>
                        <td class="px-6 py-4 text-sm font-semibold text-slate-900">$${f.amount.toLocaleString()}</td>
                        <td class="px-6 py-4">
                            <span class="px-2.5 py-1 rounded-full text-xs font-medium ${a.status === 'Paid' ? 'bg-green-100 text-green-700' : 'bg-amber-100 text-amber-700'}">${a.status}</span>
                        </td>
                    </tr>
                `;
            }).join('');
        }

        function renderPayments() {
            document.getElementById('payments-table').innerHTML = data.payments.map(p => {
                const s = data.students.find(st => st.id === p.studentId);
                const f = data.fees.find(fe => fe.id === p.feeId);
                const methodIcons = { card: 'credit-card', bank: 'landmark', mobile: 'smartphone' };
                return `
                    <tr class="hover:bg-slate-50">
                        <td class="px-6 py-4 text-sm font-mono text-slate-600">${p.paytenRef}</td>
                        <td class="px-6 py-4 text-sm font-medium text-slate-900">${s?.name || 'Unknown'}</td>
                        <td class="px-6 py-4 text-sm text-slate-600">${f?.name || 'Unknown'}</td>
                        <td class="px-6 py-4 text-sm font-bold text-slate-900">$${p.amount.toLocaleString()}</td>
                        <td class="px-6 py-4 text-sm text-slate-600 capitalize flex items-center gap-1.5">
                            <i data-lucide="${methodIcons[p.method]}" class="w-3.5 h-3.5"></i> ${p.method}
                        </td>
                        <td class="px-6 py-4 text-sm text-slate-600">${p.date}</td>
                        <td class="px-6 py-4">
                            <span class="px-2.5 py-1 rounded-full text-xs font-medium bg-green-100 text-green-700">${p.status}</span>
                        </td>
                    </tr>
                `;
            }).join('');
        }

        function updateSelects() {
            const studentOpts = data.students.map(s => `<option value="${s.id}">${s.name} - ${s.grade}</option>`).join('');
            const feeOpts = data.fees.map(f => `<option value="${f.id}">${f.name} ($${f.amount})</option>`).join('');
            ['assign-student', 'pay-student'].forEach(id => {
                const el = document.getElementById(id);
                if (el) el.innerHTML = `<option value="">Select Student</option>` + studentOpts;
            });
            const assignFeeEl = document.getElementById('assign-fee');
            if (assignFeeEl) assignFeeEl.innerHTML = `<option value="">Select Fee Type</option>` + feeOpts;
        }

        function updatePayFeeOptions() {
            const studentId = parseInt(document.getElementById('pay-student').value);
            const feeSelect = document.getElementById('pay-fee');
            if (!studentId) {
                feeSelect.innerHTML = '<option value="">Select Pending Fee</option>';
                return;
            }
            const pendingAssignments = data.assignments.filter(a => a.studentId === studentId && a.status === 'Pending');
            feeSelect.innerHTML = '<option value="">Select Pending Fee</option>' + pendingAssignments.map(a => {
                const f = data.fees.find(fe => fe.id === a.feeId);
                return f ? `<option value="${a.id}">${f.name} - $${f.amount}</option>` : '';
            }).join('');
        }

        function updateDbStats() {
            document.getElementById('tbl-students').textContent = data.students.length + ' rows';
            document.getElementById('tbl-fees').textContent = data.fees.length + ' rows';
            document.getElementById('tbl-assignments').textContent = data.assignments.length + ' rows';
            document.getElementById('tbl-payments').textContent = data.payments.length + ' rows';
        }

        // Student Form
        function showStudentForm() { document.getElementById('student-modal').classList.remove('hidden'); }
        function closeStudentForm() { document.getElementById('student-modal').classList.add('hidden'); }
        function saveStudent(e) {
            e.preventDefault();
            const student = {
                id: nextIds.students++,
                name: document.getElementById('s-name').value,
                email: document.getElementById('s-email').value,
                grade: document.getElementById('s-grade').value,
                parentName: document.getElementById('s-parent').value,
                phone: document.getElementById('s-phone').value,
                status: document.getElementById('s-status').value
            };
            data.students.push(student);
            closeStudentForm();
            e.target.reset();
            renderAll();
            showToast('Student registered & saved to PostgreSQL');
            addLog(`> INSERT INTO students VALUES (${student.id}, '${student.name}', ...)`);
        }
        function deleteStudent(id) {
            if (confirm('Delete this student record from PostgreSQL?')) {
                data.students = data.students.filter(s => s.id !== id);
                renderAll();
                showToast('Student deleted from database');
                addLog(`> DELETE FROM students WHERE id = ${id}`);
            }
        }

        // Fee Form
        function showFeeForm() { document.getElementById('fee-modal').classList.remove('hidden'); }
        function closeFeeForm() { document.getElementById('fee-modal').classList.add('hidden'); }
        function saveFee(e) {
            e.preventDefault();
            const fee = {
                id: nextIds.fees++,
                name: document.getElementById('f-name').value,
                amount: parseFloat(document.getElementById('f-amount').value),
                description: document.getElementById('f-desc').value,
                category: document.getElementById('f-category').value
            };
            data.fees.push(fee);
            closeFeeForm();
            e.target.reset();
            renderAll();
            showToast('Fee type created successfully');
            addLog(`> INSERT INTO fee_types VALUES (${fee.id}, '${fee.name}', ${fee.amount})`);
        }
        function deleteFee(id) {
            if (confirm('Delete this fee type?')) {
                data.fees = data.fees.filter(f => f.id !== id);
                renderAll();
                showToast('Fee type deleted');
            }
        }

        // Assign Fee
        function assignFee() {
            const studentId = parseInt(document.getElementById('assign-student').value);
            const feeId = parseInt(document.getElementById('assign-fee').value);
            if (!studentId || !feeId) { showToast('Please select student and fee', true); return; }
            const exists = data.assignments.find(a => a.studentId === studentId && a.feeId === feeId);
            if (exists) { showToast('Fee already assigned', true); return; }
            data.assignments.push({ id: nextIds.assignments++, studentId, feeId, status: 'Pending' });
            renderAll();
            showToast('Fee assigned to student');
            addLog(`> INSERT INTO fee_assignments (student_id, fee_id) VALUES (${studentId}, ${feeId})`);
        }

        // Payment Processing (Payten)
        function processPayment() {
            const studentId = parseInt(document.getElementById('pay-student').value);
            const assignmentId = parseInt(document.getElementById('pay-fee').value);
            const method = document.getElementById('pay-method').value;
            if (!studentId || !assignmentId) { showToast('Please select student and fee', true); return; }

            const assignment = data.assignments.find(a => a.id === assignmentId);
            const fee = data.fees.find(f => f.id === assignment.feeId);
            const student = data.students.find(s => s.id === studentId);

            // Simulate Payten processing
            showToast('Processing payment via Payten Gateway...');
            setTimeout(() => {
                const ref = 'PAY-' + new Date().getFullYear() + '-' + String(nextIds.payments).padStart(3, '0');
                const payment = {
                    id: nextIds.payments++,
                    studentId,
                    feeId: assignment.feeId,
                    amount: fee.amount,
                    method,
                    date: new Date().toISOString().split('T')[0],
                    status: 'Success',
                    paytenRef: ref
                };
                data.payments.push(payment);
                assignment.status = 'Paid';
                renderAll();
                showToast(`Payment successful! Ref: ${ref}`);
                addLog(`> Payten Gateway: Transaction ${ref} approved`);
                addLog(`> INSERT INTO payments VALUES (${payment.id}, ${studentId}, ${fee.amount}, '${ref}')`);
            }, 1500);
        }

        // Database Operations
        function syncDatabase() {
            showToast('Syncing all tables to PostgreSQL...');
            addLog('> BEGIN TRANSACTION;');
            addLog('> Syncing students table... ' + data.students.length + ' rows');
            addLog('> Syncing fee_types table... ' + data.fees.length + ' rows');
            addLog('> Syncing fee_assignments table... ' + data.assignments.length + ' rows');
            addLog('> Syncing payments table... ' + data.payments.length + ' rows');
            addLog('> COMMIT; All tables synced successfully');
            setTimeout(() => showToast('Database sync completed'), 1000);
        }
        function backupDatabase() {
            showToast('Creating PostgreSQL backup...');
            addLog('> pg_dump school_register > backup_' + new Date().toISOString().split('T')[0] + '.sql');
            addLog('> Backup completed: 2.4 MB');
            setTimeout(() => showToast('Database backup created'), 1000);
        }
        function runQuery() {
            const query = prompt('Enter SQL query:', 'SELECT * FROM students WHERE status = \'Active\' LIMIT 10;');
            if (query) {
                addLog(`> Executing: ${query}`);
                addLog(`> Query returned ${data.students.filter(s => s.status === 'Active').length} rows in 12ms`);
                showToast('Query executed successfully');
            }
        }
        function addLog(msg) {
            const log = document.getElementById('sync-log');
            if (log) {
                log.innerHTML += `<p>${msg}</p>`;
                log.scrollTop = log.scrollHeight;
            }
        }

        // Toast
        function showToast(msg, isError = false) {
            const toast = document.getElementById('toast');
            document.getElementById('toast-msg').textContent = msg;
            toast.classList.remove('hidden');
            setTimeout(() => toast.classList.add('hidden'), 3000);
        }

        // Init
        lucide.createIcons();
        renderAll();
    </script>
</body>
</html>
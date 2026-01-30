'use client';

import { useState, useEffect, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/lib/auth-context';
import { api } from '@/lib/api';
import { Button, Modal, Toast } from '@/components/shared';
import { TaskList, TaskForm } from '@/components/tasks';
import type { Task, TaskCreate } from '@/types';

type FilterType = 'all' | 'pending' | 'completed';
type ToastType = { message: string; type: 'success' | 'error' | 'info' } | null;

export default function DashboardPage() {
  const { user, isLoading: authLoading } = useAuth();
  const router = useRouter();

  const [tasks, setTasks] = useState<Task[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [filter, setFilter] = useState<FilterType>('all');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [toast, setToast] = useState<ToastType>(null);

  const fetchTasks = useCallback(async () => {
    try {
      setIsLoading(true);
      const completed = filter === 'all' ? undefined : filter === 'completed';
      const data = await api.getTasks(completed);
      setTasks(data);
    } catch {
      setToast({ message: 'Failed to load tasks', type: 'error' });
    } finally {
      setIsLoading(false);
    }
  }, [filter]);

  useEffect(() => {
    if (!authLoading && !user) {
      router.push('/login');
    }
  }, [user, authLoading, router]);

  useEffect(() => {
    if (user) {
      fetchTasks();
    }
  }, [user, fetchTasks]);

  const handleCreateTask = async (data: TaskCreate) => {
    setIsSubmitting(true);
    try {
      await api.createTask(data);
      setIsModalOpen(false);
      setToast({ message: 'Task created successfully', type: 'success' });
      fetchTasks();
    } catch {
      setToast({ message: 'Failed to create task', type: 'error' });
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleUpdateTask = async (data: TaskCreate) => {
    if (!editingTask) return;

    setIsSubmitting(true);
    try {
      await api.updateTask(editingTask.id, data);
      setEditingTask(null);
      setIsModalOpen(false);
      setToast({ message: 'Task updated successfully', type: 'success' });
      fetchTasks();
    } catch {
      setToast({ message: 'Failed to update task', type: 'error' });
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleToggleTask = async (id: number) => {
    try {
      await api.toggleTaskCompletion(id);
      fetchTasks();
    } catch {
      setToast({ message: 'Failed to update task', type: 'error' });
    }
  };

  const handleDeleteTask = async (id: number) => {
    if (!confirm('Are you sure you want to delete this task?')) return;

    try {
      await api.deleteTask(id);
      setToast({ message: 'Task deleted successfully', type: 'success' });
      fetchTasks();
    } catch {
      setToast({ message: 'Failed to delete task', type: 'error' });
    }
  };

  const openCreateModal = () => {
    setEditingTask(null);
    setIsModalOpen(true);
  };

  const openEditModal = (task: Task) => {
    setEditingTask(task);
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
    setEditingTask(null);
  };

  if (authLoading || !user) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="h-10 w-10 animate-spin rounded-full border-4 border-indigo-600 border-t-transparent" />
      </div>
    );
  }

  const completedCount = tasks.filter((t) => t.completed).length;
  const pendingCount = tasks.filter((t) => !t.completed).length;

  return (
    <div className="mx-auto max-w-4xl px-4 py-8 sm:px-6">
      {/* Header */}
      <div className="mb-8 flex flex-col items-start justify-between gap-4 sm:flex-row sm:items-center">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-gray-900">My Tasks</h1>
          <p className="mt-1.5 text-gray-600">
            {pendingCount} pending • {completedCount} completed
          </p>
        </div>

        <button
          onClick={openCreateModal}
          className="inline-flex items-center gap-2 rounded-lg bg-indigo-600 px-5 py-2.5 text-sm font-medium text-white shadow-sm transition-colors hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
        >
          <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M12 4v16m8-8H4" />
          </svg>
          Add Task
        </button>
      </div>

      {/* Filters */}
      <div className="mb-6 flex flex-wrap gap-2">
        {(['all', 'pending', 'completed'] as const).map((f) => (
          <button
            key={f}
            onClick={() => setFilter(f)}
            className={`
              rounded-lg px-5 py-2 text-sm font-medium transition-all
              ${
                filter === f
                  ? 'bg-indigo-600 text-white shadow-sm'
                  : 'border border-gray-300 bg-white text-gray-700 hover:bg-gray-50 active:bg-gray-100'
              }
            `}
          >
            {f.charAt(0).toUpperCase() + f.slice(1)}
          </button>
        ))}
      </div>

      {/* Task List */}
      <TaskList
        tasks={tasks}
        isLoading={isLoading}
        onToggle={handleToggleTask}
        onEdit={openEditModal}
        onDelete={handleDeleteTask}
      />

      {/* Modal */}
      <Modal
        isOpen={isModalOpen}
        onClose={closeModal}
        title={editingTask ? 'Edit Task' : 'Create Task'}
      >
        <TaskForm
          task={editingTask}
          onSubmit={editingTask ? handleUpdateTask : handleCreateTask}
          onCancel={closeModal}
          isLoading={isSubmitting}
        />
      </Modal>

      {/* Toast */}
      {toast && (
        <Toast
          message={toast.message}
          type={toast.type}
          onClose={() => setToast(null)}
        />
      )}
    </div>
  );
}

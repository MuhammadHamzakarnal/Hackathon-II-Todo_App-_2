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
        <div className="animate-spin w-8 h-8 border-4 border-indigo-600 border-t-transparent rounded-full" />
      </div>
    );
  }

  const completedCount = tasks.filter((t) => t.completed).length;
  const pendingCount = tasks.filter((t) => !t.completed).length;

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 py-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-8">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">My Tasks</h1>
          <p className="text-gray-600 mt-1">
            {pendingCount} pending, {completedCount} completed
          </p>
        </div>
        <Button onClick={openCreateModal}>
          <svg className="w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
          </svg>
          Add Task
        </Button>
      </div>

      {/* Filters */}
      <div className="flex gap-2 mb-6">
        {(['all', 'pending', 'completed'] as const).map((f) => (
          <button
            key={f}
            onClick={() => setFilter(f)}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
              filter === f
                ? 'bg-indigo-600 text-white'
                : 'bg-white text-gray-600 hover:bg-gray-100 border border-gray-200'
            }`}
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

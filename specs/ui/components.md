# Component Specification: UI Components

**Feature Branch**: `ui-components`
**Created**: 2026-01-16
**Status**: Draft
**Input**: User description: "Build responsive, reusable components for the Todo app frontend."

## Component Catalog

### Core Component: Task Card

**Purpose**: Display individual task details with interactive controls.

**Props**:
```typescript
interface TaskCardProps {
  task: {
    id: string;
    title: string;
    description?: string;
    due_date: string;
    status: 'pending' | 'completed';
    created_at: string;
    updated_at: string;
  };
  onEdit: (taskId: string) => void;
  onDelete: (taskId: string) => void;
  onToggleComplete: (taskId: string) => void;
  isLoading?: boolean;
  error?: string;
}
```

**Visual States**:
- **Default**: Full task details with edit/delete/toggle buttons
- **Loading**: Skeleton loader while data fetches
- **Error**: Error message with retry option
- **Empty**: Placeholder for no tasks

**Behavior**:
- Click edit button → opens edit modal/form
- Click delete button → confirmation dialog → delete
- Click complete toggle → instantly updates status
- Responsive layout adapts to screen size

**Accessibility**:
- ARIA labels for all buttons
- Keyboard navigation support
- Screen reader friendly status indicators

---

### Core Component: Task List

**Purpose**: Display collection of tasks with performance optimizations.

**Props**:
```typescript
interface TaskListProps {
  tasks: Task[];
  onTaskAction: (action: 'edit' | 'delete' | 'complete', taskId: string) => void;
  isLoading?: boolean;
  emptyMessage?: string;
  error?: string;
}
```

**Performance Requirements**:
- Virtual scrolling for large lists (>50 tasks)
- Memoized Task Card components to prevent unnecessary re-renders
- Lazy loading for initial render
- Optimized React keys using task IDs

**Behavior**:
- Sorts tasks by due date (ascending) by default
- Filtering capability (status, search)
- Pagination for large datasets
- Pull-to-refresh on mobile

**Empty States**:
- No tasks: "No tasks yet. Create your first task!"
- No matching filters: "No tasks match your filters"
- Error: "Failed to load tasks. Please try again."

---

### Form Components

#### Signup/Login Form
**Fields**:
- Email (required, validated format)
- Password (required, min 8 chars, strength indicator)
- Confirm password (signup only)

**Validation**:
- Real-time field validation
- Submission validation with clear error messages
- Password strength meter
- Email format verification

**States**:
- Pristine: Empty form
- Valid: All inputs valid
- Invalid: Validation errors shown
- Submitting: Loading spinner, disabled inputs
- Submitted: Success message, redirect

#### Task Create/Edit Form
**Fields**:
- Title (required, max 100 chars)
- Description (optional, markdown support)
- Due Date (date picker with time)
- Status (radio: pending/completed)

**Validation**:
- Title required
- Due date must be future or today
- Character limits enforced

---

### Navigation Component

**Purpose**: Global navigation with user context.

**Desktop Layout**:
```
[Logo] [Search] [User Avatar] [Logout]
```

**Mobile Layout**:
```
[Menu Toggle] [Logo] [User Avatar]
└─ Expanded Menu:
   [Search] [Tasks] [Profile] [Logout]
```

**User Info**:
- Avatar with initials fallback
- Email display
- Logout confirmation

**Responsive Behavior**:
- Mobile: Hamburger menu
- Tablet: Condensed navigation
- Desktop: Full navigation bar

---

### Feedback Components

#### Button Variants
```typescript
type ButtonVariant = 'primary' | 'secondary' | 'danger' | 'success' | 'outline';
type ButtonSize = 'sm' | 'md' | 'lg';
```

**States**: Default, Hover, Active, Disabled, Loading

**Accessibility**: Focus states, ARIA labels, keyboard activation

#### Notification System
**Types**: Success, Error, Warning, Info

**Behavior**:
- Auto-dismiss after 5 seconds (configurable)
- Manual dismiss with close button
- Stack multiple notifications
- Persistent for important errors

#### Loading Indicators
- Page-level spinner (full screen overlay)
- Component-level skeleton
- Button-level spinner
- Progress bar for long operations

---

## Design System Guidelines

### Responsive Breakpoints
```css
/* Tailwind defaults */
sm: 640px
md: 768px
lg: 1024px
xl: 1280px
2xl: 1536px
```

### Color Palette
- **Primary**: Blue 600 (#2563eb) - main actions
- **Secondary**: Gray 600 (#4b5563) - secondary elements
- **Success**: Green 600 (#16a34a) - success states
- **Error**: Red 600 (#dc2626) - error states
- **Warning**: Yellow 600 (#ca8a04) - warning states
- **Background**: White (#ffffff) / Gray 50 (#f9fafb)

### Typography
- **Headings**: Inter, system-ui, sans-serif
- **Body**: Inter, system-ui, sans-serif
- **Code**: JetBrains Mono, monospace

### Spacing Scale
- **Base**: 4px (0.25rem)
- **Multiples**: 2x, 3x, 4x, 6x, 8x, 12x, 16x

### Animation Principles
- **Duration**: 150ms (quick), 300ms (standard), 500ms (deliberate)
- **Easing**: Cubic bezier for natural motion
- **Purpose**: Only enhance UX (notifications, transitions)
- **Performance**: GPU-accelerated transforms, will-change for complex animations

## Implementation Requirements

### Technical Stack
- **Framework**: Next.js 16+ with React 18
- **Styling**: Tailwind CSS with JIT compilation
- **Icons**: Lucide React or similar icon library
- **State**: React Context + useState/useReducer
- **Forms**: React Hook Form with Zod validation
- **Testing**: Jest + React Testing Library

### Performance Standards
- **FCP**: < 1.0s
- **LCP**: < 2.5s
- **CLS**: < 0.1
- **INP**: < 200ms
- **Bundle Size**: Component chunks < 10KB

### Accessibility Compliance
- **WCAG**: AA compliance
- **Keyboard**: Full navigation support
- **Screen Readers**: ARIA labels, semantic HTML
- **Color Contrast**: 4.5:1 minimum
- **Focus Management**: Logical tab order, visible focus indicators

### Code Quality
- **Type Safety**: TypeScript strict mode
- **Testing**: > 80% component test coverage
- **Documentation**: Props documentation with Storybook/JSDoc
- **Reusability**: Generic components with specific implementations
- **Maintainability**: Clean imports, consistent naming

## Component Dependencies

### Shared Dependencies
```
components/
├── shared/
│   ├── Button/
│   ├── Input/
│   ├── Card/
│   └── Modal/
├── tasks/
│   ├── TaskCard/
│   ├── TaskList/
│   └── TaskForm/
├── auth/
│   ├── LoginForm/
│   └── SignupForm/
└── layout/
    ├── Header/
    ├── Footer/
    └── Navigation/
```

### Third-Party Dependencies
- `date-fns` for date formatting
- `react-hook-form` for form handling
- `zod` for validation schemas
- `framer-motion` for animations (optional)
- `@tanstack/react-virtual` for virtualization
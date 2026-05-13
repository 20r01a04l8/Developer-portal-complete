import { Routes, Route } from 'react-router-dom';
import { MainLayout } from '../layouts/MainLayout';
import {
  HomePage,
  ProjectListPage,
  ProjectFormPage,
  ProjectDetailPage,
  TaskListPage,
  TaskFormPage,
  TaskDetailPage,
} from '../pages';

export const AppRoutes = () => {
  return (
    <Routes>
      <Route path="/" element={<MainLayout />}>
        <Route index element={<HomePage />} />
        
        <Route path="projects">
          <Route index element={<ProjectListPage />} />
          <Route path="create" element={<ProjectFormPage />} />
          <Route path=":id" element={<ProjectDetailPage />} />
          <Route path=":id/edit" element={<ProjectFormPage />} />
        </Route>

        <Route path="tasks">
          <Route index element={<TaskListPage />} />
          <Route path="create" element={<TaskFormPage />} />
          <Route path=":id" element={<TaskDetailPage />} />
          <Route path=":id/edit" element={<TaskFormPage />} />
        </Route>
      </Route>
    </Routes>
  );
};
